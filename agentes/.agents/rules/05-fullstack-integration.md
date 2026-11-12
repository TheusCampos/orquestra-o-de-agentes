# Regra 05: Integração Fullstack, Fatiamento Vertical e Sincronização de Contratos

Esta regra governa o trabalho do **`@fullstack-specialist`** e seus sub-agentes auxiliares (`sub-vertical-slice`, `sub-schema-syncer`).

---

## 1. Princípio do Fatiamento Vertical (*Vertical Slices*)
- Em vez de implementar camadas isoladas (apenas backend ou apenas frontend) que ficam órfãs, o especialista Fullstack entrega **fluxos completos e funcionais de ponta a ponta**:
  `Banco de Dados / Modelo -> API / Rota -> Cliente / Hook -> Interface / Componente UI -> Feedback ao Usuário`.
- Cada fatia vertical deve ser autônoma, testável e pronta para uso imediato pelo usuário final.

---

## 2. Sincronização de Tipos e Contratos (Single Source of Truth)
1. **Tipagem Compartilhada (End-to-End Type Safety)**:
   - Utilizar contratos tipados compartilhados (ex: schemas Zod inferindo tipos TypeScript, tRPC, OpenAPI gerado para clientes tipados).
   - Qualquer alteração em um campo da API deve propagar imediatamente para os componentes de interface correspondentes.
2. **Tratamento Resiliente de Estados**:
   - Toda integração fullstack deve gerenciar explicitamente 4 estados essenciais na UI:
     - `Idle`: Estado inicial antes da ação.
     - `Loading / Pending`: Indicador visual claro (skeleton, spinner, estado desabilitado).
     - `Error`: Mensagem de erro amigável e acionável com opção de retry.
     - `Success`: Atualização instantânea da interface e feedback ao usuário (toast, redirecionamento, optimistic update).

---

## 3. Diretrizes para os Sub-Agentes Fullstack
- **`sub-vertical-slice`**:
  - Orquestra a implementação simultânea das camadas front e back de um recurso.
  - Assegura que Server Components, Server Actions ou chamadas REST/GraphQL estejam perfeitamente amarradas aos formulários e exibições.
- **`sub-schema-syncer`**:
  - Audita a paridade de tipos entre DTOs do backend e interfaces do frontend.
  - Garante que validações de formulário no cliente espelhem exatamente as regras de validação do servidor.
