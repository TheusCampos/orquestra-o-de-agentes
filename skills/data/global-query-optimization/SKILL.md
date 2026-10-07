---
name: global-query-optimization
description: Investigar consultas lentas e propor índices ou mudanças de acesso a dados com evidência.
---

# global-query-optimization

Examine consulta real, parâmetros, volume representativo, índices e versão do banco.
Capture plano e baseline no ambiente autorizado. EXPLAIN ANALYZE executa a consulta; considere efeitos em escrita.
Identifique scans, cardinalidade, joins, N+1, locks ou excesso de transferência demonstrados.
Avalie índice e reescrita com custos de escrita, memória, armazenamento e manutenção.
Compare antes/depois com dados e parâmetros equivalentes. Preserve semântica e isolamento.
Não extrapole resultados de base vazia para produção. Registre o que ainda requer medição.
