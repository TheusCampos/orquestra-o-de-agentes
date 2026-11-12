# Regra 02: Protocolo Formal de Comunicação e Handoff Entre Agentes

Esta regra define como o **Master Orchestrator**, os **Especialistas**, os **Sub-Agentes** e os **Bug Agents** trocam tarefas, dados de contexto e resultados de execução sem ruído ou perda de requisitos.

---

## 1. Ciclo de Vida do Handoff

```
[Master Orchestrator]
       │ (1. Emite Task Dispatch Contract)
       ▼
[Agente Especialista / Sub-Agente]
       │ (2. Executa usando Skills & Rules específicas)
       ▼
[Validação Local / Sub-Agente Helper]
       │ (3. Produz Artefato de Saída / Diff)
       ▼
[Master Orchestrator / Próximo Agente] (4. Recebe Handoff Result)
```

---

## 2. Estrutura do Contrato de Despacho (`TASK_DISPATCH_CONTRACT`)
O Master Orchestrator sempre emite tarefas contendo:

```markdown
### 📋 [TASK DISPATCH CONTRACT]
- **Task ID**: `TASK-<ANO>-<NUMERO>`
- **Target Agent**: `@nome-do-agente` (ex: `@frontend-specialist`, `@backend-specialist`, `@deep-debugger`)
- **Sub-Agent Auxiliar**: (ex: `sub-ui-builder`, `sub-api-designer`, `sub-root-cause`)
- **Objetivo**: Descrição precisa e inequívoca do resultado esperado.
- **Arquivos Afetados / Contexto**:
  - `caminho/arquivo1.ts`
  - `caminho/arquivo2.tsx`
- **Restrições Arquiteturais**:
  - Ex: "Não utilizar dependências externas não instaladas".
  - Ex: "Manter compatibilidade com TypeScript 5+ em modo strict".
- **Critérios de Aceite (DoD - Definition of Done)**:
  1. [ ] Critério 1 verificável
  2. [ ] Critério 2 verificável
- **Handoff de Sucesso**: Próximo agente a ser notificado (`@qa-tester`, `@code-reviewer`, etc.).
```

---

## 3. Estrutura do Relatório de Conclusão de Handoff (`HANDOFF_REPORT`)
Ao concluir sua tarefa, todo agente especialista deve responder com o bloco padronizado:

```markdown
### 🚀 [HANDOFF REPORT]
- **Task ID**: `TASK-<ANO>-<NUMERO>`
- **Status**: `COMPLETED` | `BLOCKED` | `NEEDS_REVISION`
- **Agente Executor**: `@nome-do-agente`
- **Arquivos Criados / Modificados**:
  - `src/components/UserCard.tsx` (Criado)
  - `src/styles/theme.css` (Modificado)
- **Resumo Técnico da Entrega**: Breve descrição das alterações implementadas.
- **Evidências de Validação**:
  - [x] Testes unitários executados com sucesso
  - [x] Tipagem estrita validada sem erros
- **Próximo Passo Recomendado**: `@qa-tester` para execução de testes integrados.
```

---

## 4. Tratamento de Erros e Escalabilidade
- Se um agente encontrar um bloqueio ou dependência não resolvida, deve definir `Status: BLOCKED`, detalhar o impedimento no relatório de handoff e devolver a execução ao `@master-orchestrator`.
- Nenhum agente deve tentar "adivinhar" requisitos ausentes sem consultar a especificação ou registrar a decisão no relatório.
