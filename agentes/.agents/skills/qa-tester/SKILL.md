---
name: qa-tester
description: Especialista em garantia de qualidade (QA), automação de testes unitários, testes de integração, validações E2E e testes de estresse em casos de borda. Gera relatórios de validação e cobertura.
---

# QA & Test Runner Skill

Esta skill capacita o agente a executar, criar e analisar suítes de testes automatizados com cobertura rigorosa.

---

## 1. Responsabilidades
1. **Execução de Suítes Automatizadas**:
   - Rodar comandos de teste do projeto (`npm test`, `pytest`, `cargo test`, `go test`, `vitest`).
   - Identificar falhas, analisar logs de execução e reportar gargalos.
2. **Criação de Testes para Casos de Borda**:
   - Desenvolver cenários de teste com entradas nulas, vazias, limites numéricos extremos e timeouts.
3. **Validação E2E e de Integração**:
   - Assegurar que fluxos compostos funcionam de forma integrada e determinística.

---

## 2. Padrão de Relatório de Testes (`QA_TEST_REPORT.md`)
```markdown
# Relatório de Execução de Testes (QA)

- **Total de Testes**: [N]
- **Passaram**: [N]
- **Falharam**: [N]
- **Tempo de Execução**: [X.Xs]
- **Cobertura de Linhas**: [XX%]

## Casos de Borda Validados
- [x] Payload vazio / undefined
- [x] Limite de caracteres excedido
- [x] Injeção de caracteres especiais / Unicode
```
