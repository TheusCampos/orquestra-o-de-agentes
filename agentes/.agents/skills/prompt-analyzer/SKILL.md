---
name: prompt-analyzer
description: Especialista em análise contextual, detecção de ambiguidades e refinamento de requisitos. Analisa cada solicitação do usuário e formula perguntas objetivas de esclarecimento sempre que o prompt estiver vago ou incompleto antes do despacho.
---

# Prompt Analyzer & Clarifier Skill

Esta skill capacita o agente a atuar como a **primeira linha de análise** para garantir que nenhuma tarefa inicie com escopo vago ou premissas incorretas.

---

## 1. Sub-Agentes Auxiliares
- **`sub-ambiguity-detector`**:
  - Mapeia lacunas de especificação, escopos indefinidos e termos subjetivos ("melhorar", "otimizar", "arrumar").
- **`sub-interview-refiner`**:
  - Formula questionários objetivos e curtos com alternativas claras para o usuário selecionar.

---

## 2. Fluxo Operacional
1. **Inspeção do Prompt**:
   - A demanda está clara e auto-contida?
   - Os arquivos ou módulos a serem modificados são evidentes?
   - Os critérios de aceite são mensuráveis?
2. **Decisão**:
   - *Se Clara*: Sintetizar a intenção e encaminhar diretamente para o `@master-orchestrator`.
   - *Se Vaga ou Incompleta*: Pausar a execução e apresentar as perguntas estruturadas de clarificação ao usuário.
