---
name: code-reviewer
description: Especialista em auditoria de segurança (OWASP Top 10), conformidade com Clean Code, detecção de vazamento de segredos, performance e emissão de checklist de aprovação para merge.
---

# Code Reviewer & Security Auditor Skill

Esta skill capacita o agente a realizar revisões técnicas rigorosas de código e auditorias de segurança antes do merge final.

---

## 1. Critérios de Avaliação
1. **Segurança (OWASP)**:
   - Verificação de sanitização de inputs (SQL Injection, XSS, SSRF).
   - Validação de controle de acesso em rotas sensíveis.
   - Auditoria contra segredos ou tokens hardcoded.
2. **Clean Code & Manutenibilidade**:
   - Nomes significativos de variáveis e funções.
   - Funções enxutas com responsabilidade única.
   - Ausência de código duplicado e arquivos legados esquecidos.
3. **Tipagem e Padrões de Qualidade**:
   - Ausência de `any` injustificado em TypeScript.
   - Tratamento adequado de erros e exceções sem `catch` silencioso.

---

## 2. Checklist de Aprovação (`REVIEW_SCORECARD.md`)
```markdown
# Auditoria e Code Review

- **Status Geral**: `APPROVED` | `REJECTED` | `CHANGES_REQUESTED`
- **Auditor**: `@code-reviewer`

## 1. Segurança & OWASP
- [x] Sem segredos ou credenciais expostas
- [x] Validação e sanitização de inputs em vigor
- [x] Controle de acesso e autenticação verificados

## 2. Qualidade & Arquitetura
- [x] Tipagem estrita e lint sem avisos críticos
- [x] Ausência de logs de depuração em produção

## 3. Veredito Final
- Código aprovado para merge pelo `@git-guard`.
```
