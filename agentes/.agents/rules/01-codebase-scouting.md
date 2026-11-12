# Regra 01: Estratégia de Reconhecimento Rápido de Codebase (Scouting)

Esta regra orienta a exploração inteligente e econômica de projetos legados e de grande porte sem saturação de contexto.

---

## 1. Princípios do Reconhecimento Eficiente
1. **Nunca ler arquivos inteiros às cegas**: Utilize primeiro listagens de diretórios, árvores de arquivos e buscas pontuais por padrões (`grep_search`).
2. **Identificar o Ponto de Entrada (Entrypoints)**:
   - Web/Fullstack: `package.json`, `src/App.tsx`, `src/main.ts`, `pages/`, `app/`.
   - Backend/APIs: `server.ts`, `main.py`, `app.py`, `Cargo.toml`, `go.mod`.
   - Banco de Dados: `prisma/schema.prisma`, `drizzle.config.ts`, `migrations/`, `models/`.
3. **Mapeamento Top-Down**:
   - Nível 1: Entender a arquitetura geral (Monolito, Microserviços, Monorepo, Clean Arch).
   - Nível 2: Mapear módulos e rotas principais.
   - Nível 3: Inspecionar cirurgicamente apenas os arquivos afetados pela tarefa.

---

## 2. Padrão de Artefato: Mapa Arquitetural (`ARCHITECTURE_MAP.md`)
Quando o `codebase-scout` for acionado para indexar um repositório, ele deve produzir ou atualizar o mapa estruturado contendo:

```markdown
# Mapa Arquitetural do Projeto

## 1. Stack Tecnológica
- **Linguagem**: [TypeScript | Python | Go | etc.]
- **Framework Web**: [Next.js | Express | FastAPI | etc.]
- **Persistência**: [PostgreSQL | MongoDB | Prisma | etc.]
- **Testes**: [Vitest | Jest | Pytest | Playwright]

## 2. Estrutura de Diretórios Chave
- `/src/components`: Componentes visuais e design system.
- `/src/server/api`: Rotas e controllers.
- `/src/services`: Regras de negócio e integrações.
- `/src/db`: Schemas, migrations e repositórios de dados.

## 3. Padrões de Código e Convenções Identificadas
- Gerenciamento de estado via [Zustand | Redux | Context API].
- Autenticação implementada via [JWT em Cookies HttpOnly | NextAuth].
- Validações de entrada via [Zod | Yup | Pydantic].
```

---

## 3. Diretrizes de Preservação de Contexto
- Faça buscas direcionadas com regex ou texto exato antes de abrir arquivos grandes.
- Limite a visualização de linhas aos trechos relevantes (`StartLine` e `EndLine`).
- Ao passar o bastão para os construtores (`frontend`, `backend`, `fullstack`), entregue apenas as referências exatas dos arquivos e contratos que precisam ser alterados.
