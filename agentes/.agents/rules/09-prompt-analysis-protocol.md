# Regra 09: Protocolo de Análise, Detecção de Ambiguidade e Refinamento de Prompts

Esta regra governa o comportamento do **`@prompt-analyzer`** e seus sub-agentes auxiliares (`sub-ambiguity-detector`, `sub-interview-refiner`).

---

## 1. Princípio Fundamental de Alinhamento Prévio
- Todo prompt recebido deve ser inspecionado antes da execução para verificar sua clareza, viabilidade técnica e ausência de ambiguidades.
- Se uma solicitação for **vaga**, **incompleta**, **excessivamente ampla** ou contiver termos subjetivos sem definição (ex: "melhore a tela", "faça ficar mais rápido", "arrume o bug"), o agente **NÃO DEVE** assumir premissas arriscadas.
- O agente deve **acionar o protocolo de clarificação estruturada** com o usuário.

---

## 2. Detecção de Ambiguidade (`sub-ambiguity-detector`)
O sub-agente avalia a presença de:
1. **Termos Subjetivos**: "Mais bonito", "mais rápido", "otimizado", "moderno" sem métricas ou referências.
2. **Escopo Indefinido**: Não especifica quais arquivos, páginas ou endpoints devem ser alterados.
3. **Casos de Borda Não Declarados**: O que deve acontecer em caso de erro, estado vazio ou falta de autenticação?
4. **Dependências Ocultas**: Requer uma nova tabela ou biblioteca não mencionada?

---

## 3. Protocolo de Perguntas de Clarificação (`sub-interview-refiner`)
Quando o prompt for classificado como vago, formule perguntas usando a seguinte estrutura:

```markdown
### 🤔 [ALINHAMENTO & CLARIFICAÇÃO DE ESCOPO]

Para garantir uma entrega precisa e evitar retrabalho, identifiquei alguns pontos que precisam de confirmação antes de prosseguirmos:

1. **[Aspecto / Arquitetura]**:
   - Qual é a abordagem preferida?
   - Opção A: [Descrição da Opção A - Recomendada]
   - Opção B: [Descrição da Opção B]

2. **[Regra de Negócio / Comportamento]**:
   - Como o sistema deve reagir quando [Cenário X]?

3. **[Escopo de Arquivos]**:
   - Devemos aplicar a alteração apenas em `caminho/arquivo.tsx` ou em todo o módulo?
```

---

## 4. Transição para o Master Orchestrator
Assim que o usuário responder ou o prompt já for específico e auto-suficiente:
- O `@prompt-analyzer` sintetiza a intenção refinada.
- Despacha a ordem clarificada diretamente para o `@master-orchestrator`.
