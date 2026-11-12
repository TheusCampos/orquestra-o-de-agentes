# Regra 03: Padrões de Frontend, UI/UX, SEO, Performance e Acessibilidade

Esta regra governa o trabalho do **`@frontend-specialist`** e seus sub-agentes auxiliares (`sub-ui-builder`, `sub-browser-tester`, `sub-seo-optimizer`, `sub-performance-optimizer`, `sub-clean-ui-auditor`, `sub-a11y-enforcer`).

---

## 1. Princípios de Excelência Visual e Estética
- **Design de Alto Impacto (Rich Aesthetics)**: O design deve impressionar à primeira vista. Interfaces comuns ou genéricas são inaceitáveis.
- **Paletas Curadas e Modernas**: Utilize paletas HSL/RGB coerentes, temas escuros elegantes (dark mode), gradientes suaves e profundidade com sombras sutis ou glassmorphism.
- **Tipografia Moderna**: Utilize tipografia contemporânea (ex: Inter, Outfit, Plus Jakarta Sans, Roboto) com hierarquia visual clara (h1, h2, corpo, legendas).
- **Micro-Interações e Feedback**: Todos os elementos interativos devem ter estados de hover, active, focus-visible e transições suaves (`transition: all 0.2s ease`).

---

## 2. Otimização Técnica de SEO (`sub-seo-optimizer`)
1. **Meta Tags e Redes Sociais**:
   - Títulos de página dinâmicos e descritivos (`<title>`).
   - Meta descriptions atraentes (< 160 caracteres).
   - Tags OpenGraph (`og:title`, `og:description`, `og:image`, `og:type`) e Twitter Cards (`twitter:card`, `twitter:image`).
2. **Dados Estruturados e Indexação**:
   - Schemas JSON-LD Schema.org (Product, Organization, Article, BreadcrumbList).
   - Estrutura semântica rigorosa com exatamente **um único `<h1>` por página** e hierarquia ordenada (`<h2>` a `<h6>`).
   - Geração e manutenção de `sitemap.xml` e `robots.txt`.

---

## 3. Velocidade e Core Web Vitals (`sub-performance-optimizer`)
1. **Métricas Vitais**:
   - **LCP (Largest Contentful Paint)**: < 2.5s. Imagens hero com preload, formatos modernos (WebP/AVIF) e dimensões explícitas `width`/`height`.
   - **INP (Interaction to Next Paint)**: < 200ms. Evitar tarefas longas na thread principal, desmembrar renderizações pesadas.
   - **CLS (Cumulative Layout Shift)**: < 0.1. Reservar espaço para imagens, skeletons e banners dinâmicos.
2. **Otimização de Assets e Bundles**:
   - Lazy loading de imagens e componentes abaixo da dobra (*code-splitting* dinâmico com `React.lazy` ou Dynamic Imports).
   - Otimização de importações para viabilizar Tree-Shaking eficiente.

---

## 4. Boas Práticas e Clean Code UI (`sub-clean-ui-auditor`)
1. **Componentização Pura**:
   - Manter componentes focados e com responsabilidade única.
   - Separar lógica de visualização (Custom Hooks vs. Presentational Components).
   - Respeitar o princípio DRY evitando duplicações desnecessárias de layouts e classes.
2. **Gerenciamento de Estados**:
   - Manter estados locais nos componentes mais baixos da árvore sempre que possível.

---

## 5. Acessibilidade Universal (`sub-a11y-enforcer` - WCAG 2.1/2.2 AA)
1. **Semântica e Leitores de Tela**:
   - Uso de tags semânticas (`<main>`, `<section>`, `<article>`, `<nav>`, `<header>`, `<footer>`, `<aside>`).
   - Atributos `aria-label`, `aria-expanded`, `aria-hidden` e `role` onde elementos nativos não forem suficientes.
2. **Navegação por Teclado e Foco**:
   - Todos os fluxos operáveis via teclado (`Tab`, `Shift+Tab`, `Enter`, `Space`, `Escape`).
   - Indicador de foco visualmente destacado (`focus-visible: ring-2`).
   - Relação de contraste de cores mínima de 4.5:1 para texto normal e 3:1 para texto grande/componentes de UI.
   - IDs únicos e descritivos em todos os elementos interativos para testes automatizados.
