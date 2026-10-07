---
name: img2threejs
description: Transformação de imagens e assets em canvas WebGL interativos via Three.js.
---

# Img2ThreeJS

Esta skill instrui o agente de Creative Development a implementar fundos e imagens distorcidas em 3D.

## Aplicação
- Use Three.js para ler imagens via `TextureLoader` e aplicar shaders customizados.
- Excelente para efeitos de ripple, partículas e profundidade paralaxe em fotografias.
- CDN obrigatório: `<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>`
- Assegure-se de que o `canvas` possua `z-index` inferior ao conteúdo para servir como fundo responsivo e redimensionável (`window.addEventListener('resize')`).
