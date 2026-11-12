# Regra 06: Protocolo Forense de Triagem, Investigação e Correção de Bugs

Esta regra governa o trabalho do **`@deep-debugger`** (Líder de Investigação) e seus sub-agentes auxiliares (`sub-root-cause`, `sub-repro-generator`, `sub-patch-verifier`).

---

## 1. O Pipeline Forense de 4 Etapas

```
[1. Isolamento & Hipótese] ──> [2. Reprodução Automatizada] ──> [3. Patch Cirúrgico] ──> [4. Validação Anti-Regressão]
     (sub-root-cause)              (sub-repro-generator)          (Especialista)             (sub-patch-verifier)
```

---

## 2. Detalhamento Operacional dos Sub-Agentes de Bugs

### Etapa 1: Investigação Forense (`sub-root-cause`)
- Coleta stack traces, logs de erro, payload que gerou a falha e condições de ambiente.
- Realiza análise reversa do fluxo de dados até encontrar a causa-raiz (ex: mutação de estado assíncrono, condição de corrida, tipo `undefined`, estouro de limite).
- **Proibição**: Nunca aplicar "remendos superficiais" (como `try/catch` vazios ou mascaramento de erros com `as any` ou `|| {}`) sem tratar a causa-raiz.

### Etapa 2: Criação do Teste de Reprodução (`sub-repro-generator`)
- Escreve um teste unitário ou de integração automatizado mínimo que **falha com precisão** (estado vermelho).
- Esse teste serve como prova matemática do bug e garantia futura contra regressão.

### Etapa 3: Aplicação do Patch Cirúrgico
- O especialista de domínio (`frontend`, `backend` ou `fullstack`) modifica o código com o menor diff possível para sanar a causa-raiz.

### Etapa 4: Validação Anti-Regressão (`sub-patch-verifier`)
- Executa o teste de reprodução e comprova que ele agora **passa com sucesso** (estado verde).
- Executa a suíte de testes existente do projeto para garantir que nenhuma funcionalidade adjacente foi quebrada.
- Emite o `BUG_RESOLUTION_REPORT.md`.

---

## 3. Formato do Relatório de Resolução de Bug (`BUG_RESOLUTION_REPORT.md`)
```markdown
# Relatório Forense de Resolução de Bug

## 1. Descrição do Problema
- **Sintoma Observado**: [Erro relatado pelo usuário ou log]
- **Componentes Afetados**: `src/server/auth.ts:L45`

## 2. Diagnóstico da Causa-Raiz (Root Cause)
- [Explicação detalhada do porquê o erro ocorria]

## 3. Teste de Reprodução Adicionado
- `tests/bugs/repro-issue-42.test.ts` (Validado: Falhou antes do fix, Passou após o fix).

## 4. Patch Aplicado
- Resumo cirúrgico das alterações realizadas.

## 5. Garantia Anti-Regressão
- Suíte completa de testes executada: [X] testes passaram sem erros.
```
