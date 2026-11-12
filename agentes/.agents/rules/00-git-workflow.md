# Regra 00: Fluxo Estrito de Git e Isolamento de Branches

Esta regra é de cumprimento obrigatório para todos os agentes ao interagir com o controle de versão Git.

---

## 1. Regra Fundamental de Proteção da Branch Principal
- **NUNCA** commitar ou fazer alterações diretas na branch `main` ou `master`.
- Toda nova demanda (feature, refatoração, correção de bug) **DEVE** iniciar com a criação de uma branch dedicada a partir do estado atualizado da `main`/`master`.

---

## 2. Padrão de Nomenclatura de Branches
As branches devem seguir a convenção semântica com kebab-case:
- `feature/<descricao-curta>`: Para novos recursos e melhorias (ex: `feature/auth-jwt-login`).
- `fix/<descricao-curta>`: Para correções de bugs (ex: `fix/button-hydration-mismatch`).
- `refactor/<descricao-curta>`: Para melhorias estruturais sem alteração de comportamento externo.
- `chore/<descricao-curta>`: Para atualizações de dependências, configs e documentação.

---

## 3. Padrão de Commits Atômicos Semânticos (Conventional Commits)
Todo commit deve ser atômico (uma única responsabilidade lógica bem definida) e seguir a convenção:

```
<tipo>(<escopo opcional>): <descrição no imperativo e em minúsculas>

[corpo opcional explicando o 'porquê' e não apenas o 'o quê']

[rodapé opcional com referências a issues ou breaking changes]
```

### Tipos Permitidos:
- `feat`: Nova funcionalidade para o usuário final.
- `fix`: Correção de bug.
- `docs`: Alterações exclusivamente em documentação.
- `style`: Formatação, ponto e vírgula, sem alteração de lógica.
- `refactor`: Refatoração de código que não corrige bug nem adiciona funcionalidade.
- `perf`: Mudança de código focada em ganho de performance.
- `test`: Adição ou correção de testes automatizados.
- `chore`: Tarefas de build, configurações de ferramentas ou pacotes.

---

## 4. Checklist do Git Guard antes de qualquer Commit/Merge
1. [ ] Verificar se a branch atual **não** é `main` ou `master` (`git branch --show-current`).
2. [ ] Garantir que nenhum segredo (`.env`, chaves de API, senhas) está no staging (`git status`).
3. [ ] Confirmar que apenas os arquivos explicitamente modificados estão no staging (`git add <arquivos-específicos>`). **Evitar `git add .` indiscriminado**.
4. [ ] Validar que todos os testes automatizados passaram antes de commitar.
