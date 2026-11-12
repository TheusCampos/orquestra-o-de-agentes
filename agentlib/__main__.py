"""CLI portável da biblioteca de orquestração."""
from __future__ import annotations

import argparse
import json
import sys

from .catalog import validate
from .core import AgentLibError
from .memory import query_memory_sqlite, read_memory, record_memory
from .sync import sync_project
from .tasks import (
    accept_contract, acknowledge_task, create_task, propose_contract,
    read_task, transfer_task, transition_task,
)


def _print(value) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2) if isinstance(value, dict) else value)


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m agentlib", description="Biblioteca de orquestração de agentes")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="validar catálogo, perfis e skills")
    sync = commands.add_parser("sync", help="instalar ou sincronizar um perfil em um projeto")
    sync.add_argument("project_path")
    sync.add_argument("--profile", default="general")
    memory = commands.add_parser("memory", help="ler ou registrar memória")
    memory.add_argument("action", choices=["Read", "Init", "Record", "Recover", "Sync", "Query"], default="Read")
    memory.add_argument("--project-path", default=".")
    memory.add_argument("--kind", default="checkpoint")
    memory.add_argument("--actor", default="orchestrator")
    memory.add_argument("--content", default="")
    memory.add_argument("--evidence", default="")
    memory.add_argument("--confidence", default="reported")
    memory.add_argument("--id", default="")
    memory.add_argument("--supersedes", default="")
    memory.add_argument("--search", default="")
    memory.add_argument("--limit", type=int, default=20)
    memory.add_argument("--query-sql", default="SELECT * FROM events ORDER BY rowid DESC LIMIT 20", help="consulta SQL no banco memory.sqlite")
    task = commands.add_parser("task", help="criar e atualizar tarefas com ownership")
    task_commands = task.add_subparsers(dest="task_command", required=True)
    create = task_commands.add_parser("create")
    create.add_argument("--project-path", default=".")
    create.add_argument("--id", required=True)
    create.add_argument("--objective", required=True)
    create.add_argument("--role", required=True)
    create.add_argument("--runtime-id", default="")
    create.add_argument("--paths", required=True, help="caminhos separados por vírgula")
    create.add_argument("--dependencies", default="")
    ack = task_commands.add_parser("ack")
    ack.add_argument("--project-path", default=".")
    ack.add_argument("--id", required=True)
    ack.add_argument("--runtime-id", required=True)
    ack.add_argument("--note", default="")
    transition = task_commands.add_parser("transition")
    transition.add_argument("--project-path", default=".")
    transition.add_argument("--id", required=True)
    transition.add_argument("--state", required=True)
    transition.add_argument("--runtime-id", required=True)
    transition.add_argument("--note", default="")
    transfer = task_commands.add_parser("transfer")
    transfer.add_argument("--project-path", default=".")
    transfer.add_argument("--id", required=True)
    transfer.add_argument("--runtime-id", required=True)
    transfer.add_argument("--new-role", required=True)
    transfer.add_argument("--new-runtime-id", required=True)
    transfer.add_argument("--note", default="")
    propose = task_commands.add_parser("propose-contract")
    propose.add_argument("--project-path", default=".")
    propose.add_argument("--id", required=True)
    propose.add_argument("--contract-id", required=True)
    propose.add_argument("--version", required=True)
    propose.add_argument("--runtime-id", required=True)
    propose.add_argument("--consumer-runtime-id", required=True)
    propose.add_argument("--summary", required=True)
    accept = task_commands.add_parser("accept-contract")
    accept.add_argument("--project-path", default=".")
    accept.add_argument("--id", required=True)
    accept.add_argument("--contract-id", required=True)
    accept.add_argument("--version", required=True)
    accept.add_argument("--runtime-id", required=True)
    show = task_commands.add_parser("show")
    show.add_argument("--project-path", default=".")
    show.add_argument("--id", required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            _print(validate())
        elif args.command == "sync":
            _print(sync_project(args.project_path, args.profile)[1])
        elif args.command == "memory":
            if args.action == "Read":
                _print(read_memory(args.project_path, args.search, args.limit))
            elif args.action == "Query":
                _print(query_memory_sqlite(args.project_path, args.query_sql))
            else:
                _print(record_memory(args.project_path, args.action, args.kind, args.actor, args.content, args.evidence, args.confidence, args.id, args.supersedes))
        elif args.task_command == "create":
            _print(create_task(args.project_path, args.id, args.objective, args.role, args.runtime_id, args.paths.split(","), args.dependencies.split(",") if args.dependencies else []))
        elif args.task_command == "ack":
            _print(acknowledge_task(args.project_path, args.id, args.runtime_id, args.note))
        elif args.task_command == "transition":
            _print(transition_task(args.project_path, args.id, args.state, args.runtime_id, args.note))
        elif args.task_command == "transfer":
            _print(transfer_task(args.project_path, args.id, args.runtime_id, args.new_role, args.new_runtime_id, args.note))
        elif args.task_command == "propose-contract":
            _print(propose_contract(args.project_path, args.id, args.contract_id, args.version, args.runtime_id, args.consumer_runtime_id, args.summary))
        elif args.task_command == "accept-contract":
            _print(accept_contract(args.project_path, args.id, args.contract_id, args.version, args.runtime_id))
        else:
            _print(read_task(args.project_path, args.id))
        return 0
    except AgentLibError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
