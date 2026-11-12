# Roteamento de skills e novos papéis

A biblioteca instala as skills de `registry/skills.json` conforme o perfil. As skills pessoais de `.agents/skills` são descobertas na sessão e distribuídas pelo mapa `registry/workspace-skill-routing.json`. A presença no mapa indica que o papel pode usá-la; o agente lê o `SKILL.md` completo quando a tarefa corresponder à descrição e o runtime realmente oferecer a skill.

| Papel | Responsabilidade | Skills extras típicas |
| --- | --- | --- |
| CEO | Estratégia, opções e prioridades | Nenhuma skill visual por padrão; usa requisitos e planejamento da biblioteca. |
| Product Manager | Jornada, escopo e aceitação | `prototype`, somente por invocação explícita. |
| Designer | Identidade, experiência, protótipo e motion planejado | `brandkit`, `design-taste-frontend`, `imagegen-frontend-*`, `apple-design`, `improve-animations`, direções visuais. |
| Frontend | Implementação e verificação de UI | `image-to-code`, `animate`, `animation-performance`, `mobile-native`, `break-ui`, bibliotecas de UI e direção visual pertinente. |
| Developer | Implementação geral e plataformas | `write-swift`, `animate-expo`, `ask-sonner`, `mobile-native`. |
| Architect | Decisões técnicas | `pick-ui-library` apenas quando invocada. |
| QA e Reviewer | Testes e avaliação independente | `break-ui`, `review-animations`; reviewer também pode revisar Swift. |
| Backend e Data | Implementação especializada | `full-output-enforcement` quando saída exaustiva for realmente necessária. |

O mapa JSON contém a atribuição completa por nome. Algumas skills aparecem em mais de um papel porque concepção, implementação e revisão são trabalhos diferentes. `design-taste-frontend-v1` e `design-taste-frontend-v2-experimental` ficam somente para compatibilidade explicitamente solicitada. `pick-ui-library` e `prototype` requerem invocação explícita. Skills pessoais não são copiadas por `sync`; um projeto em outra máquina precisa instalá-las separadamente.

Os novos papéis `global-ceo`, `global-product-manager` e `global-designer` são instalados pelos perfis pertinentes. O orquestrador mantém o limite de três especialistas simultâneos e só chama cada papel quando a tarefa justifica. CEO e Product Manager não substituem a autoridade do usuário; Designer especifica experiência, enquanto Frontend implementa e valida no navegador.
