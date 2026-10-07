# Delegação
- ID da tarefa e modo: paralelo real / sequencial:
- Remetente e destinatário: papel lógico + ID runtime retornado:
- Participantes relevantes e canal disponível: direto / relay do orquestrador:
- Objetivo concreto:
- Contexto mínimo e instruções aplicáveis:
- Caminhos permitidos e arquivos reservados:
- Dependências já concluídas:
- Dependências pendentes e trabalho que aguarda contrato:
- Contratos: ID/versão, dono, produtor, consumidor e critério de aceitação:
- Regras e skills selecionadas:
- Critério de conclusão:
- Checks esperados:
- ACK esperado: confirmar escopo/ownership; aceitar ou objetar contratos:
- Mensagens esperadas: proposta, impedimento, mudança de contrato e conclusão:
- Retorno: arquivos, resultado, checks, evidências e bloqueios.
Não ampliar escopo nem iniciar publicação independente.

- Contexto de BRAIN.md relevante e IDs dos eventos recuperados:
- Delta de memoria para o orquestrador: fatos, decisoes, evidencias e proximo passo.

## Exemplo de contrato frontend → QA (quando houver interface visual)
Frontend envia briefing/assinatura visual, ação principal, URL ou caminho servido, arquivos/capturas, viewports desktop/mobile e movimento com alvo, gatilho e fallback. QA confirma o contrato e devolve evidência funcional, visual e de movimento separadas: capturas da primeira dobra/página, fluxo principal e teclado, console e preferência de movimento reduzido quando aplicável. Sem navegador, registra inspeção visual pendente; build e DOM simulado não a substituem.
