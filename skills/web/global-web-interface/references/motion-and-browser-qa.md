# Movimento e QA no navegador

## Escolha e implementação de movimento
Use movimento para orientar atenção, mostrar relações ou confirmar mudança. Para cada efeito relevante, registre alvo, gatilho, intensidade e fallback. Exemplos: entrada curta da primeira dobra; revelação discreta de seção; transição de conteúdo em uma demonstração; resposta de botão/modal. Não é necessário empilhar efeitos nem aplicar todos os exemplos.

Faixas iniciais, ajustáveis ao contexto: feedback de controles em 120–220 ms e entradas em 300–600 ms. Stagger curto pode guiar leitura; não atrase acesso aos controles. Prefira transform/opacity quando apropriado. Evite animar propriedades de layout a cada frame, parallax intenso, cursor obrigatório, rolagem sequestrada e movimento automático interminável sem controle.

Revelações progressivas precisam de fallback: conteúdo visível por padrão, ou restauração segura se a inicialização falhar. Não deixe seções permanentemente com opacity: 0 esperando um observer. Evite esconder o principal visual até uma animação ou download completar.

Em prefers-reduced-motion, reduza/remova deslocamentos e loops, preservando feedback de estado e acesso ao conteúdo. Confira a preferência no navegador, incluindo mudança em runtime quando o código observar matchMedia. Efeitos hover não podem ser necessários no touch ou no teclado. Movimento automático prolongado precisa de pausa/controle quando aplicável.

## Matriz mínima para página nova ou redesign substancial
Use ferramentas já disponíveis no ambiente: navegador controlável, automação instalada ou outro renderer real compatível. Não assuma indisponibilidade apenas porque um executável conhecido não está no PATH. Se não houver renderer adequado, registre a limitação real sem transformar inspeção de código em aprovação visual.

| Verificação | Evidência útil |
| --- | --- |
| Desktop e mobile representativos (por exemplo 1440 × 900 e 390 × 844) | Capturas da primeira dobra e página completa; dimensões registradas |
| Limite estreito e pontos onde o layout muda | Conferir overflow horizontal, quebras, sobreposição e alvos de toque; acrescentar tablet se houver mudança intermediária |
| Ação principal e navegação | Exercitar links, formulário, menu, modal ou demo relevantes; verificar resultado e retorno de foco |
| Teclado | Percorrer controles, observar foco e fechar overlays com o mecanismo previsto |
| Movimento normal e reduzido | Observar efeitos após load/scroll/interação e confirmar conteúdo acessível com preferência reduzida |
| Console e rede | Registrar falhas pertinentes à página; verificar assets e fonte efetivamente utilizados |
| Conteúdo e layout | Comparar com briefing, contraste, legibilidade e estados relevantes; não usar somente screenshot da hero |

Para alteração local, execute apenas linhas afetadas e o fluxo essencial. Quando usar testes automatizados, priorize comportamento observável (menu abre/fecha, formulário apresenta resultado, nenhum conteúdo fica oculto), não seletores ou snapshots que apenas espelhem a implementação.

## Relatório de verificação
Registre URL/caminho servido, ferramenta, viewports, fluxo, capturas e resultados separados em funcional, visual e movimento. Informe defeitos corrigidos e checks pendentes. Uma captura comprova o estado fotografado; não comprova sozinha teclado, transição ou ausência de erros. Um build aprovado não comprova nenhum desses comportamentos.
