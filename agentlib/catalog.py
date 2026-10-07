"""Carga e validacao do catalogo: registry/*.json, perfis, skills e agentes."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List

from .core import LIBRARY_ROOT, AgentLibError, assert_no_links, read_json, read_text, resolve_child

SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
AGENT_NAME = re.compile(r"^global-[a-z0-9-]+$")
PROFILE_NAME = re.compile(r"^[a-z][a-z0-9-]*$")
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
SANDBOXES = {"read-only", "workspace-write"}


def load_catalog(kind: str, root: Path = LIBRARY_ROOT) -> list:
    data = read_json(root / "registry" / f"{kind}.json")
    if not isinstance(data, list):
        raise AgentLibError(f"registry/{kind}.json deve ser uma lista.")
    return data


def load_profile(name: str, root: Path = LIBRARY_ROOT) -> dict:
    if not PROFILE_NAME.match(name or ""):
        raise AgentLibError(f"Perfil invalido: {name}")
    path = resolve_child(root, f"profiles/{name}.json")
    if not path.is_file():
        available = ", ".join(sorted(p.stem for p in (root / "profiles").glob("*.json")))
        raise AgentLibError(f"Perfil inexistente: {name}. Disponiveis: {available}")
    return read_json(path)


def select(catalog: list, ids: Iterable[str]) -> list:
    result = []
    for item_id in ids or []:
        found = [entry for entry in catalog if entry.get("id") == item_id]
        if len(found) != 1:
            raise AgentLibError(f"Referencia ausente ou duplicada: {item_id}")
        result.append(found[0])
    return result


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    body = match.group(1)
    result = {}
    name = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", body)
    description = re.search(r"(?m)^description:\s*(\S[^\r\n]*)$", body)
    if name:
        result["name"] = name.group(1)
    if description:
        result["description"] = description.group(1).strip()
    return result


def short_description(agent: dict) -> str:
    """Parte de missao da descricao (antes de 'Ativar:')."""
    return agent.get("description", "").split(" Ativar:")[0].strip()


def validate(root: Path = LIBRARY_ROOT) -> str:
    """Valida a biblioteca inteira. Junta todos os problemas antes de falhar."""
    errors: List[str] = []

    def check(condition: bool, message: str) -> bool:
        if not condition:
            errors.append(message)
        return condition

    try:
        agents = load_catalog("agents", root)
        skills = load_catalog("skills", root)
        rules = load_catalog("rules", root)
        external = load_catalog("external-skills", root)
    except (OSError, ValueError, AgentLibError) as exc:
        raise AgentLibError(f"Catalogo ilegivel: {exc}")

    for kind, catalog in (("agents", agents), ("skills", skills), ("rules", rules)):
        seen = set()
        for item in catalog:
            item_id = item.get("id")
            check(item_id not in seen, f"ID duplicado em {kind}: {item_id}")
            seen.add(item_id)
            try:
                path = resolve_child(root, item.get("path", ""))
                assert_no_links(path, stop_at=root)
                check(path.exists(), f"Referencia inexistente: {item.get('path')}")
            except AgentLibError as exc:
                errors.append(str(exc))
            check(bool(str(item.get("description", "")).strip()), f"Descricao ausente: {item_id}")

    names = set()
    for skill in skills:
        name = skill.get("name", "")
        check(bool(SKILL_NAME.match(name)) and len(name) < 64, f"Nome de skill invalido: {name}")
        check(name not in names, f"Nome de skill duplicado: {name}")
        names.add(name)
        check(Path(skill.get("path", "")).name == name, f"Pasta difere do nome: {name}")
        skill_file = root / skill.get("path", "") / "SKILL.md"
        if not check(skill_file.is_file(), f"SKILL.md ausente: {name}"):
            continue
        body = read_text(skill_file)
        front = parse_frontmatter(body)
        check(front.get("name") == name and bool(front.get("description")), f"Frontmatter invalido: {name}")
        check(len(front.get("description", "")) <= 1024, f"Descricao da skill acima de 1024 caracteres: {name}")
        check(not re.search(r"\bTODO\b|\[TODO\]|INSERT_HERE", body), f"Scaffold incompleto: {name}")

    registered = {str(Path(s.get("path", ""))).replace("\\", "/") for s in skills}
    on_disk = {str(p.parent.relative_to(root)).replace("\\", "/") for p in (root / "skills").rglob("SKILL.md")}
    for missing in sorted(on_disk - registered):
        errors.append(f"Skill no disco sem registro em registry/skills.json: {missing}")
    for missing in sorted(registered - on_disk):
        errors.append(f"Skill registrada sem SKILL.md no disco: {missing}")

    agent_names = set()
    for agent in agents:
        for label, catalog, ids in (("skill", skills, agent.get("preferredSkills")),
                                    ("referencia externa", external, agent.get("externalReferences"))):
            try:
                select(catalog, ids)
            except AgentLibError as exc:
                errors.append(f"Agente {agent.get('id')}: {label} {exc}")
        protocol = root / agent.get("protocol", "")
        check(protocol.is_file(), f"Protocolo ausente: {agent.get('id')}")
        name = agent.get("name", "")
        check(bool(AGENT_NAME.match(name)), f"Nome de agente invalido: {name}")
        check(name not in agent_names, f"Nome de agente duplicado: {name}")
        agent_names.add(name)
        check(agent.get("sandbox") in SANDBOXES, f"Sandbox invalido: {agent.get('id')}")
        agent_file = root / agent.get("path", "")
        if agent_file.is_file():
            text = read_text(agent_file)
            check(f"Nome nativo: {name}" in text, f"{agent.get('path')} sem linha 'Nome nativo: {name}'")
            check("'''" not in text, f"{agent.get('path')} contem ''' (incompativel com TOML)")
    if (root / "agents/protocol.md").is_file():
        check("'''" not in read_text(root / "agents/protocol.md"), "protocol.md contem ''' (incompativel com TOML)")

    profiles = sorted((root / "profiles").glob("*.json"))
    for profile_file in profiles:
        try:
            profile = read_json(profile_file)
        except ValueError as exc:
            errors.append(f"Perfil JSON invalido {profile_file.name}: {exc}")
            continue
        pid = profile.get("id")
        check(profile.get("schemaVersion") == 1 and pid == profile_file.stem, f"Perfil invalido: {profile_file.name}")
        for catalog, ids in ((agents, profile.get("agents", [])), (skills, profile.get("skills", [])),
                             (rules, list(profile.get("rules", [])) + list(profile.get("conditionalRules", [])))):
            check(len(set(ids)) == len(ids), f"Selecao duplicada: {pid}")
            try:
                select(catalog, ids)
            except AgentLibError as exc:
                errors.append(f"Perfil {pid}: {exc}")
        try:
            for role in select(agents, profile.get("agents", [])):
                for skill_id in role.get("preferredSkills", []):
                    check(skill_id in profile.get("skills", []), f"Perfil {pid} sem skill do agente {role['id']}: {skill_id}")
        except AgentLibError:
            pass
        check("global-persistent-memory" in profile.get("skills", []), f"Perfil sem memoria: {pid}")
        check("orchestrator" in profile.get("agents", []), f"Perfil sem orquestrador: {pid}")
        check(int(profile.get("maxConcurrentSpecialists", 0)) >= 1, f"Concorrencia invalida: {pid}")

    sources = read_json(root / "registry/sources.lock.json")
    for source in sources.get("sources", []):
        check(source.get("status") == "catalog-only", f"Fonte externa promovida sem validador de importacao: {source.get('id')}")
    check(not sources.get("installedExternalSkills"), "Importacoes externas ainda nao suportadas pelo validador.")

    # Texto corrompido (U+FFFD) costuma vir de arquivo salvo em ANSI e lido como UTF-8.
    for folder in ("agents", "skills", "rules", "workflows", "templates"):
        for md in (root / folder).rglob("*.md"):
            try:
                if "\ufffd" in read_text(md):
                    errors.append(f"Caractere corrompido (U+FFFD) em {md.relative_to(root)}; salve como UTF-8.")
            except UnicodeDecodeError:
                errors.append(f"Arquivo nao e UTF-8: {md.relative_to(root)}")

    if errors:
        raise AgentLibError("Validacao falhou:\n- " + "\n- ".join(errors))
    return f"OK: {len(agents)} agentes, {len(skills)} skills, {len(rules)} regras, {len(profiles)} perfis."
