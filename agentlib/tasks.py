"""Estado durável de tarefas para orquestração com múltiplos agentes.

O arquivo de tarefa é a fonte de verdade para ownership e transições. Ele não
substitui as mensagens entre agentes: registra o acordo que já foi confirmado.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .core import AgentLibError, FileLock, assert_no_links, dump_json, read_json, resolve_child, write_atomic

TASK_ID = re.compile(r"^[a-zA-Z0-9_.-]{1,100}$")
STATES = ("planned", "ready", "running", "blocked", "review", "done")
ACTIVE_STATES = frozenset(STATES) - {"done"}
TRANSITIONS = {
    "planned": {"ready", "blocked"},
    "ready": {"running", "blocked"},
    "running": {"review", "blocked"},
    "review": {"running", "blocked", "done"},
    "blocked": {"ready"},
    "done": set(),
}


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _paths(paths: Iterable[str]) -> List[str]:
    result: List[str] = []
    for value in paths:
        path = str(value).replace("\\", "/").strip("/")
        if not path or re.match(r"^[A-Za-z]:", path) or path.startswith("../") or "/../" in path or path == "..":
            raise AgentLibError(f"Caminho reservado invalido: {value}")
        if path not in result:
            result.append(path)
    if not result:
        raise AgentLibError("Uma tarefa precisa reservar pelo menos um caminho.")
    return result


def _paths_overlap(left: str, right: str) -> bool:
    """Considera conflito exato e relação diretório/descendente."""
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def _task_path(project: Path, task_id: str) -> Path:
    if not TASK_ID.fullmatch(task_id or ""):
        raise AgentLibError(f"ID de tarefa invalido: {task_id}")
    return resolve_child(project, f".work/tasks/{task_id}.json")


def _task_lock(project: Path) -> Path:
    return resolve_child(project, ".work/tasks/.writer.lock")


def _read_task(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        raise AgentLibError(f"Tarefa ausente: {path.name}")
    try:
        task = read_json(path)
    except ValueError as exc:
        raise AgentLibError(f"Tarefa JSON invalida: {path.name}: {exc}")
    if task.get("schemaVersion") != 1 or task.get("id") != path.stem or task.get("state") not in STATES:
        raise AgentLibError(f"Tarefa incompativel: {path.name}")
    return task


def _assert_owner(task: Dict[str, Any], runtime_id: str) -> None:
    owner = task.get("owner", {})
    expected = owner.get("runtimeId", "")
    if expected and expected != runtime_id:
        raise AgentLibError(f"Somente o owner runtime {expected} pode alterar a tarefa {task['id']}.")


def _active_tasks(tasks_dir: Path) -> Iterable[Dict[str, Any]]:
    if not tasks_dir.is_dir():
        return []
    tasks = []
    for path in tasks_dir.glob("*.json"):
        tasks.append(_read_task(path))
    return tasks


def create_task(
    project_path: str,
    task_id: str,
    objective: str,
    owner_role: str,
    owner_runtime_id: str,
    paths: Iterable[str],
    dependencies: Iterable[str] = (),
) -> Dict[str, Any]:
    """Cria uma tarefa e recusa conflitos de escrita com tarefas ativas."""
    project = Path(project_path).resolve()
    assert_no_links(project)
    if project.is_file():
        raise AgentLibError("Projeto e um arquivo.")
    if not objective.strip() or not owner_role.strip():
        raise AgentLibError("Objetivo e papel responsavel sao obrigatorios.")
    reserved = _paths(paths)
    target = _task_path(project, task_id)
    tasks_dir = target.parent
    lock = _task_lock(project)
    dependencies = list(dict.fromkeys(str(value) for value in dependencies if str(value).strip()))

    with FileLock(lock, stale_after=120.0, wait=10.0, purpose="tarefas"):
        if target.exists():
            raise AgentLibError(f"Tarefa ja existe: {task_id}")
        for other in _active_tasks(tasks_dir):
            if other["state"] not in ACTIVE_STATES:
                continue
            overlap = sorted(
                left
                for left in reserved
                if any(_paths_overlap(left, right) for right in other.get("ownership", {}).get("paths", []))
            )
            if overlap:
                raise AgentLibError(
                    f"Conflito de ownership com {other['id']} ({other['state']}): {', '.join(overlap)}"
                )
        task = {
            "schemaVersion": 1,
            "id": task_id,
            "objective": objective.strip(),
            "state": "planned",
            "owner": {"role": owner_role.strip(), "runtimeId": owner_runtime_id.strip()},
            "ownership": {"paths": reserved},
            "dependencies": dependencies,
            "ack": None,
            "contracts": [],
            "history": [{"at": _now(), "event": "created", "actorRuntimeId": owner_runtime_id.strip()}],
        }
        write_atomic(target, dump_json(task))
    return task


def acknowledge_task(project_path: str, task_id: str, runtime_id: str, note: str = "") -> Dict[str, Any]:
    """Registra o ACK do executor antes de ele iniciar trabalho dependente."""
    project = Path(project_path).resolve()
    target = _task_path(project, task_id)
    with FileLock(_task_lock(project), stale_after=120.0, wait=10.0, purpose="tarefas"):
        task = _read_task(target)
        _assert_owner(task, runtime_id)
        if task["state"] == "done":
            raise AgentLibError("Nao e possivel confirmar uma tarefa concluida.")
        task["ack"] = {"runtimeId": runtime_id, "at": _now(), "note": note.strip()}
        task["history"].append({"at": _now(), "event": "ack", "actorRuntimeId": runtime_id})
        write_atomic(target, dump_json(task))
    return task


def transition_task(project_path: str, task_id: str, state: str, runtime_id: str, note: str = "") -> Dict[str, Any]:
    """Faz uma transição válida e exige ACK antes de execução, revisão ou conclusão."""
    if state not in STATES:
        raise AgentLibError(f"Estado invalido: {state}")
    project = Path(project_path).resolve()
    target = _task_path(project, task_id)
    with FileLock(_task_lock(project), stale_after=120.0, wait=10.0, purpose="tarefas"):
        task = _read_task(target)
        _assert_owner(task, runtime_id)
        current = task["state"]
        if state not in TRANSITIONS[current]:
            raise AgentLibError(f"Transicao invalida: {current} -> {state}")
        if state in {"running", "review", "done"} and not task.get("ack"):
            raise AgentLibError("ACK do owner e obrigatorio antes de executar, revisar ou concluir.")
        pending_contracts = [item["id"] for item in task.get("contracts", []) if item.get("state") != "accepted"]
        if state in {"running", "review", "done"} and pending_contracts:
            raise AgentLibError(f"Contratos sem aceite: {', '.join(pending_contracts)}")
        if state == "done":
            pending_dependencies = []
            for dependency in task.get("dependencies", []):
                dependency_task = _read_task(_task_path(project, dependency))
                if dependency_task["state"] != "done":
                    pending_dependencies.append(dependency)
            if pending_dependencies:
                raise AgentLibError(f"Dependencias pendentes: {', '.join(pending_dependencies)}")
        task["state"] = state
        task["history"].append({"at": _now(), "event": f"state:{state}", "actorRuntimeId": runtime_id, "note": note.strip()})
        write_atomic(target, dump_json(task))
    return task


def transfer_task(
    project_path: str,
    task_id: str,
    current_runtime_id: str,
    new_role: str,
    new_runtime_id: str,
    note: str = "",
) -> Dict[str, Any]:
    """Transfere ownership explicitamente e invalida o ACK anterior."""
    if not new_role.strip() or not new_runtime_id.strip():
        raise AgentLibError("Novo papel e runtime ID sao obrigatorios.")
    project = Path(project_path).resolve()
    target = _task_path(project, task_id)
    with FileLock(_task_lock(project), stale_after=120.0, wait=10.0, purpose="tarefas"):
        task = _read_task(target)
        _assert_owner(task, current_runtime_id)
        if task["state"] == "done":
            raise AgentLibError("Nao e possivel transferir uma tarefa concluida.")
        task["owner"] = {"role": new_role.strip(), "runtimeId": new_runtime_id.strip()}
        task["ack"] = None
        task["history"].append({
            "at": _now(), "event": "ownership-transferred", "actorRuntimeId": current_runtime_id,
            "newRuntimeId": new_runtime_id.strip(), "note": note.strip(),
        })
        write_atomic(target, dump_json(task))
    return task


def propose_contract(
    project_path: str,
    task_id: str,
    contract_id: str,
    version: str,
    owner_runtime_id: str,
    consumer_runtime_id: str,
    summary: str,
) -> Dict[str, Any]:
    """Registra uma versão de contrato que exige aceite explícito do consumidor."""
    if not TASK_ID.fullmatch(contract_id or "") or not version.strip():
        raise AgentLibError("ID e versao de contrato sao obrigatorios.")
    if not consumer_runtime_id.strip() or not summary.strip():
        raise AgentLibError("Consumidor e resumo do contrato sao obrigatorios.")
    project = Path(project_path).resolve()
    target = _task_path(project, task_id)
    with FileLock(_task_lock(project), stale_after=120.0, wait=10.0, purpose="tarefas"):
        task = _read_task(target)
        _assert_owner(task, owner_runtime_id)
        if any(item["id"] == contract_id and item["version"] == version for item in task.get("contracts", [])):
            raise AgentLibError(f"Contrato ja existe: {contract_id}@{version}")
        task.setdefault("contracts", []).append({
            "id": contract_id,
            "version": version.strip(),
            "ownerRuntimeId": owner_runtime_id,
            "consumerRuntimeId": consumer_runtime_id.strip(),
            "summary": summary.strip(),
            "state": "proposed",
            "proposedAt": _now(),
            "acceptedAt": None,
        })
        task["history"].append({"at": _now(), "event": f"contract-proposed:{contract_id}@{version}", "actorRuntimeId": owner_runtime_id})
        write_atomic(target, dump_json(task))
    return task


def accept_contract(
    project_path: str, task_id: str, contract_id: str, version: str, consumer_runtime_id: str
) -> Dict[str, Any]:
    """Aceita exatamente a versão proposta; silêncio nunca equivale a aceite."""
    project = Path(project_path).resolve()
    target = _task_path(project, task_id)
    with FileLock(_task_lock(project), stale_after=120.0, wait=10.0, purpose="tarefas"):
        task = _read_task(target)
        contract = next(
            (item for item in task.get("contracts", []) if item["id"] == contract_id and item["version"] == version),
            None,
        )
        if contract is None:
            raise AgentLibError(f"Contrato ausente: {contract_id}@{version}")
        if contract["consumerRuntimeId"] != consumer_runtime_id:
            raise AgentLibError(f"Somente o consumidor {contract['consumerRuntimeId']} pode aceitar o contrato.")
        contract["state"] = "accepted"
        contract["acceptedAt"] = _now()
        task["history"].append({"at": _now(), "event": f"contract-accepted:{contract_id}@{version}", "actorRuntimeId": consumer_runtime_id})
        write_atomic(target, dump_json(task))
    return task


def read_task(project_path: str, task_id: str) -> Dict[str, Any]:
    project = Path(project_path).resolve()
    target = _task_path(project, task_id)
    return _read_task(target)
