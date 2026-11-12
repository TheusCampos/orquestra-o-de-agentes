# Manual de Governança e Orquestração Multi-Agente (.agents)

Bem-vindo ao ecossistema multi-agente padronizado de alta performance. Este repositório utiliza uma arquitetura de **13 Agentes Especialistas**, clusters de **Sub-Agentes Auxiliares**, **Skills Progressivas**, **Guardrails de Qualidade** e regras formais de handoff, otimizado para o **Google Antigravity (AGY)** com compatibilidade transparente para **Cursor, Windsurf, VS Code (Cline/Roo/Copilot) e Claude Code**.

---

## 1. Topologia e Hierarquia Operacional

O ecossistema opera sob uma estrutura hierárquica coordenada pelo **Master Orchestrator**, precedida pelo **Prompt Analyzer & Clarifier**:

```
                              [ Usuário / Prompt ]
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │  0A. Prompt Analyzer          │
                       │      (@prompt-analyzer)       │
                       └───────────────┬───────────────┘
                                       │ (Prompt refinado / sem ambiguidades)
                                       ▼
                       ┌───────────────────────────────┐
                       │  0. Master Orchestrator       │
                       │     (@master-orchestrator)    │
                       └───────────────┬───────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         │                             │                             │
         ▼                             ▼                             ▼
┌──────────────────┐          ┌──────────────────┐          ┌──────────────────┐
│ 1. Codebase      │          │ 2. Spec Planner  │          │ 3. Git Guard     │
│    Scout         │          │    (@spec-planner)│         │    (@git-guard)  │
│    (@scout)      │          └──────────────────┘          └──────────────────┘
└──────────────────┘                   │                             │
         │                             │                             │
         └─────────────┬───────────────┴───────────────┬─────────────┘
                       │                               │
                       ▼                               ▼
       ┌───────────────────────────────┐ ┌───────────────────────────────┐
       │ 4. Frontend Specialist        │ │ 5. Backend Specialist         │
       │    (@frontend-specialist)     │ │    (@backend-specialist)      │
       │ ├─ sub-ui-builder             │ │ ├─ sub-api-designer           │
       │ ├─ sub-browser-tester         │ │ └─ sub-db-migrator            │
       │ ├─ sub-seo-optimizer          │ └───────────────────────────────┘
       │ ├─ sub-performance-optimizer  │               │
       │ ├─ sub-clean-ui-auditor       │               │
       │ └─ sub-a11y-enforcer          │               │
       └───────────────────────────────┘               │
                       │                               │
                       ├───────────────────────────────┤
                       │                               │
                       ▼                               ▼
       ┌───────────────────────────────┐ ┌───────────────────────────────┐
       │ 6. Fullstack Specialist       │ │ 7. Security Specialist        │
       │    (@fullstack-specialist)    │ │    (@security-specialist)     │
       │ ├─ sub-vertical-slice         │ │ ├─ sub-security-auditor       │
       │ └─ sub-schema-syncer          │ │ ├─ sub-secret-detector        │
       └───────────────────────────────┘ │ ├─ sub-threat-modeler         │
                       │                 │ └─ sub-compliance-guard       │
                       │                 └───────────────────────────────┘
                       │                               │
                       ▼                               ▼
       ┌───────────────────────────────┐ ┌───────────────────────────────┐
       │ 8. Deep Debugger (Bug Lead)   │ │ 9. QA & Test Runner           │
       │    (@deep-debugger)           │ │    (@qa-tester)               │
       │ ├─ sub-root-cause             │ └───────────────────────────────┘
       │ ├─ sub-repro-generator        │               │
       │ └─ sub-patch-verifier         │               ▼
       └───────────────────────────────┘ ┌───────────────────────────────┐
                                         │ 10. Code Reviewer             │
                                         │     (@code-reviewer)          │
                                         └───────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
  Agente de Avaliação Sob Demanda (Ativado apenas sob invocação explícita):
  ┌─────────────────────────────────────────────────────────────────────┐
  │ 11. Product Quality Evaluator (@product-quality)                    │
  │     ├─ sub-architecture-scorer  (Acoplamento, Coesão, Clean Code)   │
  │     ├─ sub-health-auditor       (Débito Técnico, Complexidade, Testes)│
  │     └─ sub-benchmark-reporter   (Scorecard 0-100, Radar de Qualidade)│
  └─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Catálogo de Agentes e Sub-Agentes

### 0A. `prompt-analyzer` (Analisador & Clarificador de Prompts)
- **Função**: Analisar cada solicitação recebida. Se o prompt for vago, ambíguo ou faltar entendimento de escopo/critérios, dispara perguntas objetivas ao usuário antes do início da execução.
- **Sub-Agentes Auxiliares**:
  - `sub-ambiguity-detector`: Identifica lacunas de requisitos e riscos de suposições incorretas.
  - `sub-interview-refiner`: Converte dúvidas em perguntas diretas de múltipla escolha ou cenários objetivos.
- **Skill Principal**: `prompt-analyzer`

### 0. `master-orchestrator` (Comandante & Coordenador Geral)
- **Função**: Decompor requisitos, rotear tarefas para especialistas, gerenciar dependências de execução (DAG), validar critérios de aceite e consolidar entregas.
- **Sub-capacidades**: Dispatcher de tarefas, monitor de SLA/progresso, consolidador de artefatos.
- **Skill Principal**: `master-orchestrator`

### 1. `codebase-scout` (Mapeador de Contexto & AST)
- **Função**: Escanear rapidamente repositórios legados e grandes sem estourar a janela de contexto. Localiza símbolos, dependências e pontos de impacto.
- **Saídas**: Mapas arquiteturais, árvores de dependência, resumos conceituais.
- **Skill Principal**: `codebase-scout`

### 2. `spec-planner` (Arquiteto de Requisitos & OpenSpec)
- **Função**: Converter intenções em especificações técnicas precisas (OpenSpec SDD), planos de implementação, checklists de tarefas e critérios de aceite.
- **Saídas**: `proposal.md`, `tasks.md`, `specs/`.
- **Skill Principal**: `spec-planner`

### 3. `git-guard` (Isolamento de Branches & Commits Semânticos)
- **Função**: Proteger a branch `main`/`master`, criar branches de feature/fix isoladas, organizar staging cirúrgico e formatar commits convencionais atômicos.
- **Saídas**: Branches limpas, commits convencionais (`feat:`, `fix:`, `refactor:`), PR diffs.
- **Skill Principal**: `git-guard`

### 4. `frontend-specialist` (Especialista de UI/UX & Web Client)
- **Função**: Interfaces modernas, design systems, CSS/Tailwind, micro-interações, acessibilidade, SEO, velocidade e Core Web Vitals.
- **Sub-Agentes Auxiliares**:
  - `sub-ui-builder`: Componentização limpa, tokens de design, layouts responsivos e animações fluidas.
  - `sub-browser-tester`: Validação visual via browser, screenshots, testes de regressão de layout.
  - `sub-seo-optimizer`: Meta tags, OpenGraph, JSON-LD Schema.org, hierarquia semântica de headings e sitemaps.
  - `sub-performance-optimizer`: Core Web Vitals (LCP, INP, CLS), lazy loading, bundle analysis e render budgets.
  - `sub-clean-ui-auditor`: Boas práticas de UI, separação de concerns, DRY e integridade visual.
  - `sub-a11y-enforcer`: Acessibilidade WCAG 2.1/2.2 AA/AAA, ARIA e navegação por teclado.
- **Skill Principal**: `frontend-specialist`

### 5. `backend-specialist` (Especialista de Serviços, APIs & Dados)
- **Função**: Arquitetura de APIs (REST, GraphQL, gRPC), regras de negócio, modelagem de banco de dados, migrations, auth (JWT/OAuth/Argon2) e caching.
- **Sub-Agentes Auxiliares**:
  - `sub-api-designer`: Contratos OpenAPI/Swagger, rotas, validações de schema e rate-limiting.
  - `sub-db-migrator`: Modelos relacionais e NoSQL, migrações seguras, queries performáticas e indexação.
- **Skill Principal**: `backend-specialist`

### 6. `fullstack-specialist` (Especialista em Integrações Ponta a Ponta)
- **Função**: Implementação de fatias verticais (*Vertical Slices*), sincronização de tipagem e contratos entre Front e Back, Server Actions, SSR/SSG.
- **Sub-Agentes Auxiliares**:
  - `sub-vertical-slice`: Construção do fluxo completo desde o banco até a interface em um único ciclo.
  - `sub-schema-syncer`: Compartilhamento de tipos (tRPC, Zod, TypeScript interfaces) e contratos unificados.
- **Skill Principal**: `fullstack-specialist`

### 7. `security-specialist` (Especialista em Segurança & Auditoria Contínua)
- **Função**: Análise estática de segurança (SAST), proteção contra ataques (OWASP Top 10), detecção de segredos/chaves vazadas e conformidade normativa.
- **Sub-Agentes Auxiliares**:
  - `sub-security-auditor`: Varredura de vulnerabilidades de código (SQLi, XSS, SSRF, IDOR).
  - `sub-secret-detector`: Identificação de tokens, chaves de API e credenciais hardcoded.
  - `sub-threat-modeler`: Modelagem de ameaças e superfícies de ataque em novos fluxos.
  - `sub-compliance-guard`: Headers de segurança (CSP, CORS, HSTS) e conformidade LGPD/GDPR.
- **Skill Principal**: `security-specialist`

### 8. `deep-debugger` (Líder de Investigação & Bug Agents)
- **Função**: Diagnóstico forense de falhas, análise de stack traces, isolamento da causa-raiz e emissão de patches atômicos.
- **Sub-Agentes de Bug**:
  - `sub-root-cause`: Análise forense de logs, isolamento de variáveis e hipótese de causa-raiz.
  - `sub-repro-generator`: Criação de script ou teste mínimo automatizado que reproduz a falha (teste vermelho).
  - `sub-patch-verifier`: Aplicação de patch cirúrgico e validação de que o teste de reprodução passa e a suíte não regrediu.
- **Skill Principal**: `deep-debugger`

### 9. `qa-tester` (Automação de Testes & Validação)
- **Função**: Testes unitários, de integração e ponta a ponta (E2E), cobertura de código, testes de carga e validação de casos de borda.
- **Saídas**: Relatórios de teste, matriz de cenários de borda.
- **Skill Principal**: `qa-tester`

### 10. `code-reviewer` (Auditor de Clean Code & Performance)
- **Função**: Checagem de padrões de código, tipagem estrita, boas práticas e checklist de aprovação para merge.
- **Saídas**: Review scorecard, aprovação formal para merge.
- **Skill Principal**: `code-reviewer`

### 11. `product-quality-evaluator` (Avaliador de Qualidade & Métricas - On-Demand)
- **Função**: Acionado **exclusivamente sob demanda** (quando chamado diretamente ou quando o usuário solicita uma nota/métrica do sistema).
- **Sub-Agentes Auxiliares**:
  - `sub-architecture-scorer`: Análise de acoplamento, modularidade e manutenibilidade.
  - `sub-health-auditor`: Métricas de débito técnico, complexidade e cobertura.
  - `sub-benchmark-reporter`: Geração do Scorecard de 0 a 100 e matriz de recomendações.
- **Skill Principal**: `product-quality-evaluator`

---

## 3. Protocolo de Despacho do Master (`Task Dispatch Contract - TDC`)

Quando o `@master-orchestrator` aciona qualquer especialista ou sub-agente, ele emite a instrução contendo o bloco contratual:

```markdown
### 📋 [TASK DISPATCH CONTRACT]
- **Task ID**: TASK-XXX
- **Target Agent**: @frontend-specialist | @backend-specialist | @fullstack-specialist | @security-specialist | @deep-debugger | @product-quality | etc.
- **Sub-Agent Helper**: sub-seo-optimizer | sub-performance-optimizer | sub-security-auditor | sub-root-cause | etc.
- **Objetivo**: Descrição clara da meta.
- **Arquivos no Escopo**:
  - `caminho/do/arquivo1.ts`
  - `caminho/do/arquivo2.tsx`
- **Restrições**: Regras inegociáveis (ex: manter compatibilidade, seguir design system).
- **Critérios de Aceite**:
  1. [ ] Critério 1
  2. [ ] Critério 2
- **Handoff Após Conclusão**: Próximo agente na esteira (ex: `@qa-tester`).
```

---

## 4. Estrutura de Diretórios do Ecossistema

```
.agents/
├── AGENTS.md                                # Este manual mestre
├── rules/                                   # Diretrizes e restrições ativas
│   ├── 00-git-workflow.md                   # Fluxo de Git e branches
│   ├── 01-codebase-scouting.md              # Estratégia de leitura de repositórios
│   ├── 02-agent-handoff-protocol.md         # Protocolo de comunicação entre agentes
│   ├── 03-frontend-standards.md             # Padrões de UI/UX, SEO, Web Vitals, A11y
│   ├── 04-backend-standards.md              # Padrões de APIs, DB, Auth e Performance
│   ├── 05-fullstack-integration.md          # Padrões de fatiamento vertical e contratos
│   ├── 06-bug-triage-and-patching.md        # Protocolo forense de resolução de bugs
│   ├── 07-quality-and-security.md           # Padrões de QA e revisão de código
│   ├── 08-security-and-threat-modeling.md   # Segurança SAST, segredos e conformidade
│   ├── 09-prompt-analysis-protocol.md       # Protocolo de clarificação de prompts
│   └── 10-product-quality-scoring.md        # Framework de métricas e notas 0-100 (On-Demand)
└── skills/                                  # Habilidades especializadas sob demanda
    ├── prompt-analyzer/SKILL.md
    ├── master-orchestrator/SKILL.md
    ├── codebase-scout/SKILL.md
    ├── spec-planner/SKILL.md
    ├── git-guard/SKILL.md
    ├── frontend-specialist/SKILL.md
    ├── backend-specialist/SKILL.md
    ├── fullstack-specialist/SKILL.md
    ├── security-specialist/SKILL.md
    ├── deep-debugger/SKILL.md
    ├── qa-tester/SKILL.md
    ├── code-reviewer/SKILL.md
    └── product-quality-evaluator/SKILL.md
```
