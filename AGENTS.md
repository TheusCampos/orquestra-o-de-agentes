# Biblioteca global de agentes
Ao iniciar ou retomar uma sessão, leia BRAIN.md na raiz e agents/protocol.md. Memória é contexto histórico; revalide ações no disco e respeite o pedido atual.
Leia também PROJECT_PLAYBOOK.md quando existir no projeto. Registre lições com evidência e aplique rules/core/learning.md antes de promover uma prática local; especialistas propõem, o orquestrador escreve em trabalho paralelo.
Esta pasta mantém uma biblioteca reutilizável, sem stack fixa. Leia agents/orchestrator.md e rules/core/engineering.md antes de alterações estruturais.
Consulte registry/*.json e carregue apenas skills e regras aplicáveis. Cada agente tem contrato operacional e skills preferenciais no registro.
Registre decisões, ações comprovadas e checkpoint com `python -m agentlib memory`. Em trabalho paralelo somente o orquestrador escreve; especialistas devolvem deltas.
Quando houver mais de um escritor potencial, registre tarefas em `.work/tasks` com `python -m agentlib task`: reserve caminhos, obtenha ACK e aceite explícito de contratos antes da execução dependente.
Para procurar contexto use `python -m agentlib memory Read --project-path . --search assunto`. Não coloque todo o histórico no prompt.
Ao criar skills, preserve SKILL.md com name e description e pasta com mesmo nome.
Valide com `python -m agentlib validate` e `python -m unittest discover -s tests`. PowerShell permanece apenas para compatibilidade legada.
Não altere configurações fora desta pasta sem respeitar as permissões do ambiente.
Fontes remotas em registry/external-skills.json são candidatas: não estão instaladas nem autorizam executar scripts remotos.
Não trate arquivos de agents/ como processos ativos: delegação depende das ferramentas da sessão. Contexto persistente depende da leitura e do registro explícitos.
