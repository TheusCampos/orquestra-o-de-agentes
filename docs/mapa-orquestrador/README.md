# Mapa do orquestrador e dos agentes

Data da análise: 12 de novembro de 2026. Escopo: biblioteca `orquestra-o-de-agentes` no estado local atual.

## Conclusão rápida

Este repositório é uma **biblioteca declarativa de orquestração**, não um serviço que deixa dez agentes rodando em segundo plano. Os arquivos em `agents/` definem papéis e contratos; os agentes só existem em uma sessão quando o Codex (ou outro runtime compatível) encontra os arquivos sincronizados e oferece ferramentas de delegação.

O papel principal é `global-orchestrator`. Ele lê contexto e memória, escolhe um perfil, roteia o trabalho, reserva os caminhos de escrita, integra resultados e registra a continuidade. Para tarefas pequenas, ele próprio implementa. Para trabalho transversal, pode abrir até **três especialistas simultâneos**, se o runtime permitir; sem essa capacidade, executa os papéis em sequência.

Abra o [mapa mental animado](mapa-interativo.html) para explorar as conexões entre orquestrador, subagentes, skills, rules e perfis. O [painel completo](dashboard.html) mostra prompts, fontes, memória e alterações locais. Para renovar o snapshot após modificar a biblioteca, execute `python docs/mapa-orquestrador/build-dashboard-data.py`. Veja também [o mapa Mermaid](mapa-mental.md) e [os fluxos](fluxos.md).

## O que está definido x o que está em execução

| Camada | Estado observado | Significado |
| --- | --- | --- |
| Catálogo | 13 papéis, 29 skills da biblioteca, 11 regras e 7 perfis; `python -m agentlib validate` passou. | A biblioteca está estruturalmente consistente. |
| Orquestrador | Definido em `agents/orchestrator.md`. | É uma instrução/papel; não é daemon nem scheduler próprio. |
| Especialistas | Definidos em `agents/*.md`; `architect`, `reviewer` e `security` são read-only. | Só viram agentes runtime após descoberta pelo cliente e delegação explícita. |
| Paralelismo | Limite configurado de 3 especialistas por perfil e no template Codex. | É um teto, não a garantia de três agentes ativos. |
| Tarefas ativas | Não há diretório `.work/` nesta raiz. | Não há evidência de tarefas/ownership persistentes em andamento aqui. |
| Memória | `BRAIN.md` e `memory/events.{jsonl,json,sqlite}` existem. | Há histórico do projeto; o orquestrador deve revalidá-lo no disco antes de agir. |

Importante: a presença de um arquivo em `agents/` ou de um registro JSON **não prova** que um subagente foi criado numa sessão. O próprio protocolo exige mapear o ID runtime real, tarefa, estado e caminhos reservados antes de chamar isso de colaboração paralela.

## Papéis e quando entram

| Papel | Quando usar | Permissão | Responsabilidade na prática |
| --- | --- | --- | --- |
| `orchestrator` | Todo pedido de desenvolvimento. | escrita | Descoberta, contrato de entrega, roteamento, integração e memória. |
| `ceo` | Estratégia e prioridades entre equipes. | somente leitura | Compara opções e define critérios de sucesso sem assumir decisões do usuário. |
| `product-manager` | Requisitos amplos, jornada e escopo. | somente leitura | Converte objetivo em critérios e ordem de entrega. |
| `designer` | Novo produto, identidade, redesign ou protótipo. | somente leitura | Define experiência e especificações visuais para implementação. |
| `architect` | Nova arquitetura, módulos integrados, decisão incompatível ou requisito operacional. | somente leitura | Define limites, decisões e contratos antes da implementação. |
| `developer` | Feature geral, correção, automação ou refatoração. | escrita | Implementa mudanças funcionais gerais. |
| `frontend` | Página, componente, formulário, navegação, acessibilidade ou performance de renderização. | escrita | Implementa e verifica a interface. |
| `backend` | API, autenticação, integração, job, transação ou domínio de servidor. | escrita | Implementa serviço e contrato compatível com consumidores. |
| `data` | Modelagem, migração, consultas, integridade, backfill ou concorrência no banco. | escrita | Evolui persistência com segurança. |
| `qa` | Fluxo integrado, regressão, funcionalidade ou teste instável. | escrita | Produz evidência reproduzível dos critérios de aceitação. |
| `reviewer` | Revisão pedida, contrato alterado ou risco relevante após integração. | somente leitura | Encontra defeitos materiais com evidência. |
| `security` | Mudança em autenticação, permissão, entrada, segredo ou dado sensível. | somente leitura | Avalia fronteiras de confiança e propõe mitigação. |
| `devops` | CI/CD, build, ambiente, infraestrutura, release ou incidente operacional autorizado. | escrita | Prepara e diagnostica operação e entrega. |

## Como o perfil seleciona os agentes

O perfil é a composição instalada por `python -m agentlib sync <projeto> --profile <nome>`. Ele não obriga o uso de todos os papéis: disponibiliza a equipe e as skills candidatas; o orquestrador seleciona apenas o necessário.

| Perfil | Equipe disponível | Uso típico |
| --- | --- | --- |
| `general` | orquestrador, CEO, Product Manager, developer, reviewer, qa | Projeto indefinido ou desenvolvimento geral. |
| `website` | orquestrador, CEO, Product Manager, Designer, frontend, developer, reviewer, qa | Site e interface web. |
| `fullstack` | orquestrador, CEO, Product Manager, Designer, architect, frontend, backend, data, reviewer, qa, security, devops | Aplicação com UI, serviços, dados e operação. |
| `api` | orquestrador, Product Manager, backend, data, reviewer, qa, security | API e serviços. |
| `automation` | orquestrador, Product Manager, developer, reviewer, qa | Automação. |
| `mobile` | orquestrador, CEO, Product Manager, Designer, architect, developer, reviewer, qa | Aplicação mobile. |
| `desktop` | orquestrador, CEO, Product Manager, Designer, architect, developer, reviewer, qa | Aplicação desktop. |

Observação: o perfil `fullstack` não inclui `developer`; a implementação é especializada em frontend/backend/data. Nos demais perfis, essa escolha é mais enxuta.

## O caminho até um projeto consumidor

`agentlib sync` transforma a biblioteca em uma instalação por projeto:

1. Lê o perfil e seleciona agentes, skills e regras nos registros.
2. Copia o protocolo e contratos para `.agent-library/`.
3. Gera um TOML por papel em `.codex/agents/global-*.toml`.
4. Copia skills selecionadas para `.agents/skills/` e também para `.agent-library/`.
5. Insere um bloco gerenciado em `AGENTS.md`, preservando o texto externo.
6. Inicializa `BRAIN.md` somente se ele ainda não existir e grava um manifesto de hashes.

O adaptador prevê `agents.enabled = true` e `max_concurrent_threads_per_session = 3`, mas uma nova sessão ainda precisa confirmar que o cliente realmente descobriu essa configuração. A sincronização também recusa colisões e arquivos gerenciados editados localmente.

## Como a colaboração deveria acontecer

1. O orquestrador lê `AGENTS.md`, `BRAIN.md`, checkpoint, perfil e estado real do projeto.
2. Traduz o pedido em critérios de aceitação e consulta registros para escolher papéis e skills.
3. Para cada subtarefa paralela, cria uma tarefa em `.work/tasks/<id>.json`, com um único dono por caminho de escrita.
4. O agente destinatário confirma ACK, escopo, dependências e ownership.
5. Para fronteiras compartilhadas, o produtor propõe um contrato versionado; o consumidor precisa aceitá-lo explicitamente antes da execução dependente.
6. Especialistas devolvem resultado, evidência, riscos e delta de memória. O orquestrador integra, revisa o diff, executa as verificações adequadas e registra decisões/checkpoint.

Os comandos `python -m agentlib task create|ack|transition|transfer|propose-contract|accept-contract` são a camada que materializa essa disciplina. A CLI bloqueia ownership concorrente, transições inválidas e execução sem ACK.

## Pontos de atenção encontrados

- Há uma divergência de versão histórica: `README.md` descreve a versão 0.4.0, enquanto o `BRAIN.md` ainda traz referências anteriores a 0.3.0. O protocolo já prevê que memória é contexto histórico e precisa ser revalidada; aqui isso é especialmente relevante.

- O repositório tem alterações locais pré-existentes (modificados e não rastreados). Esta análise não as alterou; os novos artefatos estão isolados em `docs/mapa-orquestrador/`.

- O catálogo validou com sucesso, mas esta análise não abriu uma sessão de um projeto consumidor para provar a descoberta runtime dos custom agents. Essa confirmação depende do cliente e da configuração efetivamente carregada.

## Evidências consultadas

- `AGENTS.md`, `BRAIN.md`, `agents/protocol.md` e `agents/orchestrator.md`.
- `registry/agents.json`, `registry/skills.json` e `profiles/*.json`.
- `agentlib/sync.py`, `agentlib/tasks.py`, `agentlib/memory.py` e `agentlib/__main__.py`.
- `adapters/codex/README.md` e `adapters/codex/templates/config.toml`.
- Verificação executada: `python -m agentlib validate` → `OK: 13 agentes, 29 skills, 11 regras, 7 perfis.` Consulte também [o roteamento das skills](../skill-routing.md) e [a revisão das rules](../rules-review.md).
