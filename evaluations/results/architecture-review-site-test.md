# Análise arquitetural e teste de landing page

Data local: 06/10/2026. Biblioteca 0.2.0. Nota: **7,5/10**.

## Parecer

A arquitetura é uma biblioteca declarativa de engenharia: dez papéis, vinte skills, oito regras e sete perfis. A documentação distingue corretamente instruções persistentes de processos ativos; o orquestrador depende das ferramentas da sessão. É uma boa base reutilizável, mas ainda não constitui um runtime que imponha todos os contratos descritos.

Pontos fortes: protocolo comum; gatilhos por especialidade; memória por projeto com evidência e correções; revisão e segurança read-only no registro; catálogo externo sem execução automática; sincronização com hashes, preservação de personalizações e detecção prévia de conflitos.

## Melhorias prioritárias

1. **Executar avaliações comportamentais.** `evaluations/results/verification-0.2.0.md` declara ausência de chamadas ao modelo e invocação comprovada dos custom agents. Os cenários devem produzir evidências reproduzíveis: aceitação, retorno dos agentes, falhas, intervenções, duração e custo. Começar por website, API, conflicting-writes e memory-continuity.
2. **Verificar propriedade e estado das tarefas.** `templates/task.md` e `global-task-planning` descrevem escopo, mas não há controlador de reservas de arquivos. Registrar proprietário, dependências e transições; conferir alterações contra escopo na integração. Usar worktrees quando escritas paralelas justificarem isolamento.
3. **Tornar a memória resistente a interrupções.** `scripts/memory.ps1` sobrescreve BRAIN.md diretamente; a leitura não toma a trava do escritor. O journal ajuda a reconstruir eventos, mas não necessariamente o texto curado. Escrever temporário, substituir atomicamente, manter backup e testar interrupções. Risco inferido do código, sem reprodução de queda nesta revisão.
4. **Proteger sincronização concorrente e recuperação.** `scripts/sync-project.ps1` tem rollback para exceções no mesmo processo, com originais em memória. Não há trava por destino nem recuperação durável após encerramento forçado. Adicionar lock, staging, journal e commit do manifesto ao final; testar falha parcial e dois instaladores simultâneos.
5. **Permitir evolução controlada dos perfis.** O sync recusa troca de perfil e remoção de componentes antigos. Implementar migração com preview, hashes e preservação de personalizações, permitindo website → fullstack sem reinstalar em outro projeto.
6. **Unificar configuração de concorrência.** `maxConcurrentSpecialists` nos perfis, três especialistas no orquestrador e `max_concurrent_threads_per_session = 3` no template são fontes separadas. Gerar configuração de uma fonte e ajustar ao limite efetivo da sessão, após verificar a semântica do adaptador.
7. **Aprofundar validação dos registros.** O validador verifica unicidade de IDs, mas não de `agent.name`; nomes repetidos podem gerar a mesma chave de TOML no plano de sync. Adicionar unicidade de nomes, schemas completos e fixtures negativas.

Prioridade de implementação: avaliações + nomes únicos; depois concorrência e persistência; por último migração de perfis. Aumentar a quantidade de agentes não resolve essas lacunas.

## Teste executado

Landing page demonstrativa Nexo criada em `C:/Users/Matheus/Desktop/SITE TESTE`, com index.html, styles.css, script.js e README.md. HTML/CSS/JS puro, sem instalação, build ou chamadas externas. Layout com breakpoints mobile/desktop, menu, três cenários e briefing em modal. Formulário e cenários são locais; não enviam mensagens nem executam IA.

Verificações nesta sessão:

- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate.ps1`: passou, 10 agentes / 20 skills / 8 regras / 7 perfis.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/test-memory.ps1`: passou; artefatos em `.work/memory-18e21cc2d9c34e64a69eb664f1f74fe7`.
- `node --check .work/site-teste/script.js`: passou.
- `node .work/verify-site.cjs`: passou; assets, IDs, âncoras, breakpoints declarados, movimento reduzido, menu/Escape, cenários, modal, briefing e reset verificados com DOM simulado.
- Destino criado e arquivos listados após cópia autorizada fora do workspace.

## Limites

Não houve inspeção visual nem teste de layout, teclado ou acessibilidade em navegador real: o inventário de superfícies retornou browsers vazio. Testes com DOM simulado não substituem esses checks.

Um subagente foi utilizado para revisão arquitetural read-only, conforme autorização de delegação do orquestrador. Essa execução não prova descoberta/invocação dos TOMLs de custom agents gerados pelo instalador. O teste demonstra uma entrega concreta nesta sessão, não o desempenho integral dos sete perfis. Testes de integração do instalador não foram repetidos; o instalador não foi alterado.

Nenhuma correção estrutural foi aplicada à biblioteca; o pedido era análise e criação do site. Próxima ação recomendada: abrir a landing page em navegador e executar os cenários de avaliação em sessões novas.
