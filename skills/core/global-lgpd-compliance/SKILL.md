---
name: global-lgpd-compliance
description: Implementar diretrizes, avisos de privacidade, consentimento de cookies e tratamento seguro de dados pessoais conforme a LGPD.
---

# global-lgpd-compliance

## Fundamentos e escopo da LGPD
A Lei Geral de Proteção de Dados (Lei nº 13.709/2018) disciplina o tratamento de dados pessoais de indivíduos no Brasil.
Esta skill orienta a implementação técnica de conformidade em aplicações web, APIs e bancos de dados.

## Bases legais e mapeamento de dados
Identifique cada fluxo de entrada de dados pessoais e determine sua base legal (Art. 7º e 11 da LGPD):
- **Consentimento (Art. 7º, I)**: Uso de cookies de marketing/analíticos, recebimento de newsletters, campanhas promocionais.
- **Execução de Contrato (Art. 7º, V)**: Dados necessários para checkout, prestação de serviços, entrega de produtos.
- **Obrigação Legal ou Regulatória (Art. 7º, II)**: Emissão de notas fiscais, guarda de logs de conexão conforme Marco Civil da Internet.
- **Legítimo Interesse (Art. 7º, IX)**: Prevenção a fraudes e segurança da informação, com teste de proporcionalidade documentado.
Aplique minimização: remova formulários com campos dispensáveis (ex: não solicitar CPF ou data de nascimento quando apenas e-mail ou nome bastam).

## Banner de cookies e gestão de consentimento
- **Opt-in Ativo**: Scripts e cookies não essenciais (Google Analytics, Meta Pixel, ferramentas de gravação de tela) NÃO podem ser carregados antes do aceite explícito do usuário.
- **Categorização transparente**:
  1. *Necessários*: Essenciais para segurança, sessão e carrinho de compras (não requerem consentimento, mas devem ser informados).
  2. *Analíticos/Estatísticos*: Medição de uso anônima (exigem consentimento).
  3. *Marketing/Publicidade*: Rastreamento para anúncios direcionados (exigem consentimento).
- **Sem caixas pré-marcadas**: As opções de consentimento devem vir desmarcadas por padrão.
- **Persistência do consentimento**: Armazenar a escolha do usuário no `localStorage` ou cookie técnico com identificador, timestamp e versão dos termos.
- **Facilidade de revogação**: Manter no rodapé do site um link ou botão visível ("Gerenciar Cookies" ou "Preferências de Privacidade") que reabra o painel de consentimento a qualquer instante.

## Formulários, termos e contratos
- Formulários de contato ou cadastro devem conter um checkbox explícito de concordância com os termos:
  `[ ] Li e concordo com a Política de Privacidade.` (sem pré-seleção).
- Link visível e direto para a página de `/politica-de-privacidade` e `/termos-de-uso`.
- Finalidade descrita em linguagem clara, simples e acessível ao cidadão comum.

## Segurança e proteção de dados (Privacy by Design)
- **Criptografia em trânsito**: HTTPS (TLS 1.2+) obrigatório em todas as rotas; redirecionamento automático de HTTP para HTTPS; cabeçalho HSTS (`Strict-Transport-Security`).
- **Criptografia em repouso**: Senhas com funções de derivação de chave fortes com sal (Argon2id ou Bcrypt com custo adequado); dados bancários/cartões delegados a gateways PCI-DSS (não armazenar CVV ou números de cartão no banco local).
- **Sanitização de logs**: Nunca registrar no console ou em arquivos de log: senhas, hashes de senha, tokens de autorização, CPF, números de cartão ou dados médicos/sensíveis. Criar filtros no middleware de logging.
- **Mascaramento visual (PII Masking)**: Exibir dados pessoais mascarados na interface do usuário (ex: `***.456.789-**` para CPF, `(11) 9****-1234` para telefone, `m*****@dominio.com` para e-mail).

## Direitos dos titulares (Art. 18 da LGPD)
O sistema deve prever mecanismos operacionais ou automatizados para atender:
- Confirmação da existência de tratamento e acesso aos dados.
- Correção de dados incompletos, inexatos ou desatualizados.
- Anonimização, bloqueio ou eliminação de dados desnecessários ou tratados em desconformidade.
- Portabilidade dos dados a outro fornecedor (exportação em formato legível por máquina, como JSON ou CSV).
- Revogação do consentimento com eliminação dos dados tratados sob essa base.

## Verificação e auditoria de conformidade
1. Abrir o site em modo anônimo e verificar se cookies de terceiros ou analytics são injetados antes do consentimento no banner.
2. Inspecionar requisições de rede para garantir que nenhum dado pessoal é transmitido via URL (GET query string).
3. Verificar a presença dos links de rodapé para a Política de Privacidade e gerenciador de cookies.
4. Executar varredura no código para confirmar ausência de senhas e credenciais em texto claro.
