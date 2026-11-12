# Regra 10: Framework de Avaliação de Qualidade do Produto e Métricas 0-100 (On-Demand)

Esta regra governa a operação do **`@product-quality`** (`product-quality-evaluator`) e seus sub-agentes auxiliares (`sub-architecture-scorer`, `sub-health-auditor`, `sub-benchmark-reporter`).

---

## 1. Condição Estrita de Ativação (On-Demand)
- O `@product-quality` é um agente **exclusivamente sob demanda**.
- Ele **NÃO** deve ser executado automaticamente a cada tarefa comum para não onerar o tempo de resposta do desenvolvedor.
- Ele é disparado **apenas** quando:
  1. O usuário invocar explicitamente `@product-quality` ou `/product-quality`.
  2. O usuário solicitar uma nota, métrica, scorecard de qualidade, diagnóstico geral ou benchmark do projeto.

---

## 2. Pilares de Avaliação e Matriz de Pontuação (0 a 100)

O cálculo da nota consolidada baseia-se em 5 pilares com pesos técnicos:

| Pilar | Peso | Aspectos Avaliados |
|---|---|---|
| **1. Arquitetura & Modularidade** | 25% | Separação de responsabilidades, acoplamento, Clean Architecture, componentização e ausência de código duplicado. |
| **2. Qualidade de Código & Tipagem** | 20% | Conformidade TypeScript/Lint, ausência de `any`, legibilidade e convenções de nomenclatura. |
| **3. Segurança & Resiliência** | 20% | OWASP Top 10, proteção de segredos, sanitização de inputs, headers seguros e tratamento de erros. |
| **4. Frontend UX, SEO & A11y** | 20% | Acessibilidade WCAG, Core Web Vitals, semântica HTML, responsividade e tags de SEO. |
| **5. Cobertura de Testes & Débito Técnico** | 15% | Testes unitários/E2E, cenários de borda, complexidade ciclomática e facilidade de manutenção. |

---

## 3. Padrão do Relatório de Avaliação (`PRODUCT_QUALITY_SCORECARD.md`)

```markdown
# 📊 Scorecard de Qualidade do Produto

- **Data da Avaliação**: [Data/Hora]
- **Pontuação Global**: **[XX / 100]** ⭐⭐⭐⭐☆
- **Status Geral**: `EXCELENTE` (90-100) | `BOM` (75-89) | `ATENÇÃO` (50-74) | `CRÍTICO` (< 50)

---

## 1. Desempenho por Pilar

```mermaid
radar
  title Radar de Qualidade Técnica
  "Arquitetura": [Nota]
  "Qualidade & Tipagem": [Nota]
  "Segurança": [Nota]
  "Frontend & UX": [Nota]
  "Testes & Cobertura": [Nota]
```

- **Arquitetura & Modularidade**: **[XX/100]**
- **Qualidade de Código & Tipagem**: **[XX/100]**
- **Segurança & Resiliência**: **[XX/100]**
- **Frontend UX, SEO & A11y**: **[XX/100]**
- **Testes & Cobertura**: **[XX/100]**

---

## 2. Pontos Fortes Identificados
- [Ponto forte 1]
- [Ponto forte 2]

## 3. Oportunidades de Melhoria Prioritárias (Plano de Ação)
1. 🔴 **[Crítico / Alta Prioridade]**: [Ação recomendada]
2. 🟡 **[Média Prioridade]**: [Ação recomendada]
3. 🟢 **[Baixa Prioridade]**: [Ação recomendada]
```
