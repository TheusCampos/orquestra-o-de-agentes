# Pesquisa de skills por especialidade — 2026-10-06
A biblioteca implementa procedimentos próprios. Os links abaixo são referências avaliadas na pesquisa e candidatas a importação; nenhum pacote remoto foi instalado.

| Área | Fonte primária | Aplicação e limite |
|---|---|---|
| Orquestração e arquitetura | [Superpowers](https://github.com/obra/superpowers) e [OpenAI Skills](https://github.com/openai/skills) | Planejamento, depuração e revisão; verificar regras do pacote antes de adoção. |
| Frontend e design | [Anthropic frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Referência para direção visual; manter escolhas do usuário e identidade existente. |
| React e Next.js | [Vercel react-best-practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices) | Otimização em stack compatível; medir problema real antes de aplicar. |
| Backend e segurança | [OpenAI security-threat-model](https://github.com/openai/skills/tree/main/skills/.curated/security-threat-model) | Modelagem de ameaças; não substitui verificação de controles. |
| Banco de dados | [Supabase Agent Skills](https://github.com/supabase/agent-skills) | Referência Postgres/Supabase; confirmar banco e recursos usados. |
| QA e navegador | [Anthropic webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) | Testes web; conferir dependências e ferramentas disponíveis. |
| Revisão e depuração | [Superpowers systematic-debugging](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) e [requesting-code-review](https://github.com/obra/superpowers/tree/main/skills/requesting-code-review) | Investigar causa e revisar evidência; adoção exige avaliação das prescrições do pacote. |
| Mobile | [Expo Skills](https://github.com/expo/skills) | Expo/EAS; outros frameworks usam documentação da própria stack. |
| Infraestrutura | [HashiCorp Agent Skills](https://github.com/hashicorp/agent-skills) | Terraform/Packer; planejar alterações e respeitar autorização para apply. |
| Desktop | [Tauri Security](https://v2.tauri.app/security/) | Documentação, não skill instalada. Consultar somente em projeto Tauri; a skill local cobre fronteiras nativas gerais. |
| Memória | Procedimento local global-persistent-memory | Arquivos por projeto, histórico verificável e recuperação explícita; não depende de framework externo. |

O catálogo estruturado está em registry/external-skills.json. A fonte lock registra repositórios, mantendo revisão e licença indefinidas enquanto não houver importação.
A pesquisa leu entradas SKILL.md de design, testes web, depuração, React e modelo de ameaças e os READMEs dos catálogos Supabase, Expo e HashiCorp. Isso não equivale a auditoria de todos os scripts.

## Importação futura
Selecionar skill concreta, confirmar licença, revisar conteúdo e scripts, identificar rede/escritas/dependências, fixar commit e hashes e testar em ambiente descartável.
As regras de um pacote não se tornam regras desta biblioteca só porque ele foi pesquisado. Requisitos do usuário e ambiente permanecem aplicáveis.
Não há garantia de skill externa adequada a todo domínio; lacunas são registradas e cobertas por procedimentos locais ou documentação oficial.
