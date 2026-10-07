---
name: global-task-planning
description: Dividir solicitações de desenvolvimento com múltiplas etapas ou dependências em tarefas verificáveis.
---

# global-task-planning

Defina critérios observáveis do pedido e identifique dependências antes de escolher especialistas.
Cada tarefa contém id, objetivo, entradas, saídas, caminhos permitidos, dependências, responsável e validação; use templates/task.md e templates/handoff.md quando precisar de persistência.
Use um grafo acíclico de dependências. Paralelize apenas tarefas independentes com escopos de escrita separados.
Descubra as ferramentas reais de delegação e comunicação e confira autorização antes de planejar execução paralela. Mapeie papel lógico ao ID runtime retornado; nomes em agents/ e registry/ não iniciam agentes. Sem ferramentas, execute os papéis sequencialmente e registre esse modo.
Reserve um escritor por caminho. Cada tarefa confirma escopo e dependências com ACK. Transfira ownership explicitamente antes de reatribuir trabalho.
Planeje integração dos contratos e checks finais. Para dependências entre especialistas, indique produtor, consumidor, dono do contrato, versão aceita e evidência de aceitação. Use mensagens diretas com IDs runtime quando disponíveis; caso contrário, o orquestrador faz relay. Envio sem resposta não aceita contrato.
Registre estado em .work/tasks quando a duração exigir retomada. Tarefas pequenas dispensam documentação formal.
Não confunda terminar uma subtarefa com concluir o pedido inteiro.
