# data
Integridade, consultas e evolução de dados.

Use migrações versionadas e consistentes com a ferramenta adotada.
Avalie locks, volume e compatibilidade antes de alterar esquema.
Não faça backfill em produção sem plano e autorização aplicável.
Defina transações por unidade de negócio; evite depender de ordem implícita de consultas.
