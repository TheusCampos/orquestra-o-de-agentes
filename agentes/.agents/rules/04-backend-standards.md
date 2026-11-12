# Regra 04: Padrões de Backend, APIs, Banco de Dados e Segurança

Esta regra governa o trabalho do **`@backend-specialist`** e seus sub-agentes auxiliares (`sub-api-designer`, `sub-db-migrator`).

---

## 1. Arquitetura de APIs e Serviços
1. **Design de Rotas e Recursos (RESTful / RPC)**:
   - Utilizar substantivos no plural para recursos (`/api/v1/users`, `/api/v1/products`).
   - Códigos de status HTTP semânticos:
     - `200 OK`: Sucesso com retorno de dados.
     - `201 Created`: Recurso criado com sucesso.
     - `204 No Content`: Operação concluída sem payload de retorno.
     - `400 Bad Request`: Erro de validação de payload/parâmetros.
     - `401 Unauthorized`: Autenticação ausente ou inválida.
     - `403 Forbidden`: Autenticado, mas sem permissão de acesso.
     - `404 Not Found`: Recurso inexistente.
     - `422 Unprocessable Entity`: Erro de regra de negócio.
     - `500 Internal Server Error`: Falha inesperada tratada.
2. **Validação Estrita de Entrada**:
   - Todo payload, query param e route param deve ser validado via schema (Zod, Pydantic, Joi, Class-Validator).
   - Sanitização de strings para prevenção de Injeção SQL e XSS.

---

## 2. Padrões de Banco de Dados e Persistência
1. **Modelagem e Migrations**:
   - Nomes de tabelas e colunas consistentes (`snake_case` para SQL).
   - Criação obrigatória de índices em chaves estrangeiras (`foreign keys`) e campos de busca frequente.
   - Toda alteração estrutural no banco de dados deve ser versionada através de arquivos de migração reversíveis.
2. **Segurança e Criptografia**:
   - Hash de senhas exclusivamente com algoritmos robustos com salting automático (Argon2id ou Bcrypt com fator de custo >= 12).
   - Armazenamento de segredos via variáveis de ambiente (`.env`), nunca hardcoded no código.

---

## 3. Diretrizes para os Sub-Agentes de Backend
- **`sub-api-designer`**:
  - Modela endpoints, gera especificações OpenAPI/Swagger, aplica rate-limiting e middlewares de autenticação/autorização.
- **`sub-db-migrator`**:
  - Escreve queries otimizadas, previne problemas de *N+1 queries*, configura transações atômicas para operações compostas e gerencia migrações seguras.
