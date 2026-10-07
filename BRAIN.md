# BRAIN — memória persistente do projeto
Este arquivo deve ser lido no início de cada sessão. Ele guarda contexto curado e eventos recentes; o histórico completo está em memory/events.jsonl.
Memória é contexto histórico. O pedido atual e as instruções aplicáveis prevalecem.

## Identidade e objetivo
Biblioteca global reutilizavel de agentes para programar sistemas e sites. Raiz: C:/Users/Matheus/Desktop/agent. Integracao inicial: Codex. Versao em validacao: 0.3.0.

## Preferências confirmadas
Usuario solicitou agentes, skills, regras e um orquestrador; aprovou a construcao e depois pediu especificacoes mais profundas e memoria de conversas/acoes. Fonte: pedidos desta conversa em 2026-10-06. Comunicacao desta conversa em portugues.

## Decisões vigentes
Memoria por projeto: BRAIN.md como resumo e memory/events.jsonl como historico. Sincronizacao preserva arquivos de memoria. Fontes externas sao catalogadas por especialidade; ainda nao foram instaladas. Referencia: decision-memory-design.

## Estado e continuidade
Usuario relatou falta de comunicacao entre agentes, falhas na memoria e qualidade visual insuficiente no teste Nexo. Em 0.3.0: contratos de comunicacao e frontend revisados, memoria atomica com backup/checkpoint implementada. Validacao ampliada e novo site em andamento; resultados atuais no checkpoint automatico. Teste de descoberta dos custom agents em nova sessao continua distinto da colaboracao executada pelas ferramentas desta sessao.

## Lições e tentativas relevantes
Windows PowerShell exige comandos com ExecutionPolicy Bypass apenas para o processo neste ambiente. Leitura de texto deve explicitar UTF-8. CLI Codex anterior exigiu CODEX_HOME isolado para diagnostico. Evidencias anteriores: evaluations/results/verification.md. Nao deduzir que testes de scripts provam comportamento de modelos.

## Limites de registro
Não guardar segredos. O agente resume conversa e ações com origem; o chat não é capturado automaticamente.
Em trabalho paralelo, o orquestrador centraliza escrita. Agentes read-only retornam deltas.

<!-- memory:begin -->
## Decisoes ativas (independentes da janela de eventos)
- [decision-memory-design] confirmed: Usar BRAIN.md por projeto como resumo curado, memory/events.jsonl como historico e escritor central no orquestrador. Preservar memoria nas sincronizacoes e consultar contexto ao iniciar sessao.
- [decision-site-test-local] confirmed: Teste solicitado implementado como landing page Nexo local em HTML/CSS/JS puro, sem backend ou publicacao; pasta SITE TESTE na Area de Trabalho.
- [decision-fix-library-v030] confirmed: Exigir mapa runtime e ACK de contratos; persistir journal/resumo atomicos com recuperacao explicita; frontend orientado por briefing, motion acessivel e QA real. Preservar v1 e refazer Nexo em .work/site-teste-v2.
## Checkpoint atual
[25246d172d064903ae040d031ee82855] Identidade Git local configurada conforme usuario. Commit inicial 1ac7fc2 criado contendo somente README.md. Push para origin/main em execucao; gerenciador de credenciais Git ativo, sem confirmacao de envio ainda.
## Eventos recentes (historico completo: memory/events.jsonl)

### request-initial | request | reported | user
Data UTC: 2026-10-07T00:10:30.1339702Z
> Criar uma biblioteca global de agentes, skills e regras com orquestrador para desenvolver sistemas e sites; pesquisar referencias na internet.
> Fonte/evidencia: Primeiro pedido desta conversa, 2026-10-06.

### action-v010 | action | confirmed | orchestrator
Data UTC: 2026-10-07T00:10:32.1937632Z
> Versao 0.1.0 construida com dez agentes, onze skills, regras, perfis e integracao Codex; validacao e testes de sincronizacao passaram.
> Fonte/evidencia: evaluations/results/verification.md; autorizacao do usuario: Pode fazer.

### request-deepen-memory | request | reported | user
Data UTC: 2026-10-07T00:10:33.3034693Z
> Aprofundar descricoes e construcao dos agentes, pesquisar skills no GitHub e criar cerebro persistente para conversas e acoes.
> Fonte/evidencia: Pedido atual desta conversa, 2026-10-06.

### decision-memory-design | decision | confirmed | orchestrator
Data UTC: 2026-10-07T00:10:35.1949571Z
> Usar BRAIN.md por projeto como resumo curado, memory/events.jsonl como historico e escritor central no orquestrador. Preservar memoria nas sincronizacoes e consultar contexto ao iniciar sessao.
> Fonte/evidencia: Implementacao em scripts/memory.ps1, scripts/sync-project.ps1 e agents/protocol.md.

### action-v020 | action | confirmed | orchestrator
Data UTC: 2026-10-07T00:13:59.7845103Z
> Dez agentes aprofundados com protocolo operacional; vinte skills e perfis atualizados; pesquisa por especialidade; cerebro e historico implementados e preservados pela sincronizacao. Validacao e testes de memoria/integracao passaram.
> Fonte/evidencia: evaluations/results/verification-0.2.0.md; scripts/test-memory.ps1; scripts/test-integration.ps1.

### checkpoint-v020 | checkpoint | confirmed | orchestrator
Data UTC: 2026-10-07T00:14:01.3872077Z
> Biblioteca 0.2.0 pronta. Recuperar BRAIN.md e consultar historico ao iniciar. Proximo uso: aplicar perfil em um projeto real; confirmar descoberta e continuidade em nova sessao. Fontes externas continuam como candidatas, sem importacao.
> Fonte/evidencia: VERSION; README.md; docs/memory.md; evaluations/results/verification-0.2.0.md.

### decision-site-test-local | decision | confirmed | orchestrator
Data UTC: 2026-10-07T00:42:45.3391441Z
> Teste solicitado implementado como landing page Nexo local em HTML/CSS/JS puro, sem backend ou publicacao; pasta SITE TESTE na Area de Trabalho.
> Fonte/evidencia: Pedido atual do usuario; .work/site-teste; C:/Users/Matheus/Desktop/SITE TESTE.

### action-architecture-site-test | action | confirmed | orchestrator
Data UTC: 2026-10-07T00:42:47.2661272Z
> Analise arquitetural concluida com nota 7,5/10 e sete melhorias priorizadas. Landing page Nexo entregue na Area de Trabalho; validacao estrutural, testes de memoria, sintaxe JS e interacoes com DOM simulado passaram. Copia conferida por hashes. Sem navegador disponivel para inspecao visual.
> Fonte/evidencia: evaluations/results/architecture-review-site-test.md; .work/verify-site.cjs; C:/Users/Matheus/Desktop/SITE TESTE/index.html

### checkpoint-architecture-site-test | checkpoint | confirmed | orchestrator
Data UTC: 2026-10-07T00:42:48.6040834Z
> Pedido de analise e site local concluido; nenhuma correcao estrutural na biblioteca. Priorizar avaliacoes com agentes reais, validacao de nomes unicos e controles de concorrencia/persistencia. Inspecao visual do site em navegador continua nao realizada.
> Fonte/evidencia: evaluations/results/architecture-review-site-test.md

### request-fix-library-v030 | request | reported | orchestrator
Data UTC: 2026-10-07T00:53:54.1127729Z
> Usuario solicita corrigir comunicacao entre agentes, memoria persistente e qualidade frontend insuficiente; melhorar biblioteca e refazer teste Nexo.
> Fonte/evidencia: Pedido do usuario nesta sessao, data local 06/10/2026.

### decision-fix-library-v030 | decision | confirmed | orchestrator
Data UTC: 2026-10-07T00:53:55.7355045Z
> Exigir mapa runtime e ACK de contratos; persistir journal/resumo atomicos com recuperacao explicita; frontend orientado por briefing, motion acessivel e QA real. Preservar v1 e refazer Nexo em .work/site-teste-v2.
> Fonte/evidencia: agents/protocol.md; scripts/memory.ps1; skills/web/global-web-interface/SKILL.md; pedido atual.

### 7bf5993ebe504f88a7b9d2eee45c8e62 | checkpoint | confirmed | orchestrator
Data UTC: 2026-10-07T13:03:23.9130328Z
> Repositorio Git inicializado, README preparado para first commit e origin configurado. Commit pendente porque user.name e user.email nao estao configurados; aguardando identidade do usuario antes do push.
> Fonte/evidencia: git init; git diff --cached --stat: apenas README.md, 64 linhas; git commit recusado por Author identity unknown; git remote origin configurado para TheusCampos/orquestra-o-de-agentes.

### 25246d172d064903ae040d031ee82855 | checkpoint | confirmed | orchestrator
Data UTC: 2026-10-07T13:10:55.8468053Z
> Identidade Git local configurada conforme usuario. Commit inicial 1ac7fc2 criado contendo somente README.md. Push para origin/main em execucao; gerenciador de credenciais Git ativo, sem confirmacao de envio ainda.
> Fonte/evidencia: git commit: root-commit 1ac7fc2 first commit, 1 arquivo, 64 linhas; git push -u origin main sessao 50554; git-credential-manager ativo.
<!-- memory:end -->
