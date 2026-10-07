[CmdletBinding()]
param()
. (Join-Path $PSScriptRoot 'common.ps1')
$agents = @(Get-Catalog agents)
$skills = @(Get-Catalog skills)
$rules = @(Get-Catalog rules)
foreach ($catalog in @($agents, $skills, $rules)) {
    $seen = @{}
    foreach ($item in $catalog) {
        if ($seen.ContainsKey($item.id)) { throw "ID duplicado: $($item.id)" }
        $seen[$item.id] = $true
        $path = Resolve-Child $script:LibraryRoot $item.path
        Assert-NoLinks $path
        if (-not (Test-Path -LiteralPath $path)) { throw "Referencia inexistente: $($item.path)" }
        if ([string]::IsNullOrWhiteSpace($item.description)) { throw "Descricao ausente: $($item.id)" }
    }
}
$names = @{}
foreach ($skill in $skills) {
    $name = $skill.name
    if ($name -notmatch '^[a-z0-9]+(-[a-z0-9]+)*$' -or $name.Length -ge 64) { throw "Nome de skill invalido: $name" }
    if ($names.ContainsKey($name)) { throw "Nome de skill duplicado: $name" }
    $names[$name] = $true
    if ((Split-Path $skill.path -Leaf) -ne $name) { throw "Pasta difere do nome: $name" }
    $body = Read-Text (Resolve-Child $script:LibraryRoot ($skill.path + '/SKILL.md'))
    $front = [regex]::Match($body, '(?s)\A---\r?\n(.*?)\r?\n---\r?\n')
    if (-not $front.Success) { throw "Frontmatter ausente: $name" }
    $declared = [regex]::Match($front.Groups[1].Value, '(?m)^name:\s*([a-z0-9-]+)\s*$')
    $description = [regex]::Match($front.Groups[1].Value, '(?m)^description:\s*(\S[^\r\n]*)$')
    if (-not $declared.Success -or $declared.Groups[1].Value -ne $name -or -not $description.Success) { throw "Frontmatter invalido: $name" }
    if ($body -match '\bTODO\b|\[TODO\]|INSERT_HERE') { throw "Scaffold incompleto: $name" }
}
$diskSkills = @(Get-ChildItem -LiteralPath (Join-Path $script:LibraryRoot 'skills') -Recurse -Filter SKILL.md -File)
if ($diskSkills.Count -ne $skills.Count) { throw 'Skills no disco e registro divergem.' }
$external = @(Get-Catalog external-skills)
$agentNames = @{}
foreach ($agent in $agents) {
    $null = @(Get-Selected $skills $agent.preferredSkills)
    $null = @(Get-Selected $external $agent.externalReferences)
    if (-not (Test-Path -LiteralPath (Resolve-Child $script:LibraryRoot $agent.protocol))) { throw 'Protocolo ausente.' }
    if ($agent.name -notmatch '^global-[a-z0-9-]+$') { throw "Nome de agente invalido: $($agent.name)" }
    if ($agentNames.ContainsKey($agent.name)) { throw "Nome de agente duplicado: $($agent.name)" }
    $agentNames[$agent.name] = $true
    if ($agent.sandbox -notin @('read-only', 'workspace-write')) { throw "Sandbox invalido: $($agent.id)" }
}
$profiles = @(Get-ChildItem -LiteralPath (Join-Path $script:LibraryRoot 'profiles') -Filter '*.json' -File)
foreach ($file in $profiles) {
    $profile = Read-Json $file.FullName
    if ($profile.schemaVersion -ne 1 -or $profile.id -ne $file.BaseName) { throw "Perfil invalido: $($file.Name)" }
    foreach ($selection in @(@{catalog=$agents; ids=$profile.agents}, @{catalog=$skills; ids=$profile.skills}, @{catalog=$rules; ids=@($profile.rules) + @($profile.conditionalRules)})) {
        $ids = @($selection.ids)
        if (@($ids | Select-Object -Unique).Count -ne $ids.Count) { throw "Selecao duplicada: $($profile.id)" }
        $null = @(Get-Selected $selection.catalog $ids)
    }
    foreach ($role in @(Get-Selected $agents $profile.agents)) {
        foreach ($skillId in $role.preferredSkills) {
            if ($profile.skills -notcontains $skillId) { throw "Perfil $($profile.id) sem skill do agente: $skillId" }
        }
    }
    if ($profile.skills -notcontains 'global-persistent-memory') { throw 'Perfil sem memoria.' }
    if ($profile.agents -notcontains 'orchestrator') { throw "Perfil sem orquestrador: $($profile.id)" }
    if ($profile.maxConcurrentSpecialists -lt 1) { throw "Concorrencia invalida: $($profile.id)" }
}
$sources = Read-Json (Join-Path $script:LibraryRoot 'registry/sources.lock.json')
foreach ($source in $sources.sources) {
    if ($source.status -ne 'catalog-only') { throw 'Fonte externa promovida sem validador de importacao nesta versao.' }
}
if (@($sources.installedExternalSkills).Count -ne 0) { throw 'Importacoes externas ainda nao suportadas pelo validador.' }
foreach ($file in Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.ps1' -File) {
    $tokens = $null; $parseErrors = $null
    $null = [Management.Automation.Language.Parser]::ParseFile($file.FullName, [ref]$tokens, [ref]$parseErrors)
    if ($parseErrors.Count) { throw "Sintaxe invalida em $($file.Name): $($parseErrors.Message -join '; ')" }
}
Write-Output "OK: $($agents.Count) agentes, $($skills.Count) skills, $($rules.Count) regras, $($profiles.Count) perfis; scripts validos."
