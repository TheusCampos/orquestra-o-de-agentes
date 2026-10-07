# Integração Codex
Referências consultadas em 2026-10-06:
- [AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [Skills](https://developers.openai.com/codex/skills)
- [Subagentes](https://developers.openai.com/codex/multi-agent)

O adaptador gera .codex/agents/global-*.toml com name, description e developer_instructions.
Reviewer, architect e security têm sandbox read-only; outros usam workspace-write. Modelos e reasoning são herdados.
Não altera permissões globais nem cria regras permissivas de shell.
Skills vão para .agents/skills/global-*; instruções do agente principal são referenciadas por bloco no AGENTS.md.
Config nova usa [agents] enabled=true e max_concurrent_threads_per_session=3. Config existente é preservada; se agentes estiverem desativados, ative manualmente na configuração escolhida.
Não substitui built-ins. Custom agents dependem da versão do cliente e da descoberta de configuração.
Execute doctor.ps1 e, após abrir uma nova sessão no projeto, peça ao Codex para listar instruções, skills e custom agents disponíveis. Diagnóstico de arquivos não prova carregamento em sessão real.
