# Revisão das rules e aprendizado por projeto

## Diagnóstico

As rules de `engineering`, `quality` e `permissions` eram curtas, mas repetiam partes do protocolo; foram reduzidas a princípios que valem para qualquer tarefa. `web` misturava direção visual, teste no navegador e detalhes de framework; ficou restrita a invariantes da experiência web. As rules de API, dados, Python e TypeScript já são específicas e compactas. A rule LGPD contém afirmações legais e técnicas prescritivas; deve receber uma revisão jurídica/técnica própria antes de ser alterada ou aplicada como checklist universal.

## Rules adicionadas

| Rule | Onde entra | Motivo |
| --- | --- | --- |
| `learning` | Todos os perfis | Mantém aprendizado local com evidência, promoção e correção de práticas. |
| `operability` | API e fullstack | Exige diagnóstico e recuperação para mudanças em serviços, jobs e releases. |

## Ciclo de melhoria

1. Especialistas retornam observação, evidência, efeito e ajuste proposto quando houver lição relevante.
2. O orquestrador registra fatos e correções no journal do projeto (`memory/events.jsonl`) e mantém o checkpoint em `BRAIN.md`.
3. Hipóteses ficam em **Candidatas a verificar** em `PROJECT_PLAYBOOK.md`. Uma prática entra em **Práticas ativas** quando determinada pelo usuário ou apoiada por repetição verificável neste projeto.
4. Cada prática ativa registra quando aplicar, fonte, data e condição de revisão. Se contradita, o orquestrador a retira, preserva o motivo e registra uma correção na memória.
5. Na próxima sessão, o orquestrador lê o playbook e revalida a prática antes de usá-la.

`PROJECT_PLAYBOOK.md` é criado apenas na primeira sincronização e pertence ao projeto; o `sync` não o sobrescreve nem o inclui no manifesto gerenciado. Essa melhoria depende da leitura e da escrita explícitas do agente em cada sessão. Não há treinamento de modelo, observador em segundo plano ou alteração automática da biblioteca global.

## Próximas melhorias recomendadas

- Medir, em avaliações com sessões reais, se os agentes retornam deltas úteis e se o orquestrador corrige práticas obsoletas; validação de arquivos não prova esse comportamento.
- Revisar a rule LGPD com fonte normativa atual e orientação jurídica do contexto do produto, mantendo-a condicional ao tratamento real de dados pessoais.
- Quando houver projetos suficientes, comparar práticas locais recorrentes antes de propor uma rule global; exigir evidência de mais de um projeto e revisão humana da mudança de escopo.
