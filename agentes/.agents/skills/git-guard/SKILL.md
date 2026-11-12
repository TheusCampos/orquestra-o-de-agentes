---
name: git-guard
description: Especialista em segurança de Git, isolamento de branches, commits semânticos convencionais e integridade de staging. Impede alterações acidentais na branch main e prepara branches limpas para Pull Requests.
---

# Git Guard Skill

Esta skill capacita o agente a gerenciar operações de controle de versão com proteção total e rastreabilidade.

---

## 1. Regras Operacionais Inegociáveis
1. **Isolamento de Branches**:
   - Antes de iniciar qualquer trabalho de código, certifique-se de criar uma branch semântica:
     `git checkout -b feature/nome-da-tarefa` ou `git checkout -b fix/nome-do-bug`.
   - **NUNCA** permitir commits na branch `main` ou `master`.
2. **Staging Cirúrgico**:
   - Adicionar apenas os arquivos relacionados à tarefa: `git add <caminho/arquivo>`.
   - Não utilizar `git add .` para evitar inclusão de arquivos temporários, logs ou segredos.
3. **Commits Convencionais Atômicos**:
   - Formatar as mensagens seguindo o padrão `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`.
4. **Verificação de Integridade Pré-Commit**:
   - Garantir que a suíte de testes passou e que não há arquivos confidenciais (`.env`) em staging.
