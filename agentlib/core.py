"""Utilitarios compartilhados: caminhos seguros, IO UTF-8, hashes, escrita atomica e travas.

Somente biblioteca padrao (Python 3.9+), para rodar igual em Windows, Linux e macOS.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import socket
import stat
import sys
import time
import uuid
from pathlib import Path
from typing import Optional, Union

# Raiz da biblioteca: na fonte e a pasta do repositorio; num projeto instalado e .agent-library/.
LIBRARY_ROOT = Path(__file__).resolve().parent.parent
NL = "\n"
_REPARSE_MOUNT_POINT = getattr(stat, "IO_REPARSE_TAG_MOUNT_POINT", 0xA0000003)
_REPARSE_SYMLINK = getattr(stat, "IO_REPARSE_TAG_SYMLINK", 0xA000000C)


class AgentLibError(Exception):
    """Erro esperado e explicado ao usuario (sem traceback)."""


def is_installed_copy(root: Path = LIBRARY_ROOT) -> bool:
    """True quando o motor roda a partir de .agent-library/ de um projeto (sem perfis/fontes completas)."""
    return root.name == ".agent-library" or not (root / "profiles").is_dir()


def warn(message: str) -> None:
    print(f"ATENCAO: {message}", file=sys.stderr)


# ---------------------------------------------------------------- IO

def read_text(path: Union[str, Path]) -> str:
    """Le UTF-8 preservando quebras de linha originais; remove BOM como o .NET fazia."""
    return Path(path).read_bytes().decode("utf-8-sig")


def read_json(path: Union[str, Path]):
    return json.loads(read_text(path))


def dump_json(data) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + NL


def byte_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def text_hash(text: str) -> str:
    return byte_hash(text.encode("utf-8"))


def file_hash(path: Union[str, Path]) -> str:
    return byte_hash(Path(path).read_bytes())


# ---------------------------------------------------------------- caminhos

def _same_path(a: Path, b: Path) -> bool:
    return os.path.normcase(str(a)) == os.path.normcase(str(b))


def is_link(path: Union[str, Path]) -> bool:
    """Symlink ou junction (Windows). Placeholders de nuvem (OneDrive) nao contam como link."""
    try:
        info = os.lstat(path)
    except (FileNotFoundError, NotADirectoryError):
        return False
    if stat.S_ISLNK(info.st_mode):
        return True
    tag = getattr(info, "st_reparse_tag", 0)
    return tag in (_REPARSE_MOUNT_POINT, _REPARSE_SYMLINK)


def assert_no_links(path: Union[str, Path], stop_at: Optional[Union[str, Path]] = None) -> None:
    """Recusa links no caminho, subindo ate stop_at (inclusive) ou ate a raiz do disco."""
    cursor = Path(os.path.abspath(path))
    stop = Path(os.path.abspath(stop_at)) if stop_at is not None else None
    while True:
        if is_link(cursor):
            raise AgentLibError(f"Link ou junction nao permitido: {cursor}")
        if stop is not None and _same_path(cursor, stop):
            return
        if cursor.parent == cursor:
            return
        cursor = cursor.parent


def resolve_child(root: Union[str, Path], relative: str) -> Path:
    """Resolve caminho relativo garantindo que permanece dentro de root."""
    rel = str(relative or "")
    if not rel.strip() or os.path.isabs(rel) or re.match(r"^[A-Za-z]:", rel) or rel.startswith(("/", "\\")):
        raise AgentLibError(f"Caminho relativo invalido: {relative}")
    base = os.path.abspath(str(root)).rstrip("\\/")
    result = os.path.abspath(os.path.join(base, rel))
    if not os.path.normcase(result).startswith(os.path.normcase(base) + os.sep):
        raise AgentLibError(f"Caminho fora do destino: {relative}")
    return Path(result)


# ---------------------------------------------------------------- escrita

def _replace_with_retry(source: Path, destination: Path) -> None:
    # Antivirus/indexador no Windows podem segurar o arquivo por alguns milissegundos.
    for attempt in range(1, 11):
        try:
            os.replace(source, destination)
            return
        except PermissionError:
            if attempt == 10:
                raise
            time.sleep(0.05 * attempt)


def write_atomic(path: Union[str, Path], data: Union[str, bytes], backup: Optional[Union[str, Path]] = None) -> None:
    """Grava em temporario no mesmo diretorio, fsync e substitui atomicamente.

    Com backup, a versao anterior e copiada (tambem atomicamente) antes da troca.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = data.encode("utf-8") if isinstance(data, str) else data
    temporary = target.with_name(f"{target.name}.{uuid.uuid4().hex}.tmp")
    try:
        with open(temporary, "xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if backup is not None and target.exists():
            backup_path = Path(backup)
            backup_tmp = backup_path.with_name(f"{backup_path.name}.{uuid.uuid4().hex}.tmp")
            try:
                with open(backup_tmp, "xb") as handle:
                    handle.write(target.read_bytes())
                    handle.flush()
                    os.fsync(handle.fileno())
                _replace_with_retry(backup_tmp, backup_path)
            finally:
                if backup_tmp.exists():
                    backup_tmp.unlink()
        _replace_with_retry(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()


# ---------------------------------------------------------------- travas

class FileLock:
    """Trava entre processos baseada em criacao exclusiva de arquivo (funciona em qualquer SO).

    O arquivo guarda dono e horario. Travas mais antigas que stale_after segundos sao
    consideradas abandonadas (processo morto) e removidas com aviso. Arquivos de trava
    legados (vazios, da versao PowerShell 0.3.x) sao removidos se nenhum processo os segura.
    """

    def __init__(self, path: Union[str, Path], stale_after: float, wait: float = 0.0, purpose: str = "operacao"):
        self.path = Path(path)
        self.stale_after = stale_after
        self.wait = max(0.0, wait)
        self.purpose = purpose
        self.token = uuid.uuid4().hex
        self.held = False

    def _busy_message(self) -> str:
        owner = ""
        try:
            info = json.loads(self.path.read_text("utf-8"))
            owner = f" (pid {info.get('pid')} em {info.get('host')}, desde {info.get('created')})"
        except Exception:
            pass
        return (f"{self.purpose.capitalize()} em uso por outro escritor{owner}; tente novamente apos o escritor "
                f"concluir ou use --wait. Trava: {self.path}")

    def _clear_stale(self) -> bool:
        """Remove a trava se estiver abandonada. Retorna True se o caminho ficou livre."""
        try:
            raw = self.path.read_bytes()
        except FileNotFoundError:
            return True
        except PermissionError:
            return False  # outro processo segura o arquivo (ex.: PowerShell 0.3.x)
        try:
            info = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            info = None
        try:
            age = time.time() - self.path.stat().st_mtime
        except FileNotFoundError:
            return True
        if not isinstance(info, dict) or info.get("tool") != "agentlib":
            if age < 2:
                return False  # pode ser uma trava sendo escrita agora
            return self._remove()
        created = float(info.get("createdEpoch", 0) or 0)
        if time.time() - created > self.stale_after:
            warn(f"Trava abandonada removida ({self.path}; pid {info.get('pid')}, {info.get('created')}).")
            return self._remove()
        return False

    def _remove(self) -> bool:
        try:
            self.path.unlink()
            return True
        except FileNotFoundError:
            return True
        except PermissionError:
            return False

    def wait_until_free(self) -> None:
        """Para leitores: espera nao haver escritor, sem criar a trava."""
        deadline = time.monotonic() + self.wait
        while self.path.exists() and not self._clear_stale():
            if time.monotonic() >= deadline:
                raise AgentLibError(self._busy_message())
            time.sleep(0.1)

    def acquire(self) -> "FileLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.wait
        while True:
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                if self._clear_stale():
                    continue
                if time.monotonic() >= deadline:
                    raise AgentLibError(self._busy_message())
                time.sleep(0.1)
                continue
            except PermissionError:
                if time.monotonic() >= deadline:
                    raise AgentLibError(self._busy_message())
                time.sleep(0.1)
                continue
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump({
                    "tool": "agentlib", "token": self.token, "pid": os.getpid(), "host": socket.gethostname(),
                    "purpose": self.purpose, "createdEpoch": time.time(),
                    "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                }, handle)
            self.held = True
            return self

    def release(self) -> None:
        if not self.held:
            return
        self.held = False
        try:
            info = json.loads(self.path.read_text("utf-8"))
            if info.get("token") != self.token:
                return  # trava foi quebrada e assumida por outro processo
        except (FileNotFoundError, ValueError):
            return
        self._remove()

    def __enter__(self) -> "FileLock":
        return self.acquire()

    def __exit__(self, *_exc) -> None:
        self.release()
