# Estado executável de tarefas

Use tarefas persistentes quando houver execução paralela, handoff ou contrato compartilhado. Para trabalho simples e sequencial, o registro é opcional.

```powershell
python -m agentlib task create --id TASK-001 --objective "Implementar API" --role backend --runtime-id /root/backend --paths src/api,tests/api
python -m agentlib task ack --id TASK-001 --runtime-id /root/backend
python -m agentlib task transition --id TASK-001 --state ready --runtime-id /root/backend
python -m agentlib task transition --id TASK-001 --state running --runtime-id /root/backend
```

Estados permitidos: `planned → ready → running → review → done`. `blocked` pode ser alcançado durante o trabalho e retorna para `ready` após o impedimento ser resolvido.

## Ownership

Cada caminho tem um único escritor ativo. A reserva de `src/api` também conflita com `src/api/users.py`. Para reatribuir, use `task transfer`; o ACK anterior é invalidado e o novo owner precisa confirmar antes de continuar.

## Contratos

```powershell
python -m agentlib task propose-contract --id TASK-001 --contract-id user-api --version v1 --runtime-id /root/backend --consumer-runtime-id /root/frontend --summary "GET /users retorna User[]"
python -m agentlib task accept-contract --id TASK-001 --contract-id user-api --version v1 --runtime-id /root/frontend
```

Uma tarefa não entra em `running`, `review` ou `done` enquanto houver contrato sem aceite. O envio de uma mensagem não equivale a aceite.

Os arquivos ficam em `.work/tasks/`. Use a CLI durante trabalho ativo para manter lock, validação e histórico coerentes.
