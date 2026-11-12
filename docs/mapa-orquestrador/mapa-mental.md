# Mapa mental — orquestrador e agentes

```mermaid
mindmap
  root((Biblioteca de orquestração))
    Fonte da verdade
      agents
        10 papéis declarativos
        protocolo compartilhado
      registry
        agentes
        skills
        regras
      profiles
        7 composições
      agentlib
        sync
        tasks
        memory
        validate
    Orquestrador
      entrada de todo pedido
      lê contexto e memória
      define contrato de entrega
      seleciona perfil e especialistas
      integra e valida
      único escritor de memória no paralelo
    Especialistas
      arquitetura
      desenvolvimento geral
      frontend
      backend
      dados
      QA
      revisão independente
      segurança
      DevOps
    Execução real
      depende do runtime
        descoberta dos custom agents
        ferramenta de criar agentes
        canal de mensagens
      sem subagentes
        papéis em sequência
      com subagentes
        até 3 especialistas
        tarefas persistentes
        ownership exclusivo
        ACK obrigatório
        contratos versionados
    Persistência
      BRAIN.md
        resumo e checkpoint
      events.jsonl
        journal canônico
      events.json
        leitura estruturada
      memory.sqlite
        consultas
    Instalação por projeto
      agentlib sync
      AGENTS.md gerenciado
      .codex agents TOML
      .agents skills
      .agent-library fontes e manifesto
```

## Legenda operacional

```mermaid
flowchart TD
    U[Pedido do usuário] --> O[global-orchestrator]
    O --> C[Recupera contexto\nAGENTS + BRAIN + projeto]
    C --> R[Define critérios e roteia]
    R --> D{Há delegação\nno runtime?}
    D -- Não --> S[Executa papéis em sequência]
    D -- Sim --> T[Cria tarefas e reserva caminhos]
    T --> A[Especialistas dão ACK]
    A --> K{Contrato compartilhado?}
    K -- Sim --> P[Propõe e aceita\nversão do contrato]
    K -- Não --> E[Executa subtarefas]
    P --> E
    S --> I[Integra e verifica]
    E --> I
    I --> M[Registra decisão, ação e checkpoint]
    M --> F[Entrega resultado verificável]
```

Os losangos são controles reais do protocolo: não são apenas recomendações. Sem ferramenta de delegação, nenhuma subtarefa deve ser apresentada como trabalho paralelo. Sem ACK, ownership válido e contratos aceitos quando necessários, a tarefa não deve avançar para execução dependente.
