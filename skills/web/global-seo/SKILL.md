---
name: global-seo
description: Otimizar páginas e aplicações web para motores de busca, visibilidade orgânica, dados estruturados (Schema.org), OpenGraph e Core Web Vitals.
---

# global-seo

## Princípios e estratégia técnica
Todo desenvolvimento web deve ser concebido para ser indexável, semântico e performático por padrão.
SEO não é uma camada adicionada ao final, mas uma disciplina integrada à semântica HTML, à arquitetura da informação, à velocidade de carregamento e à clareza dos metadados.

## Metadados e cabeçalho do documento (HTML Head)
Cada página pública deve conter tags essenciais no `<head>`:
- `<title>`: Conciso (50-60 caracteres), descritivo e único por página, contendo a palavra-chave primária e o nome da marca/projeto (ex: `Título da Página | Nome da Marca`).
- `<meta name="description">`: Resumo persuasivo e informativo (120-160 caracteres) com chamada para ação contextualizada.
- `<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">`.
- `<link rel="canonical" href="https://dominio.com.br/caminho-canonico">`: Obrigatório para consolidar autoridade e evitar conteúdo duplicado.
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`: Responsividade obrigatória.
- `<html lang="pt-BR">`: Idioma explicitado no elemento raiz.

## Open Graph e redes sociais
Metadados sociais para previews no WhatsApp, Facebook, LinkedIn e Twitter/X:
- `og:type` (`website` ou `article`), `og:site_name`, `og:title`, `og:description`, `og:url`.
- `og:image`: Imagem de alta resolução (recomendado: 1200x630px, proporção 1.91:1, formato WebP/JPG otimizado).
- `og:image:alt`: Descrição da imagem de compartilhamento.
- `og:locale`: `pt_BR`.
- `twitter:card`: `summary_large_image`.
- `twitter:title`, `twitter:description`, `twitter:image`.

## Dados estruturados (Schema.org / JSON-LD)
Injetar esquemas semânticos via `<script type="application/ld+json">`:
- `WebSite`: Nome do site, URL e `potentialAction` para busca interna (`SearchAction`).
- `Organization` / `LocalBusiness`: Nome, logotipo, telefones, endereço completo, horário e redes sociais (`sameAs`).
- Tipos de nicho (ex: `RealEstateAgent` para imobiliárias, `Product` para e-commerce, `Article` para blogs/notícias).
- `BreadcrumbList`: Navegação estruturada em trilhas de migalhas para exibição de hierarquia nas buscas.
- `FAQPage`: Perguntas e respostas frequentes para habilitação de rich snippets nas páginas de resultados.

## Semântica e arquitetura de conteúdo
- Exatamente um único `<h1>` por página, alinhado à intenção de busca principal.
- Hierarquia estrita de títulos: `<h1>` -> `<h2>` -> `<h3>` sem pular níveis para fins estéticos (utilize classes CSS para tamanho e peso tipográfico).
- Tags semânticas do HTML5: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`.
- Textos âncora claros: evitar "clique aqui", "saiba mais" ou URLs brutas; usar âncoras descritivas que informem o destino do link.
- Imagens: atributo `alt` descritivo e contextual em todas as imagens relevantes; `loading="lazy"` para elementos abaixo da primeira dobra; atributos `width` e `height` explícitos para evitar Cumulative Layout Shift (CLS).

## Rastreabilidade e indexação técnica
- `robots.txt`: Localizado na raiz do domínio, indicando `User-agent: *`, diretivas de bloqueio de áreas privadas (`Disallow: /admin/`, `Disallow: /api/`) e link absoluto para o sitemap (`Sitemap: https://dominio.com.br/sitemap.xml`).
- `sitemap.xml`: XML válido com tags `<urlset>`, `<loc>`, `<lastmod>` (formato ISO 8601), `<changefreq>` e `<priority>`.
- URLs limpas: em minúsculas, separadas por hífens (`kebab-case`), sem caracteres especiais ou query strings desnecessárias.

## Core Web Vitals e performance para SEO
- **LCP (Largest Contentful Paint < 2.5s)**: Priorizar carregamento da imagem ou bloco principal da primeira dobra; utilizar `<link rel="preload">` para fontes e imagens hero críticas; evitar lazy-loading na imagem hero.
- **INP / FID (Interaction to Next Paint < 200ms)**: Scripts pesados carregados com `defer` ou `async`; evitar bloqueio da thread principal.
- **CLS (Cumulative Layout Shift < 0.1)**: Reservar dimensões de imagens, banners e fontes com `font-display: swap` e propriedades `aspect-ratio`.

## Verificação e auditoria
- Validar conformidade de tags via DevTools e ferramentas de inspeção de DOM.
- Testar rich snippets no validador do Schema.org / Google Rich Results Test.
- Validar pontuação do Lighthouse (almejar pontuação 100 em SEO e Performance > 90).
- Confirmar ausência de links quebrados (404), erros de protocolo misto (HTTP em página HTTPS) e ausência de diretivas noindex acidentais em produção.
