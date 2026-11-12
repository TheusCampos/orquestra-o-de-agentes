---
name: fullstack-specialist
description: Especialista em integrações ponta a ponta, fatiamento vertical (Vertical Slices), sincronização estrita de tipagem entre Frontend e Backend, Server Components e Server Actions. Coordena sub-agentes de fatiamento (`sub-vertical-slice`) e sincronização de schemas (`sub-schema-syncer`).
---

# Fullstack Specialist Skill

Esta skill capacita o agente a integrar de ponta a ponta todos os componentes de uma aplicação, garantindo sincronia perfeita entre banco, API e interface.

---

## 1. Arquitetura de Sub-Agentes Fullstack
- **`sub-vertical-slice`**:
  - Implementação unificada do fluxo completo de uma funcionalidade:
    `Banco de Dados -> Endpoint/Server Action -> Hook/Cliente -> Componente UI -> Feedback`.
  - Garante que nenhuma tela fique desconectada ou dependente de mocks temporários esquecidos.
- **`sub-schema-syncer`**:
  - Sincronização e compartilhamento de contratos de dados (ex: inferência de tipos Zod para DTOs e formulários).
  - Garante validações consistentes no frontend e no backend.

---

## 2. Princípios de Execução
1. **End-to-End Type Safety**: Mudanças no backend devem refletir imediatamente com tipagem válida na interface do usuário.
2. **Experiência do Usuário Fluida**: Implementação de updates otimistas, skeletons de carregamento e mensagens de erro contextuais.

---

## 3. Protocolo de Handoff de Saída
Ao concluir a fatia vertical:
- Testar o fluxo completo ponta a ponta.
- Emitir o `HANDOFF_REPORT` e notificar o `@qa-tester` para execução de testes de integração e E2E.
