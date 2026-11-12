---
name: product-quality-evaluator
description: Especialista em métricas de produto, benchmarking técnico e geração de scorecards de qualidade (0 a 100). Acionado exclusivamente sob demanda (quando invocado ou ao solicitar métricas/nota do sistema).
---

# Product Quality Evaluator Skill

Esta skill capacita o agente a gerar diagnósticos aprofundados e relatórios de pontuação técnica global do projeto.

---

## 1. Condição de Execução (On-Demand)
- **Atenção**: Esta skill é executada **apenas sob demanda**, quando o usuário pedir expressamente uma nota, auditoria geral de qualidade ou métricas do projeto.

---

## 2. Sub-Agentes Auxiliares
- **`sub-architecture-scorer`**:
  - Avalia coesão modular, acoplamento, Clean Architecture e componentização (Peso: 25%).
- **`sub-health-auditor`**:
  - Analisa qualidade de tipagem, débito técnico, complexidade e cobertura de testes (Pesos combinados: 35%).
- **`sub-benchmark-reporter`**:
  - Audita segurança, UX/SEO/A11y e consolida a pontuação de 0 a 100 com o radar e o plano de ação (Pesos combinados: 40%).

---

## 3. Entregável Principal
- Emissão do arquivo `PRODUCT_QUALITY_SCORECARD.md` na raiz ou no diretório de relatórios com as notas calculadas e o plano de evolução prioritário.
