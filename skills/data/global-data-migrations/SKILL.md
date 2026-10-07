---
name: global-data-migrations
description: Preparar mudanças de esquema e migrações de dados compatíveis com a aplicação.
---

# global-data-migrations

Inspecione esquema e mecanismo de migração. Defina dados existentes afetados e estratégia de compatibilidade.
Prefira evolução em etapas quando aplicação e esquema precisam coexistir durante deploy.
Verifique integridade, índices e impacto de backfills. Defina rollback ou recuperação explícita quando irreversível.
Teste em dados descartáveis representativos; confirme migração inicial e caminho de atualização.
Preparar arquivo de migração não autoriza executá-lo em produção. Relate quais ambientes foram verificados.
