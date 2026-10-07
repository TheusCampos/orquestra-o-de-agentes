# Biblioteca global de agentes — 0.3.0
Base reutilizável para desenvolver sistemas e sites com Codex. Agentes e skills em português, sem stack obrigatória.
A fonte central fica nesta pasta; cada projeto recebe uma instalação por perfil.

## Começar
Abra PowerShell nesta pasta. Os comandos usam uma política válida só para o processo, sem alterar a política global:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -ProjectPath .\exemplos\meu-site -Profile website
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\doctor.ps1 -ProjectPath .\exemplos\meu-site
```
Abra uma nova sessão Codex na pasta do projeto e peça:
> Examine o projeto, use o orquestrador da biblioteca e implemente o pedido. Delegue as partes independentes quando houver suporte, integre e valide.

## Perfis
general, website, fullstack, api, automation, mobile e desktop.
Mobile e desktop usam especialistas gerais com skills locais para ciclo de vida, integração nativa e limites de verificação.

## Sincronizar
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync-project.ps1 -ProjectPath .\exemplos\meu-site -Profile website -WhatIf
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync-project.ps1 -ProjectPath .\exemplos\meu-site -Profile website
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-integration.ps1
```
WhatIf faz planejamento sem escrever. Sincronização recusa arquivos gerenciados alterados localmente e colisões antes de escrever.
Mantenha personalizações no conteúdo externo ao bloco do AGENTS.md, PROJECT_CONTEXT.md ou instruções locais específicas.
Esta versão recusa troca de perfil no mesmo destino; use uma instalação nova para outro perfil. Não remove componentes silenciosamente.
Destinos devem ser pastas normais, sem links/junctions no caminho gerenciado. Permissões do ambiente continuam aplicáveis.
Não há instalação automática em ~/.codex ou ~/.agents. Para reutilizar em outro projeto, execute install/sync no destino autorizado.

## Organização
- agents/: contratos aprofundados de dez papéis e protocolo compartilhado.
- BRAIN.md e memory/events.jsonl: contexto curado e histórico persistente do projeto.
- skills/: vinte procedimentos próprios em SKILL.md.
- rules/: regras gerais, de tecnologia e de execução.
- profiles/ e registry/: composição e catálogos JSON.
- workflows/ e templates/: etapas e estado de trabalho.
- scripts/: validação, instalação, sincronização, diagnóstico e teste.
- docs/: arquitetura, fontes e roadmap.
- evaluations/: cenários e evidências; testes comportamentais precisam de sessão real.

## Fontes externas e compatibilidade
Links pesquisados estão em docs/skill-sources.md; nenhuma skill remota é executada ou instalada automaticamente.
O adaptador segue a [documentação de subagentes Codex](https://developers.openai.com/codex/multi-agent) e de [skills](https://developers.openai.com/codex/skills).
A existência dos arquivos não prova que o cliente os carregou. Execute doctor e confira em uma nova sessão.

Não execute duas sincronizações simultâneas no mesmo destino. O rollback restaura arquivos se houver falha de escrita; pode deixar diretórios vazios. Interrupção abrupta do processo exige conferir integridade com doctor.

## Memória entre sessões
Leia [BRAIN.md](BRAIN.md) ao iniciar. O orquestrador resume pedidos, decisões, ações e checkpoints; especialistas retornam deltas.
A sincronização inicializa o cérebro de cada projeto quando ausente e preserva a memória existente.
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\memory.ps1 -Action Read -ProjectPath .
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-memory.ps1
```
No projeto instalado, o script fica em .agent-library/scripts/memory.ps1.
Veja [protocolo de memória](docs/memory.md), [fontes por especialidade](docs/skill-sources.md) e [verificação da versão](evaluations/results/verification-0.3.0.md).
O arquivo é durável, mas nenhuma ferramenta pode lembrar conteúdo que não foi registrado ou que não consegue ler.

## Correções da versão 0.3.0
Comunicação usa IDs runtime reais, ACK, ownership e contratos aceitos; sem ferramentas disponíveis, o orquestrador faz relay ou executa os papéis sequencialmente. Evidência de uma troca real: [collaboration-0.3.0.md](evaluations/results/collaboration-0.3.0.md).
Memória grava journal e resumo atomicamente, mantém backup do resumo e fixa decisões/checkpoint além da janela recente. `memory.ps1 -Action Recover` recupera resumo danificado de um backup válido; não corrige histórico inválido silenciosamente.
Frontend inclui direção visual, arte, movimento acessível e matriz de inspeção real desktop/mobile. Assets e referências da skill seguem na instalação; novos projetos usam o perfil website como antes. Atualize instalações existentes com sync-project, respeitando personalizações e permissões do destino.
# orquestra-o-de-agentes
