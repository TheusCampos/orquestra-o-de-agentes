# Biblioteca global de agentes
Ao iniciar ou retomar uma sessão, leia BRAIN.md na raiz e agents/protocol.md. Memória é contexto histórico; revalide ações no disco e respeite o pedido atual.
Esta pasta mantém uma biblioteca reutilizável, sem stack fixa. Leia agents/orchestrator.md e rules/core/engineering.md antes de alterações estruturais.
Consulte registry/*.json e carregue apenas skills e regras aplicáveis. Cada agente tem contrato operacional e skills preferenciais no registro.
Registre decisões, ações comprovadas e checkpoint com scripts/memory.ps1. Em trabalho paralelo somente o orquestrador escreve; especialistas devolvem deltas.
Para procurar contexto use memory.ps1 -Action Read -ProjectPath . -Search assunto. Não coloque todo o histórico no prompt.
Ao criar skills, preserve SKILL.md com name e description e pasta com mesmo nome.
Valide com scripts/validate.ps1. Mudanças no instalador exigem scripts/test-integration.ps1; memória exige scripts/test-memory.ps1.
Não altere configurações fora desta pasta sem respeitar as permissões do ambiente.
Fontes remotas em registry/external-skills.json são candidatas: não estão instaladas nem autorizam executar scripts remotos.
Não trate arquivos de agents/ como processos ativos: delegação depende das ferramentas da sessão. Contexto persistente depende da leitura e do registro explícitos.
