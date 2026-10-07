"""Sincronizacao de projetos com a biblioteca global de agentes.

Substitui o script sync-project.ps1, oferecendo sincronizacao segura
em qualquer sistema operacional com Python 3.9+.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Optional, Tuple

from .core import (
    LIBRARY_ROOT, AgentLibError, assert_no_links, byte_hash, dump_json,
    file_hash, read_json, read_text, resolve_child, text_hash, write_atomic
)
from .catalog import load_profile, load_catalog, select, validate

def _add_source(desired: Dict[str, str], relative: str) -> None:
    path = LIBRARY_ROOT / relative
    if path.is_file():
        desired[f".agent-library/{relative}"] = read_text(path)

def sync_project(project_path: str, profile_name: str = "general") -> Tuple[int, str]:
    """Sincroniza um projeto com o perfil escolhido da biblioteca.
    
    Retorna uma tupla (numero_arquivos_alterados, mensagem).
    """
    validate()
    target = Path(project_path).resolve()
    assert_no_links(target)
    if target.is_file():
        raise AgentLibError("Destino e um arquivo.")

    profile_data = load_profile(profile_name)
    all_agents = load_catalog("agents")
    all_skills = load_catalog("skills")
    all_rules = load_catalog("rules")

    agents = select(all_agents, profile_data.get("agents", []))
    skills = select(all_skills, profile_data.get("skills", []))
    rules = select(all_rules, list(profile_data.get("rules", [])) + list(profile_data.get("conditionalRules", [])))

    manifest_path = resolve_child(target, ".agent-library/manifest.json")
    assert_no_links(manifest_path)
    
    previous = None
    old_hashes = {}
    if manifest_path.is_file():
        previous = read_json(manifest_path)
        if previous.get("schemaVersion") != 1:
            raise AgentLibError("Manifesto incompativel.")
        if previous.get("profile") != profile_name:
            raise AgentLibError("Troca de perfil exige instalacao em destino novo nesta versao.")
        for entry in previous.get("files", []):
            rel_path = entry.get("path")
            resolve_child(target, rel_path)
            if rel_path in old_hashes:
                raise AgentLibError("Manifesto contem caminhos duplicados.")
            old_hashes[rel_path] = entry.get("hash")

    desired: Dict[str, str] = {}
    
    protocol = read_text(LIBRARY_ROOT / "agents/protocol.md")
    _add_source(desired, "agents/protocol.md")
    
    # Scripts legacy, se existirem (para retrocompatibilidade parcial, se ainda estiverem migrando)
    for script_name in ["common.ps1", "memory.ps1"]:
        if (LIBRARY_ROOT / "scripts" / script_name).is_file():
            _add_source(desired, f"scripts/{script_name}")
            
    # Arquivos core Python
    for py_module in ["core.py", "catalog.py", "memory.py", "sync.py"]:
        if (LIBRARY_ROOT / "agentlib" / py_module).is_file():
            _add_source(desired, f"agentlib/{py_module}")

    for agent in agents:
        agent_path = agent.get("path", "")
        _add_source(desired, agent_path)
        body = read_text(resolve_child(LIBRARY_ROOT, agent_path))
        instructions = f"{protocol}\n{body}\nLeia .agent-library/profiles/active.json e as regras/skills pertinentes ao escopo. Respeite instrucoes locais e limites da sessao."
        
        # Emulando Convert-ToTomlLiteral (simplificado)
        def toml_literal(s):
            return json.dumps(s) if s else '""'
            
        import json
        toml_content = [
            f"name = {toml_literal(agent.get('name'))}",
            f"description = {toml_literal(agent.get('description'))}",
            f"sandbox_mode = {toml_literal(agent.get('sandbox'))}",
            f"developer_instructions = {toml_literal(instructions)}\n"
        ]
        desired[f".codex/agents/{agent.get('name')}.toml"] = "\n".join(toml_content)

    for skill in skills:
        folder = resolve_child(LIBRARY_ROOT, skill.get("path", ""))
        for root_dir, _, files in os.walk(folder):
            for file in files:
                file_path = Path(root_dir) / file
                assert_no_links(file_path)
                relative = file_path.relative_to(folder).as_posix()
                content = read_text(file_path)
                desired[f".agents/skills/{skill.get('name')}/{relative}"] = content
                desired[f".agent-library/{skill.get('path')}/{relative}"] = content

    for rule in rules:
        _add_source(desired, rule.get("path", ""))
        
    for folder_name in ["workflows", "templates"]:
        folder_path = LIBRARY_ROOT / folder_name
        if folder_path.is_dir():
            for file_path in folder_path.iterdir():
                if file_path.is_file():
                    _add_source(desired, f"{folder_name}/{file_path.name}")

    desired[".agent-library/profiles/active.json"] = dump_json(profile_data)
    desired[".agent-library/registry/agents.json"] = dump_json(agents)
    desired[".agent-library/registry/skills.json"] = dump_json(skills)
    desired[".agent-library/registry/rules.json"] = dump_json(rules)
    
    for f in ["registry/sources.lock.json", "registry/external-skills.json", "VERSION"]:
        _add_source(desired, f)

    config_relative = ".codex/config.toml"
    config_path = resolve_child(target, config_relative)
    if not config_path.exists() or config_relative in old_hashes:
        template_path = LIBRARY_ROOT / "adapters/codex/templates/config.toml"
        if template_path.is_file():
            desired[config_relative] = read_text(template_path)

    for old in old_hashes:
        if old not in desired:
            raise AgentLibError(f"Componente antigo ausente na nova versao: {old}. Remocao requer reconciliacao manual.")

    for relative in desired:
        path = resolve_child(target, relative)
        assert_no_links(path)
        if path.is_dir():
            raise AgentLibError(f"Destino de arquivo e pasta: {relative}")
        if path.is_file():
            current_hash = file_hash(path)
            if relative in old_hashes:
                if current_hash != old_hashes[relative]:
                    raise AgentLibError(f"Arquivo gerenciado alterado localmente: {relative}")
            elif current_hash != text_hash(desired[relative]):
                raise AgentLibError(f"Colisao com arquivo nao gerenciado: {relative}")

    begin_marker = "<!-- agent-library:begin -->"
    end_marker = "<!-- agent-library:end -->"
    block_lines = [
        begin_marker,
        "# Desenvolvimento com a biblioteca global",
        "Atue como orquestrador seguindo .agent-library/agents/orchestrator.md.",
        "No inicio de cada sessao, leia BRAIN.md na raiz do projeto; recupere historico usando agentlib/memory.py quando necessario.",
        "Registre decisoes, acoes comprovadas e checkpoint via memory.py. Em paralelo, somente o orquestrador escreve; especialistas retornam deltas.",
        "Leia .agent-library/profiles/active.json e PROJECT_CONTEXT.md do projeto quando existir.",
        "Regras essenciais: .agent-library/rules/core/engineering.md, .agent-library/rules/core/quality.md e .agent-library/rules/execution/permissions.md.",
        "Consulte .agent-library/registry para selecionar apenas skills e regras aplicaveis.",
        "Delegue explicitamente partes independentes de tarefas complexas aos especialistas global-* disponiveis; sem ferramentas de subagentes, execute os papeis sequencialmente.",
        "Respeite instrucoes locais mais especificas, autorizacao do usuario e limites efetivos da sessao.",
        end_marker
    ]
    block = "\n".join(block_lines)

    agents_path = resolve_child(target, "AGENTS.md")
    assert_no_links(agents_path)
    if agents_path.is_dir():
        raise AgentLibError("AGENTS.md e uma pasta.")
    
    existing = read_text(agents_path) if agents_path.is_file() else ""
    begin_count = existing.count(begin_marker)
    end_count = existing.count(end_marker)
    
    if begin_count != end_count or begin_count > 1:
        raise AgentLibError("Marcadores invalidos em AGENTS.md.")
        
    import re
    match = re.search(f"(?s){re.escape(begin_marker)}.*?{re.escape(end_marker)}", existing)
    if begin_count == 1 and not match:
        raise AgentLibError("Ordem dos marcadores invalida.")
        
    if match:
        if not previous:
            raise AgentLibError("Bloco de biblioteca sem manifesto; reconciliar antes de instalar.")
        if text_hash(match.group(0)) != previous.get("agentsBlockHash"):
            raise AgentLibError("Bloco gerenciado de AGENTS.md alterado localmente.")
        new_agents = existing[:match.start()] + block + existing[match.end():]
    else:
        if previous:
            raise AgentLibError("Bloco gerenciado removido de AGENTS.md.")
        separator = "\n\n" if existing and not existing.endswith("\n") else ("\n" if existing else "")
        new_agents = existing + separator + block + "\n"

    hashes = [{"path": k, "hash": text_hash(v)} for k, v in desired.items()]
    
    version_text = ""
    version_file = LIBRARY_ROOT / "VERSION"
    if version_file.is_file():
        version_text = read_text(version_file).strip()
        
    manifest = {
        "schemaVersion": 1,
        "libraryVersion": version_text,
        "profile": profile_name,
        "files": hashes,
        "agentsBlockHash": text_hash(block)
    }

    brain_path = resolve_child(target, "BRAIN.md")
    assert_no_links(brain_path)
    if brain_path.is_dir():
        raise AgentLibError("BRAIN.md e uma pasta.")
        
    if not brain_path.exists():
        template_brain = LIBRARY_ROOT / "templates/brain.md"
        if template_brain.is_file():
            desired["BRAIN.md"] = read_text(template_brain)

    desired["AGENTS.md"] = new_agents
    desired[".agent-library/manifest.json"] = dump_json(manifest)

    changed = []
    for relative, content in desired.items():
        p = resolve_child(target, relative)
        if not p.is_file() or file_hash(p) != text_hash(content):
            changed.append(relative)

    if not changed:
        return 0, f"Sem alteracoes: {target} ({profile_name})."

    originals = {}
    written = []
    try:
        for relative in changed:
            path = resolve_child(target, relative)
            originals[relative] = path.read_bytes() if path.is_file() else None
            path.parent.mkdir(parents=True, exist_ok=True)
            written.append(relative)
            path.write_text(desired[relative], encoding="utf-8")
    except Exception as failure:
        for relative in written:
            path = resolve_child(target, relative)
            if originals[relative] is not None:
                path.write_bytes(originals[relative])
            elif path.is_file():
                path.unlink()
        raise failure

    return len(changed), f"Sincronizado: {target}; perfil={profile_name}; arquivos alterados={len(changed)}.\nAbra nova sessao no projeto para conferir descoberta. Configuracao preexistente foi preservada."

if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description="Sincronizar projeto com biblioteca")
    parser.add_argument("project_path", help="Caminho do projeto")
    parser.add_argument("--profile", default="general", help="Perfil a sincronizar")
    args = parser.parse_args()
    
    try:
        count, msg = sync_project(args.project_path, args.profile)
        print(msg)
    except AgentLibError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
