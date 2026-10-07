---
name: global-library-maintenance
description: Criar ou atualizar agentes, skills, regras e perfis desta biblioteca reutilizável.
---

# global-library-maintenance

Identifique uma necessidade recorrente ou requisito explícito. Prefira atualizar o componente responsável a duplicar instruções.
Skills exigem name e description precisos e pasta com mesmo nome. Registre no catálogo e nos perfis pertinentes.
Mantenha recursos condicionais separados e referenciados; não crie scaffolds vazios.
Fontes externas: revisar SKILL.md e scripts, licença, dependências, destinos de escrita e rede. Fixar commit e hashes antes de promover a instalado.
Atualize VERSION quando publicar uma versão da biblioteca; registre compatibilidade e evidências.
Execute validate.ps1. Mudanças de sincronização exigem test-integration.ps1.
Use cenários em evaluations/scenarios para validar comportamento com sessão real; não marque cenários como aprovados sem executá-los.
