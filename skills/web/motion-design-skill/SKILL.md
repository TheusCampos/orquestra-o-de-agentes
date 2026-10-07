---
name: motion-design-skill
description: Implementação de animações vetoriais fluidas com LottieFiles.
---

# Motion Design (Lottie)

Permite ao agente embutir animações complexas de After Effects exportadas em JSON na interface do usuário.

## Aplicação
- Ideal para ícones animados, loaders complexos e interações que chamam atenção sem penalizar a performance.
- Utilize o player do Bodymovin: `<script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>`.
- Acione a animação `lottie.loadAnimation(...)` definindo `container`, `path` do JSON, e se ela deve ocorrer em loop.
