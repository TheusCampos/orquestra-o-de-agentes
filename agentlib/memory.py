"""Gerenciamento de memoria: BRAIN.md e memory/events.jsonl.

Substitui o script memory.ps1, com leitura e gravacao atomica e locking.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid

from .core import (
    LIBRARY_ROOT, AgentLibError, FileLock, assert_no_links, read_text,
    resolve_child, write_atomic
)

def _get_memory_block(text: str) -> re.Match:
    begin = "<!-- memory:begin -->"
    end = "<!-- memory:end -->"
    begin_count = text.count(begin)
    end_count = text.count(end)
    if begin_count != 1 or end_count != 1:
        raise AgentLibError("BRAIN.md precisa de um par de marcadores memory:begin/end.")
    match = re.search(f"(?s){re.escape(begin)}\\s*.*?\\s*{re.escape(end)}", text)
    if not match:
        raise AgentLibError("Marcadores de memoria fora de ordem.")
    return match

def read_history(events_path: Path) -> List[Dict[str, Any]]:
    if not events_path.is_file():
        return []
    ids = set()
    history = []
    lines = events_path.read_text("utf-8").splitlines()
    for line in lines:
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            raise AgentLibError("Historico JSON invalido; preservar arquivo e reparar antes de registrar.")
        
        required_fields = ["schemaVersion", "id", "timestampUtc", "actor", "kind", "content", "evidence", "confidence", "supersedes"]
        for name in required_fields:
            if name not in event:
                raise AgentLibError(f"Evento sem campo: {name}")
                
        if event["schemaVersion"] != 1 or not re.match(r"^[a-zA-Z0-9_.-]{1,100}$", event["id"]):
            raise AgentLibError("Evento incompativel.")
        if event["id"] in ids:
            raise AgentLibError("Historico possui IDs duplicados.")
        if event["kind"] not in ("request", "decision", "action", "checkpoint", "correction"):
            raise AgentLibError("Tipo de evento invalido.")
        if event["confidence"] not in ("confirmed", "reported", "hypothesis"):
            raise AgentLibError("Confianca de evento invalida.")
        if event["supersedes"] and event["supersedes"] not in ids:
            raise AgentLibError("Supersedes deve apontar para evento anterior existente.")
            
        ids.add(event["id"])
        history.append(event)
    return history

def _set_effective_kinds(history: List[Dict[str, Any]]) -> None:
    by_id = {e["id"]: e for e in history}
    for event in history:
        origin = event
        while origin["kind"] == "correction" and origin["supersedes"]:
            origin = by_id[origin["supersedes"]]
        event["effectiveKind"] = origin["kind"]

def assert_history_present(brain: str, history: List[Dict[str, Any]]) -> None:
    block = _get_memory_block(brain)
    if len(history) == 0 and re.search(r"(?m)^### [a-zA-Z0-9_.-]+ \|", block.group(0)):
        raise AgentLibError("Journal ausente ou vazio para BRAIN.md com eventos; preservar resumo e restaurar historico antes de registrar.")

def _escape_memory(text: str) -> str:
    return text.replace("<!-- memory:", "&lt;!-- memory:")

def read_memory(project_path: str, search: str = "", limit: int = 20) -> str:
    root = Path(project_path).resolve()
    assert_no_links(root)
    if root.is_file():
        raise AgentLibError("Projeto e um arquivo.")
        
    brain_path = resolve_child(root, "BRAIN.md")
    events_path = resolve_child(root, "memory/events.jsonl")
    lock_path = resolve_child(root, "memory/.writer.lock")
    
    for p in [brain_path, events_path, lock_path]:
        assert_no_links(p)
        if p.is_dir():
            raise AgentLibError(f"Arquivo de memoria e pasta: {p}")

    lock = FileLock(lock_path, stale_after=30.0, wait=0.5, purpose="memoria_read")
    lock.wait_until_free()
    
    if not brain_path.is_file():
        raise AgentLibError("BRAIN.md ausente; use -Action Init ou grave primeiro.")
        
    brain = read_text(brain_path)
    _get_memory_block(brain)
    history = read_history(events_path)
    assert_history_present(brain, history)
    
    _set_effective_kinds(history)
    superseded_by: Dict[str, List[str]] = {}
    for event in history:
        if event["supersedes"]:
            superseded_by.setdefault(event["supersedes"], []).append(event["id"])
            
    if search:
        search_lower = search.lower()
        selected_ids = {}
        for event in history:
            text_to_search = f"{event['content']} {event['evidence']} {event['id']}".lower()
            if search_lower in text_to_search:
                selected_ids[event["id"]] = True
                
        while True:
            added = False
            for event in history:
                if event["supersedes"] and event["supersedes"] in selected_ids and event["id"] not in selected_ids:
                    selected_ids[event["id"]] = True
                    added = True
            if not added:
                break
        history = [e for e in history if e["id"] in selected_ids]

    for event in history:
        state = "superseded" if event["id"] in superseded_by else event["confidence"]
        event["effectiveState"] = state
        event["supersededBy"] = superseded_by.get(event["id"], [])
        
    active = [e for e in history if e["id"] not in superseded_by]
    checkpoint = next((e for e in reversed(active) if e.get("effectiveKind") == "checkpoint"), None)
    decisions = [e for e in active if e.get("effectiveKind") == "decision"]
    
    result = {
        "brain": brain,
        "checkpoint": checkpoint,
        "decisions": decisions,
        "events": history[-limit:] if limit > 0 else history
    }
    return json.dumps(result, ensure_ascii=False, indent=2)

def record_memory(
    project_path: str,
    action: str = "Record",  # "Init", "Record", "Recover"
    kind: str = "checkpoint",
    actor: str = "orchestrator",
    content: str = "",
    evidence: str = "",
    confidence: str = "reported",
    event_id: str = "",
    supersedes: str = ""
) -> str:
    root = Path(project_path).resolve()
    assert_no_links(root)
    if root.is_file():
        raise AgentLibError("Projeto e um arquivo.")
        
    brain_path = resolve_child(root, "BRAIN.md")
    events_path = resolve_child(root, "memory/events.jsonl")
    lock_path = resolve_child(root, "memory/.writer.lock")
    backup_path = resolve_child(root, "memory/BRAIN.previous.md")

    if action == "Record":
        if not content.strip():
            raise AgentLibError("Content obrigatorio para Record.")
        if len(content) > 16384 or len(evidence) > 2048:
            raise AgentLibError("Registro muito grande; resuma antes de registrar.")
        if kind == "action" and confidence == "confirmed" and not evidence.strip():
            raise AgentLibError("Acao confirmada exige Evidence.")
        if kind == "correction" and not supersedes:
            raise AgentLibError("Correction exige Supersedes.")
        if not event_id:
            event_id = uuid.uuid4().hex
            
    events_path.parent.mkdir(parents=True, exist_ok=True)
    
    with FileLock(lock_path, stale_after=30.0, wait=10.0, purpose="memoria_write"):
        if action == "Recover":
            if not backup_path.is_file():
                raise AgentLibError("Backup de BRAIN.md ausente; preservar arquivos e reparar manualmente.")
            brain = read_text(backup_path)
        else:
            if brain_path.is_file():
                brain = read_text(brain_path)
            else:
                template_brain = LIBRARY_ROOT / "templates/brain.md"
                brain = read_text(template_brain) if template_brain.is_file() else "<!-- memory:begin -->\n<!-- memory:end -->"
                
        match = _get_memory_block(brain)
        history = read_history(events_path)
        assert_history_present(brain, history)
        
        seen = {}
        for event in history:
            if event["id"] in seen:
                raise AgentLibError("Historico possui IDs duplicados.")
            seen[event["id"]] = event
            
        if action == "Record":
            if supersedes and supersedes not in seen:
                raise AgentLibError("Supersedes deve apontar para evento existente.")
            if supersedes == event_id:
                raise AgentLibError("Evento nao pode substituir a si mesmo.")
                
            if event_id in seen:
                old = seen[event_id]
                if (old["kind"] != kind or old["actor"] != actor or 
                    old["content"] != content or old["evidence"] != evidence or 
                    old["confidence"] != confidence or old["supersedes"] != supersedes):
                    raise AgentLibError("ID existente com conteudo diferente.")
                # Ja registrado
            else:
                new_event = {
                    "schemaVersion": 1,
                    "id": event_id,
                    "timestampUtc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "actor": actor,
                    "kind": kind,
                    "content": content,
                    "evidence": evidence,
                    "confidence": confidence,
                    "supersedes": supersedes
                }
                history.append(new_event)
                lines = [json.dumps(e, ensure_ascii=False, separators=(',', ':')) for e in history]
                serialized = "\n".join(lines) + "\n"
                write_atomic(events_path, serialized)
                
        superseded = {e["supersedes"]: True for e in history if e["supersedes"]}
        _set_effective_kinds(history)
        
        new_lines = ["<!-- memory:begin -->", "## Decisoes ativas (independentes da janela de eventos)"]
        for event in history:
            if event.get("effectiveKind") == "decision" and event["id"] not in superseded:
                content_safe = _escape_memory(event["content"]).replace("\n", " ")
                new_lines.append(f"- [{event['id']}] {event['confidence']}: {content_safe}")
                
        active_history = [e for e in history if e["id"] not in superseded]
        checkpoint = next((e for e in reversed(active_history) if e.get("effectiveKind") == "checkpoint"), None)
        if checkpoint:
            new_lines.append("## Checkpoint atual")
            new_lines.append(f"[{checkpoint['id']}] {_escape_memory(checkpoint['content'])}")
            
        new_lines.append("## Eventos recentes (historico completo: memory/events.jsonl)")
        for event in history[-20:]:
            state = "substituido" if event["id"] in superseded else event["confidence"]
            new_lines.append("")
            new_lines.append(f"### {event['id']} | {event['kind']} | {state} | {event['actor']}")
            new_lines.append(f"Data UTC: {event['timestampUtc']}")
            if event["supersedes"]:
                new_lines.append(f"Substitui: {event['supersedes']}")
            for line in event["content"].splitlines():
                new_lines.append(f"> {_escape_memory(line)}")
            if event["evidence"]:
                for line in event["evidence"].splitlines():
                    new_lines.append(f"> Fonte/evidencia: {_escape_memory(line)}")
                    
        if not history:
            new_lines.append("Sem eventos registrados.")
        new_lines.append("<!-- memory:end -->")
        
        updated = brain[:match.start()] + "\n".join(new_lines) + brain[match.end():]
        
        if action == "Recover":
            write_atomic(brain_path, updated)
        else:
            write_atomic(brain_path, updated, backup=backup_path)
            
    return f"Memoria pronta: {brain_path}"

if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser(description="Gerenciar memoria do agente")
    parser.add_argument("--action", choices=["Init", "Read", "Record", "Recover"], default="Read")
    parser.add_argument("--project_path", default=".")
    parser.add_argument("--kind", choices=["request", "decision", "action", "checkpoint", "correction"], default="checkpoint")
    parser.add_argument("--actor", default="orchestrator")
    parser.add_argument("--content", default="")
    parser.add_argument("--evidence", default="")
    parser.add_argument("--confidence", choices=["confirmed", "reported", "hypothesis"], default="reported")
    parser.add_argument("--id", default="")
    parser.add_argument("--supersedes", default="")
    parser.add_argument("--search", default="")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    
    try:
        if args.action == "Read":
            print(read_memory(args.project_path, args.search, args.limit))
        else:
            print(record_memory(
                args.project_path, args.action, args.kind, args.actor,
                args.content, args.evidence, args.confidence, args.id, args.supersedes
            ))
    except AgentLibError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
