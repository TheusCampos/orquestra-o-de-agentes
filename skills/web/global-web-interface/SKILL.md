---
name: global-web-interface
description: Construir ou refinar sites e interfaces web com direção visual, interação, movimento acessível e validação no navegador.
---

# global-web-interface

## Direção antes de implementação
Parta da identidade e dos componentes existentes ou da referência do usuário. Quando a direção estiver aberta, escolha um conceito coerente com público e tarefa, declare a suposição e avance. Não force uma nova identidade em uma correção local.

Para página nova ou redesign, escreva um briefing curto com ação principal, composição da primeira dobra, contraste tipográfico, paleta, espaçamento, arte e intenção de movimento. Confira a primeira dobra antes de expandir. Sites expressivos devem ter alguma decisão visual reconhecível que decorra do conteúdo; cor de destaque, gradiente e cards uniformes isoladamente não demonstram uma direção.

Leia [references/visual-direction.md](references/visual-direction.md) ao criar ou redesenhar páginas. Contém critérios de composição e revisão, sem prescrever um template único.

## Fluxo, conteúdo e contratos
Defina hierarquia, navegação e estados de carga, vazio, erro e sucesso pertinentes. Cada controle visível precisa produzir o resultado anunciado. Distingua demonstração local de integração real e não invente clientes, depoimentos ou métricas como fatos.

Use HTML semântico, rótulos, foco visível e teclado. Ajuste layout pelo conteúdo, incluindo títulos longos e dados realistas. Preserve contratos com backend; dúvidas de formato/erro precisam chegar ao produtor, não virar mocks silenciosos.

## Movimento e robustez
Em pedidos animados ou de experiência expressiva, planeje movimento como parte da direção: gatilho, alvo, duração/intensidade e comportamento reduzido. Leia [references/motion-and-browser-qa.md](references/motion-and-browser-qa.md) para implementação e verificação. Pequenas correções funcionais não exigem adicionar animação.

Prefira transform/opacity quando apropriado; preserve layout e conteúdo na ausência de JS. Respeite prefers-reduced-motion, teclado e dispositivos sem hover. Use as dependências da stack; uma interação simples não justifica trocar framework ou adicionar biblioteca pesada.

## Verificação e entrega
Execute build/sintaxe conforme a stack e abra o resultado no navegador disponível. Inspecione a primeira dobra e a página completa, em desktop e mobile, com capturas e exercício da ação principal; use a matriz da referência de QA. Corrija defeitos observados antes de concluir a verificação.

Relate viewports, fluxo exercitado, erros de console/rede pertinentes, capturas, motion e redução de movimento. Sem navegador, marque QA visual e interação real como pendentes, informe ferramenta/erro e o passo para executar a verificação. Validação estrutural e DOM simulado não comprovam fidelidade visual. Não declare a página visualmente aprovada apenas porque o build passou.
