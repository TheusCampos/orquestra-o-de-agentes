---
name: codebase-scout
description: Especialista em reconhecimento ultra-rápido de código e mapeamento arquitetural. Varre projetos de grande porte e legados, extrai rotas, modelos, dependências e padrões sem consumir contexto excessivo.
---

# Codebase Scout Skill

Esta skill capacita o agente a realizar reconhecimento e indexação acelerada de projetos.

---

## 1. Procedimento de Mapeamento
1. **Inspeção de Manifestos e Configurações**:
   - Localizar arquivos como `package.json`, `tsconfig.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`.
   - Identificar dependências principais (frameworks, ORMs, bibliotecas de UI, test runners).
2. **Varredura Estrutural com Filtros Cirúrgicos**:
   - Listar diretórios raiz e subpastas chave (`src/`, `app/`, `pages/`, `server/`, `lib/`, `tests/`).
   - Evitar ler diretórios pesados como `node_modules/`, `dist/`, `.git/`, `build/`, `vendor/`.
3. **Mapeamento de Símbolos e Pontos de Inserção**:
   - Utilizar busca por padrões (`grep_search`) para localizar onde funções, rotas e componentes correlatos à tarefa estão declarados.
4. **Emissão do Mapa de Contexto**:
   - Entregar ao Master Orchestrator o resumo enxuto contendo os caminhos exatos dos arquivos relevantes e seus relacionamentos.
