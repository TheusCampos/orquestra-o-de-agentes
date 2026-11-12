import tempfile
import unittest
from pathlib import Path
import json
import sqlite3

from agentlib.catalog import validate
from agentlib.core import AgentLibError
from agentlib.memory import query_memory_sqlite, read_history, read_memory, record_memory
from agentlib.sync import sync_project
from agentlib.tasks import (
    accept_contract, acknowledge_task, create_task, propose_contract,
    read_task, transfer_task, transition_task,
)


class CatalogTests(unittest.TestCase):
    def test_library_catalog_is_consistent(self):
        self.assertIn("29 skills", validate())


class ProjectLearningSyncTests(unittest.TestCase):
    def test_playbook_is_initialized_and_preserved_on_sync(self):
        with tempfile.TemporaryDirectory() as project:
            sync_project(project, "general")
            playbook = Path(project) / "PROJECT_PLAYBOOK.md"
            self.assertTrue(playbook.is_file())
            self.assertTrue((Path(project) / ".agent-library/rules/core/learning.md").is_file())
            playbook.write_text("# Prática comprovada\nUsar teste de contrato.\n", encoding="utf-8")
            sync_project(project, "general")
            self.assertEqual("# Prática comprovada\nUsar teste de contrato.\n", playbook.read_text(encoding="utf-8"))


class MemoryStorageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = self.temp.name

    def tearDown(self):
        self.temp.cleanup()

    def test_record_syncs_jsonl_json_and_sqlite(self):
        record_memory(
            self.project,
            action="Record",
            kind="decision",
            actor="orchestrator",
            content="Decisao sobre arquitetura de dados",
            evidence="Aprovado pelo usuario",
            confidence="confirmed",
            event_id="test-event-1"
        )

        jsonl_path = Path(self.project) / "memory/events.jsonl"
        json_path = Path(self.project) / "memory/events.json"
        sqlite_path = Path(self.project) / "memory/memory.sqlite"

        # Verifica presenca dos tres formatos
        self.assertTrue(jsonl_path.is_file(), "Arquivo events.jsonl deve existir")
        self.assertTrue(json_path.is_file(), "Arquivo events.json deve existir")
        self.assertTrue(sqlite_path.is_file(), "Arquivo memory.sqlite deve existir")

        # Verifica conteudo do JSON estruturado
        data_json = json.loads(json_path.read_text("utf-8"))
        self.assertEqual(1, len(data_json))
        self.assertEqual("test-event-1", data_json[0]["id"])
        self.assertEqual("decision", data_json[0]["kind"])

        # Verifica banco de dados SQLite
        rows = query_memory_sqlite(self.project, "SELECT id, kind, actor, content FROM events WHERE id = ?", ("test-event-1",))
        self.assertEqual(1, len(rows))
        self.assertEqual("test-event-1", rows[0]["id"])
        self.assertEqual("decision", rows[0]["kind"])
        self.assertEqual("orchestrator", rows[0]["actor"])

    def test_fallback_reading_from_json_and_sqlite(self):
        record_memory(
            self.project,
            action="Record",
            kind="checkpoint",
            actor="orchestrator",
            content="Checkpoint inicial",
            event_id="chk-1"
        )

        jsonl_path = Path(self.project) / "memory/events.jsonl"
        json_path = Path(self.project) / "memory/events.json"
        sqlite_path = Path(self.project) / "memory/memory.sqlite"

        # Apaga o JSONL e testa leitura via JSON
        jsonl_path.unlink()
        history_from_json = read_history(jsonl_path, json_path, sqlite_path)
        self.assertEqual(1, len(history_from_json))
        self.assertEqual("chk-1", history_from_json[0]["id"])

        # Apaga o JSON e testa leitura via SQLite
        json_path.unlink()
        history_from_sqlite = read_history(jsonl_path, json_path, sqlite_path)
        self.assertEqual(1, len(history_from_sqlite))
        self.assertEqual("chk-1", history_from_sqlite[0]["id"])


class TaskStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = self.temp.name

    def tearDown(self):
        self.temp.cleanup()

    def test_happy_path_requires_ack_and_contract_acceptance(self):
        create_task(self.project, "TASK-1", "API", "backend", "/root/backend", ["src/api"])
        transition_task(self.project, "TASK-1", "ready", "/root/backend")
        with self.assertRaisesRegex(AgentLibError, "ACK"):
            transition_task(self.project, "TASK-1", "running", "/root/backend")
        acknowledge_task(self.project, "TASK-1", "/root/backend")
        propose_contract(self.project, "TASK-1", "user-api", "v1", "/root/backend", "/root/frontend", "User[]")
        with self.assertRaisesRegex(AgentLibError, "Contratos sem aceite"):
            transition_task(self.project, "TASK-1", "running", "/root/backend")
        accept_contract(self.project, "TASK-1", "user-api", "v1", "/root/frontend")
        for state in ("running", "review", "done"):
            transition_task(self.project, "TASK-1", state, "/root/backend")
        self.assertEqual("done", read_task(self.project, "TASK-1")["state"])

    def test_descendant_path_conflicts_with_active_owner(self):
        create_task(self.project, "TASK-1", "API", "backend", "/root/backend", ["src/api"])
        with self.assertRaisesRegex(AgentLibError, "Conflito de ownership"):
            create_task(self.project, "TASK-2", "Users", "developer", "/root/developer", ["src/api/users.py"])

    def test_transfer_invalidates_ack(self):
        create_task(self.project, "TASK-1", "API", "backend", "/root/backend", ["src/api"])
        acknowledge_task(self.project, "TASK-1", "/root/backend")
        transfer_task(self.project, "TASK-1", "/root/backend", "developer", "/root/developer")
        task = read_task(self.project, "TASK-1")
        self.assertIsNone(task["ack"])
        self.assertEqual("/root/developer", task["owner"]["runtimeId"])

    def test_done_requires_completed_dependencies(self):
        create_task(self.project, "BASE", "Base", "developer", "/root/base", ["src/base"])
        create_task(self.project, "CHILD", "Child", "developer", "/root/child", ["src/child"], ["BASE"])
        for task_id, runtime in (("CHILD", "/root/child"), ("BASE", "/root/base")):
            acknowledge_task(self.project, task_id, runtime)
            for state in ("ready", "running", "review"):
                transition_task(self.project, task_id, state, runtime)
        with self.assertRaisesRegex(AgentLibError, "Dependencias pendentes"):
            transition_task(self.project, "CHILD", "done", "/root/child")
        transition_task(self.project, "BASE", "done", "/root/base")
        transition_task(self.project, "CHILD", "done", "/root/child")


if __name__ == "__main__":
    unittest.main()
