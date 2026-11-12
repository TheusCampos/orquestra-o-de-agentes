# Regra 08: Engenharia de Segurança, Modelagem de Ameaças e Auditoria Contínua

Esta regra governa o trabalho do **`@security-specialist`** e seus sub-agentes auxiliares (`sub-security-auditor`, `sub-secret-detector`, `sub-threat-modeler`, `sub-compliance-guard`).

---

## 1. Diretrizes de Auditoria SAST e OWASP Top 10 (`sub-security-auditor`)
1. **Injeção de Código e Dados**:
   - Queries de banco de dados **sempre** parametrizadas através de ORMs ou prepared statements. Concatenação de SQL ou comandos de shell é terminantemente proibida.
   - Sanitização rigorosa de entradas do usuário para prevenção de XSS (Cross-Site Scripting) em formulários e renderização de HTML.
2. **Controle de Acesso e Quebra de Autenticação (Broken Auth & IDOR)**:
   - Todo endpoint de leitura ou mutação deve verificar o token JWT e validar se o usuário autenticado é o proprietário do recurso que está tentando acessar/modificar (*Insecure Direct Object References - IDOR*).

---

## 2. Detecção Ativa de Segredos e Credenciais (`sub-secret-detector`)
1. **Regra de Zero Credenciais em Código**:
   - Nenhuma chave de API privada, token JWT, connection string com senha ou certificado privado pode existir em código versionado.
   - Padrões regex e entropy scanning aplicados contra: `AIzaSy...`, `sk_live_...`, `BEGIN PRIVATE KEY`, `ghp_...`, `eyJhbGci...`.
2. **Uso Exclusivo de `.env`**:
   - Todas as variáveis sensíveis devem residir em `.env` ou gerenciadores de segredos seguros, mantendo apenas arquivos `.env.example` sem valores reais no repositório.

---

## 3. Modelagem de Ameaças (`sub-threat-modeler`)
1. Ao implementar novos recursos ou fluxos de dados sensíveis (pagamentos, senhas, dados cadastrais):
   - Mapear a superfície de ataque utilizando o framework **STRIDE** (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
   - Implementar rate-limiting e mitigação contra ataques de força bruta.

---

## 4. Conformidade e Headers de Segurança (`sub-compliance-guard`)
1. **Headers HTTP Obrigatórios em Produção**:
   - `Content-Security-Policy (CSP)`
   - `Strict-Transport-Security (HSTS)`
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY` ou `SAMEORIGIN`
   - `Referrer-Policy: strict-origin-when-cross-origin`
2. **Cookies de Sessão**:
   - Flags obrigatórias: `HttpOnly`, `Secure`, `SameSite=Lax` ou `Strict`.
3. **Privacidade e LGPD/GDPR**:
   - Não logar dados pessoais identificáveis (PII) ou senhas em texto puro nos logs do sistema.
