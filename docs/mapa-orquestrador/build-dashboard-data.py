"""Gera os dados locais consumidos por index.html.

Execute na raiz da biblioteca ou nesta pasta sempre que agentes, skills, rules,
perfis, memória ou estado Git forem alterados:
    python docs/mapa-orquestrador/build-dashboard-data.py
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_json(path: Path):
    return json.loads(read_text(path))


def read_optional(path: Path) -> str:
    return read_text(path) if path.is_file() else ""


def git_changes() -> list[dict[str, str]]:
    try:
        output = subprocess.run(
            ["git", "status", "--short"], cwd=ROOT, text=True,
            encoding="utf-8", capture_output=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    return [
        {"status": line[:2].strip() or "?", "path": line[3:]}
        for line in output.splitlines() if line.strip()
    ]


def memory_events() -> list[dict]:
    journal = ROOT / "memory" / "events.jsonl"
    if not journal.is_file():
        return []
    events = []
    for line in read_text(journal).splitlines():
        if line.strip():
            try:
                event = json.loads(line)
                events.append({key: event.get(key, "") for key in ("id", "timestampUtc", "actor", "kind", "content", "confidence")})
            except json.JSONDecodeError:
                continue
    return events[-12:][::-1]


def workspace_skills() -> list[dict]:
    """Skills do ambiente do usuário: exibidas, mas não copiadas para a biblioteca."""
    folder = ROOT.parent / ".agents" / "skills"
    if not folder.is_dir():
        return []
    result = []
    for skill_file in sorted(folder.glob("*/SKILL.md")):
        text = read_optional(skill_file)
        name = skill_file.parent.name
        description = "Skill local do ambiente."
        for line in text.splitlines()[:20]:
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip()
            elif line.startswith("description:"):
                description = line.split(":", 1)[1].strip()
        result.append({
            "id": f"workspace:{name}", "name": name, "description": description,
            "path": str(skill_file.relative_to(ROOT.parent)).replace("\\", "/"),
            "origin": "workspace", "version": "ambiente", "source": text,
        })
    return result


def main() -> None:
    protocol = read_text(ROOT / "agents" / "protocol.md")
    agents = []
    for item in read_json(ROOT / "registry" / "agents.json"):
        role_source = read_text(ROOT / item["path"])
        agents.append({
            **item,
            "roleSource": role_source,
            "runtimePrompt": f"{protocol}\n\n{role_source}\n\nLeia .agent-library/profiles/active.json e as regras/skills pertinentes ao escopo. Respeite instruções locais e limites da sessão.",
        })

    skills = []
    for item in read_json(ROOT / "registry" / "skills.json"):
        folder = ROOT / item["path"]
        source = folder / "SKILL.md"
        if not source.is_file():
            source = folder / "README.md"
        skills.append({**item, "source": read_optional(source)})

    rules = []
    for item in read_json(ROOT / "registry" / "rules.json"):
        rules.append({**item, "source": read_optional(ROOT / item["path"])})

    profiles = [read_json(path) for path in sorted((ROOT / "profiles").glob("*.json"))]
    data = {
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": read_optional(ROOT / "VERSION").strip(),
        "agents": agents,
        "skills": skills,
        "workspaceSkills": workspace_skills(),
        "rules": rules,
        "profiles": profiles,
        "skillRouting": read_json(ROOT / "registry" / "workspace-skill-routing.json"),
        "changes": git_changes(),
        "events": memory_events(),
    }
    target = HERE / "dashboard-data.js"
    target.write_text("window.ORCHESTRATOR_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    print(f"Dados atualizados: {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
