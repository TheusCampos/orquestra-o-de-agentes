# Arquitetura — 0.2.0
A biblioteca é a fonte de autoria. O adaptador copia uma versão por perfil para cada projeto.
Agentes têm missão, ativação, entradas, processo, decisões, skills, entregáveis, limites e exemplo. agents/protocol.md centraliza recuperação, evidência, colaboração e retorno.
O registro liga agentes a skills preferenciais e referências externas. Os perfis incluem essas skills; o validador verifica a composição.
O orquestrador é o comportamento do agente principal via AGENTS.md. O custom agent global-orchestrator pode ser chamado explicitamente; não há daemon ou scheduler próprio.
Delegação depende das ferramentas da sessão. Sem suporte, os papéis são executados sequencialmente.
Os agentes leem BRAIN.md na raiz do projeto. O orquestrador centraliza registros em memory/events.jsonl e atualiza o bloco recente do resumo. Especialistas retornam deltas.
A memória do projeto não é copiada da memória desta biblioteca. Somente o template inicial vai para projetos novos; histórico e preferências continuam isolados.
A sincronização gerencia fontes selecionadas em .agent-library, skills em .agents/skills e TOML em .codex/agents.
O protocolo é embutido no TOML gerado, e memory.ps1/common.ps1 são distribuídos na instalação.
Manifesto guarda hashes de arquivos da biblioteca. BRAIN.md é inicializado somente se ausente e excluído dos hashes; journal também pertence ao projeto.
AGENTS.md recebe bloco delimitado, com leitura e registro de memória. Texto externo ao bloco é preservado.
Configuração existente do Codex é preservada. Não há instalação automática em diretórios pessoais.
Fontes externas são catálogo com mapeamento por especialidade, não importações executáveis. Revisão fixa/licença entram antes da promoção.
Consulte docs/memory.md para recuperação, concorrência e limites de persistência.
