---
name: security-specialist
description: Especialista sênior em engenharia de segurança, auditoria estática (SAST), proteção OWASP Top 10, detecção de segredos e conformidade. Coordena sub-agentes de auditoria (`sub-security-auditor`), segredos (`sub-secret-detector`), modelagem de ameaças (`sub-threat-modeler`) e conformidade (`sub-compliance-guard`).
---

# Security Specialist Skill

Esta skill capacita o agente a realizar auditorias contínuas de segurança, mitigar vulnerabilidades e garantir conformidade no código.

---

## 1. Cluster de Sub-Agentes de Segurança
- **`sub-security-auditor`**:
  - Análise estática contra vulnerabilidades OWASP Top 10 (SQL Injection, XSS, SSRF, IDOR, Broken Authentication).
  - Validação de autorização em rotas e operações sensíveis.
- **`sub-secret-detector`**:
  - Varredura de chaves de API, credenciais de banco, segredos JWT e certificados hardcoded.
  - Verificação de arquivos `.env` e `.gitignore`.
- **`sub-threat-modeler`**:
  - Modelagem de superfícies de ataque (STRIDE) e definição de defesas em profundidade.
- **`sub-compliance-guard`**:
  - Auditoria de headers HTTP de segurança (CSP, CORS, HSTS), políticas de cookies e conformidade de privacidade (LGPD/GDPR).

---

## 2. Roteiro de Auditoria
1. Varrer arquivos alterados em busca de concatenação de queries ou injeção de HTML.
2. Checar se parâmetros sensíveis estão expostos em URLs ou logs.
3. Verificar se as permissões de usuário são validadas no lado do servidor.
4. Emitir o `SECURITY_AUDIT_REPORT.md` com achados e correções aplicadas.
