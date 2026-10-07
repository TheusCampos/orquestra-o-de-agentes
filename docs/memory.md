# Cérebro e memória persistente
BRAIN.md é o ponto de recuperação de contexto de cada projeto. As seções curadas preservam objetivo, preferências, decisões e estado. O bloco automático mostra os últimos eventos.
memory/events.jsonl é o histórico completo, com ID, data UTC, ator, tipo, confiança, evidência e substituição opcional.
Não há dependência de serviço, embeddings ou banco de dados nesta versão. O arquivo acompanha o projeto; uma conversa só entra quando o agente a resume e registra.

## Uso
Na fonte execute scripts/memory.ps1; no projeto instalado execute .agent-library/scripts/memory.ps1.
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\memory.ps1 -Action Read -ProjectPath .
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\memory.ps1 -Action Record -ProjectPath . -Kind decision -Actor orchestrator -Content "Usar a stack existente." -Confidence reported -Evidence "Pedido do usuário"
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\memory.ps1 -Action Read -ProjectPath . -Search "stack"
```
Para checkpoint, registre tarefa, evidência, pendência e próximo passo. Para correção, use -Kind correction -Supersedes ID-do-evento.
Um ID repetido com conteúdo idêntico é idempotente; conteúdo diferente com mesmo ID é rejeitado.
Record atualiza somente o bloco automático; texto curado externo é preservado. O bloco fixa decisões ativas e o último checkpoint além dos 20 eventos recentes. Read retorna também decisions e checkpoint independentemente de Search/Limit; eventos consultados continuam filtrados.
Sincronização inicializa BRAIN.md apenas quando ausente. Memória não entra nos hashes de arquivos gerenciados, portanto mudanças nela não bloqueiam atualização da biblioteca.

## Integridade e concorrência
Uma trava exclusiva serializa operações do script. Durante trabalho paralelo, somente o orquestrador registra.
O journal é gravado em temporário no mesmo diretório, descarregado em disco e substituído atomicamente antes do resumo. BRAIN.md recebe o mesmo tratamento e mantém a versão anterior em memory/BRAIN.previous.md. Uma interrupção entre journal e resumo deixa eventos recuperáveis em Read; Init ou Record recompõe o bloco. A regravação do journal é linear no tamanho do histórico; para históricos muito grandes, medir antes de mudar o armazenamento.
Read toma uma trava compartilhada quando o arquivo de lock existe; escritores têm trava exclusiva. Leitura concorrente com escrita falha explicitamente para permitir nova tentativa, sem combinar versões.
Se o resumo estiver danificado, preserve uma cópia e execute `memory.ps1 -Action Recover -ProjectPath .`. A operação lê o backup, valida o journal e recompõe eventos atuais sem substituir o backup bom pelo arquivo danificado. Recupera a última versão salva do texto curado; edições manuais posteriores podem exigir recuperação manual. Sem backup válido ou com journal inválido, a operação falha preservando os dados.
Registro parcial ou JSON inválido é rejeitado, sem ignorar silenciosamente evidência corrompida. Faça cópia antes de reparar manualmente.
Para mudanças manuais do resumo, não edite simultaneamente com Record.
Correção mantém original no histórico e indica Supersedes; no bloco recente o original é rotulado como substituído.
Nas projeções, effectiveKind herda o tipo do evento original através da cadeia de correções: decisões e checkpoints corrigidos permanecem nas seções fixas. O journal preserva kind=correction; não grava campos derivados da consulta.
Se BRAIN.md contém eventos mas o journal está ausente ou vazio, Read/Init/Record/Recover falham sem descartar o resumo. Restaurar o histórico exige uma cópia válida; não reconstruir fatos como confirmados a partir de texto sem evidência.
O script não detecta todos os segredos: agentes devem excluir dados sensíveis antes de registrar.
Trava reduz conflito entre processos que usam o script; não protege contra editores externos.

## Continuidade entre sessões
AGENTS.md instrui leitura de BRAIN.md. O protocolo compartilhado exige recuperação e delta de memória.
Especialistas recebem contexto necessário na delegação e devolvem alterações propostas ao orquestrador.
Sem acesso aos arquivos ou se a ferramenta não carregar as instruções, não existe garantia de lembrança.
Dados antigos continuam sujeitos a confirmação. Não deduza autorização de deploy ou acesso a serviço externo a partir de evento histórico.

Busca retorna tambem correcoes dos eventos encontrados, mesmo se o texto novo nao contiver o termo pesquisado. effectiveState e supersededBy indicam substituicoes. Mantenha decisoes vigentes nas secoes curadas com seus IDs. Versione resumo/historico conforme pratica do projeto; exclua memory/.writer.lock do Git.
