# lgpd
Diretrizes normativas e conformidade com a LGPD (Lei Geral de Proteção de Dados - Lei nº 13.709/2018).

Projetar e implementar sistemas seguindo Privacy by Design e Privacy by Default.
Coletar estritamente os dados pessoais necessários para a finalidade declarada (princípio da necessidade e minimização).
Exigir consentimento livre, informado e inequívoco para cookies não essenciais e rastreadores; nunca utilizar caixas de seleção pré-marcadas.
Garantir canais e fluxos operacionais para os direitos dos titulares (acesso, confirmação, correção, anonimização, portabilidade e exclusão).
Proteger dados pessoais em repouso e em trânsito com criptografia robusta (HTTPS/TLS obrigatório, senhas com bcrypt ou argon2).
Proibido expor dados sensíveis ou pessoais (CPF, dados bancários, senhas, tokens) em logs, URLs, telas públicas, telemetria ou repositórios.
Anonimizar ou mascarar dados em ambientes de desenvolvimento, homologação, testes e relatórios.
Definir políticas de retenção e rotinas de descarte seguro quando a finalidade do tratamento for atingida.
