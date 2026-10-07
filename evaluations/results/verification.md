# Verificação — 0.1.0

Data: 2026-10-06. Ambiente: Windows, Windows PowerShell 5.1 e codex-cli 0.160.1.

## Executado
- validate.ps1: 10 agentes, 11 skills, 8 regras e 7 perfis; referências, frontmatter, nomes, seleção de perfis e sintaxe PowerShell aprovados.
- test-integration.ps1: WhatIf sem escrita, instalação pelos wrappers, preservação de AGENTS.md e configuração pessoal, idempotência, edição fora do bloco, recusa de alteração gerenciada, colisão sem escrita parcial, recusa de troca de perfil, marcadores fora de ordem e confinamento de caminho.
- Atualização de uma cópia isolada da biblioteca de 0.1.0 para 0.1.1: regra alterada e versão sincronizadas, integridade confirmada.
- Instalação e doctor para todos os sete perfis.
- codex features list em CODEX_HOME isolado: execução local concluída; multi_agent disponível.
- codex debug prompt-input no projeto descartável: exportação concluída, instrução de orquestração e global-testing encontrados no contexto.

Comandos:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-integration.ps1
```

Artefatos da execução ampliada: .work/integration-a31b2862fabd4ebb96309046549bda42/
Diagnóstico de prompt: .work/prompt-diagnostic.json (não inclui uma resposta de modelo).

## Limites
Não houve chamada ao modelo nem execução dos cenários comportamentais de produto. Esses cenários estão preparados em evaluations/scenarios e permanecem pendentes.
A exportação de prompt verifica descoberta de instruções/skills; não prova a invocação de um custom agent. Confira os agentes disponíveis em nova sessão no cliente escolhido.
Nenhuma skill externa foi importada. Não houve instalação fora desta pasta.
O validador de skills usado foi o local em PowerShell; o quick_validate.py da skill de autoria não foi executado porque não foi localizado um Python funcional no ambiente.

