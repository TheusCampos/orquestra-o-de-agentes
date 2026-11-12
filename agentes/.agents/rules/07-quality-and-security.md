# Regra 07: Qualidade de Código, Segurança OWASP e Auditoria

Esta regra governa o trabalho do **`@qa-tester`** e do **`@code-reviewer`**.

---

## 1. Diretrizes para o QA Tester (`@qa-tester`)
1. **Pirâmide de Testes Equilibrada**:
   - **Testes Unitários**: Rápidos, cobrindo funções puras, validadores e lógica de domínio.
   - **Testes de Integração**: Testando endpoints com banco de dados em memória/mock e fluxos de estado.
   - **Testes E2E / Browser**: Fluxos críticos do usuário (login, checkout, criação de registros).
2. **Cenários de Borda Obrigatórios**:
   - Payloads vazios, strings extremamente longas, caracteres especiais/Unicode, números negativos, datas inválidas e concorrência de requisições.
3. **Asserts Determinísticos**:
   - Testes não devem depender de ordem de execução ou de fatores de rede externos instáveis.

---

## 2. Diretrizes de Segurança para o Code Reviewer (`@code-reviewer`)
Todo código submetido deve passar pelo checklist **OWASP Top 10**:
1. **Controle de Acesso Quebrado**: Garantir que todo endpoint protegido valide o token e as permissões do usuário antes de processar os dados.
2. **Falhas Criptográficas**: Verificar se senhas, tokens e dados sensíveis utilizam criptografia moderna e nunca trafegam em texto puro.
3. **Injeção (SQL, NoSQL, OS Command)**: Garantir uso de queries parametrizadas (ORMs / Prepared Statements) e nunca concatenar strings em consultas.
4. **Vazamento de Segredos**: Auditar arquivos para assegurar que nenhuma chave de API, segredo JWT ou senha privada foi comitada.
5. **Configurações Incorretas de Segurança**: Verificar headers HTTP seguros (CORS restritivo, CSP, HSTS, X-Content-Type-Options).

---

## 3. Checklist de Aprovação Final de Entrega
Antes de autorizar o merge da branch para a `main`:
- [ ] 100% dos testes da suíte estão passando.
- [ ] Nenhuma vulnerabilidade crítica ou média apontada pelo scanner de segurança.
- [ ] Ausência de logs de depuração (`console.log`, `print`) no código de produção.
- [ ] Código com tipagem estrita sem o uso indiscriminado de `any`.
- [ ] Commits no padrão semântico do Git Guard.
