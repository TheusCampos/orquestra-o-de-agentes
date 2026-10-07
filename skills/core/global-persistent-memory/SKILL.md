---
name: global-persistent-memory
description: Recuperar contexto, registrar decisões e checkpoints e corrigir memórias em BRAIN.md e no histórico do projeto.
---

# global-persistent-memory

No início da sessão, leia BRAIN.md da raiz do projeto. Se faltar, inicialize com o script memory.ps1 da biblioteca (na instalação: .agent-library/scripts/memory.ps1).
Consulte eventos recentes e procure assunto específico com -Action Read -Search. Read retorna checkpoint e decisões ativas fora da janela Limit; use o checkpoint para recuperar pendências, mesmo quando eventos posteriores o afastaram dos últimos 20 registros.
Revalide no disco ações e comandos antigos antes de usá-los. Pedido atual prevalece sobre memória; evidência histórica não concede autorização.
Durante trabalho paralelo, somente o orquestrador escreve. Especialistas retornam delta de memória com fonte e próximo passo.
Use -Action Record com Kind request, decision, action, checkpoint ou correction. Separe confidence reported, confirmed e hypothesis. Action confirmed exige Evidence.
Cada registro tem ID único. Correção usa Supersedes apontando evento existente; não apague o original.
Registre resumos úteis de conversas, decisões e ações, sem segredos e sem prometer transcrição automática.
BRAIN.md contém contexto curado fora do bloco automático e os últimos eventos dentro dele. Eventos completos ficam em memory/events.jsonl.
Ao terminar ou interromper, registre o que foi executado, o que continua pendente e a próxima ação. A memória só funciona nas sessões que leem esses arquivos.

O bloco automático fixa decisões não substituídas e o checkpoint atual, além dos eventos recentes. Seções curadas são contexto manual e podem estar desatualizadas: confronte seus IDs com effectiveState e supersededBy. A busca inclui correções mesmo quando seu texto não contém o termo original.
O script usa trava de leitura/escrita e substituição atômica. Se BRAIN.md perder os marcadores, preserve os arquivos e use -Action Recover para restaurar o backup memory/BRAIN.previous.md e recompor o bloco a partir do journal atual. Recover não repara JSON inválido nem captura chat ausente; nesses casos, registre o limite concreto.
