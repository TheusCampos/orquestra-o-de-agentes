# Verificação — 0.2.0

Data local: 2026-10-06. Windows PowerShell e codex-cli 0.160.1.

## Executado
- validate.ps1: dez agentes, vinte skills, oito regras e sete perfis; nomes, caminhos, frontmatter, protocolo, referências externas e skills preferenciais por perfil verificados.
- test-memory.ps1: leitura sem criar arquivos, preview, inicialização, persistência, preservação do texto curado, IDs idempotentes, conflitos de ID, ações confirmadas com evidência, correções, busca, marcadores, histórico sem quebra final, exclusão de escritores simultâneos e recusa de JSON corrompido.
- Busca por conteúdo antigo recuperou a correção cujo texto não continha o termo pesquisado; estado superseded confirmado.
- test-integration.ps1: instalação, preservação de configuração pessoal, preview, idempotência, conflitos, confinamento, marcadores e todos os sete perfis.
- Atualização em cópia isolada para 0.2.1 preservou BRAIN.md e distribuiu script de memória funcional; journal criado no projeto instalado.
- codex debug prompt-input: instrução BRAIN.md, skill global-persistent-memory, global-security-assessment e referência de orquestrador encontradas no contexto exportado.
- Cérebro desta biblioteca preenchido com resumos dos pedidos da conversa, implementação anterior e decisões de memória.

## Artefatos
- .work/memory-d01d4ffa9d07443b92c801689a2b3fd3/
- .work/integration-79d35436096c40d5b9b442584fa8a4cc/
- .work/prompt-diagnostic-0.2.0.json
- BRAIN.md e memory/events.jsonl

## Limites
Não houve chamada ao modelo, execução de cenários de produto em sessões novas ou invocação comprovada dos custom agents. A exportação local demonstra descoberta de instruções/skills, não obediência garantida de modelos.
A memória captura os resumos registrados; não captura automaticamente cada mensagem da interface.
Nenhuma skill externa foi instalada. Licenças, commits fixos e scripts de pacotes externos ainda não foram validados para importação.
O validador de skills usado foi o local em PowerShell, sem atribuir execução ao quick_validate.py.

