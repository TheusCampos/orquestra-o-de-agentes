[CmdletBinding(SupportsShouldProcess)]
param([Parameter(Mandatory)][string]$ProjectPath, [string]$Profile = 'general')
. (Join-Path $PSScriptRoot 'common.ps1')
$null = & (Join-Path $PSScriptRoot 'validate.ps1')
$target = [IO.Path]::GetFullPath($ProjectPath)
Assert-NoLinks $target
if (Test-Path -LiteralPath $target -PathType Leaf) { throw 'Destino e um arquivo.' }
$profileData = Get-Profile $Profile
$agents = @(Get-Selected (Get-Catalog agents) $profileData.agents)
$skills = @(Get-Selected (Get-Catalog skills) $profileData.skills)
$rules = @(Get-Selected (Get-Catalog rules) (@($profileData.rules) + @($profileData.conditionalRules)))
$manifestPath = Resolve-Child $target '.agent-library/manifest.json'
Assert-NoLinks $manifestPath
$previous = $null
$oldHashes = @{}
if (Test-Path -LiteralPath $manifestPath) {
    $previous = Read-Json $manifestPath
    if ($previous.schemaVersion -ne 1) { throw 'Manifesto incompativel.' }
    if ($previous.profile -ne $Profile) { throw 'Troca de perfil exige instalacao em destino novo nesta versao.' }
    foreach ($entry in $previous.files) {
        $null = Resolve-Child $target $entry.path
        if ($oldHashes.ContainsKey($entry.path)) { throw 'Manifesto contem caminhos duplicados.' }
        $oldHashes[$entry.path] = $entry.hash
    }
}
$desired = [ordered]@{}
function Add-Source([string]$Relative) {
    $desired[".agent-library/$Relative"] = Read-Text (Resolve-Child $script:LibraryRoot $Relative)
}
$protocol = Read-Text (Join-Path $script:LibraryRoot 'agents/protocol.md')
Add-Source 'agents/protocol.md'
Add-Source 'scripts/common.ps1'
Add-Source 'scripts/memory.ps1'
foreach ($agent in $agents) {
    Add-Source $agent.path
    $body = Read-Text (Resolve-Child $script:LibraryRoot $agent.path)
    $instructions = $protocol + $script:NL + $body + $script:NL + 'Leia .agent-library/profiles/active.json e as regras/skills pertinentes ao escopo. Respeite instrucoes locais e limites da sessao.'
    $desired[".codex/agents/$($agent.name).toml"] = @(
        ('name = ' + (Convert-ToTomlLiteral $agent.name)),
        ('description = ' + (Convert-ToTomlLiteral $agent.description)),
        ('sandbox_mode = ' + (Convert-ToTomlLiteral $agent.sandbox)),
        ('developer_instructions = ' + (Convert-ToTomlLiteral $instructions))
    ) -join $script:NL
    $desired[".codex/agents/$($agent.name).toml"] += $script:NL
}
foreach ($skill in $skills) {
    $folder = Resolve-Child $script:LibraryRoot $skill.path
    foreach ($file in Get-ChildItem -LiteralPath $folder -Recurse -File -Force) {
        Assert-NoLinks $file.FullName
        $relative = $file.FullName.Substring($folder.Length + 1).Replace('\', '/')
        # Recursos desta versao sao textuais. Binarios exigem ampliar o adaptador.
        $desired[".agents/skills/$($skill.name)/$relative"] = Read-Text $file.FullName
        $desired[".agent-library/$($skill.path)/$relative"] = Read-Text $file.FullName
    }
}
foreach ($rule in $rules) { Add-Source $rule.path }
foreach ($folderName in @('workflows', 'templates')) {
    foreach ($file in Get-ChildItem -LiteralPath (Join-Path $script:LibraryRoot $folderName) -File) { Add-Source "$folderName/$($file.Name)" }
}
$desired['.agent-library/profiles/active.json'] = ($profileData | ConvertTo-Json -Depth 20) + $script:NL
$desired['.agent-library/registry/agents.json'] = (ConvertTo-Json -InputObject @($agents) -Depth 20) + $script:NL
$desired['.agent-library/registry/skills.json'] = (ConvertTo-Json -InputObject @($skills) -Depth 20) + $script:NL
$desired['.agent-library/registry/rules.json'] = (ConvertTo-Json -InputObject @($rules) -Depth 20) + $script:NL
Add-Source 'registry/sources.lock.json'
Add-Source 'registry/external-skills.json'
Add-Source 'VERSION'
$configRelative = '.codex/config.toml'
$configPath = Resolve-Child $target $configRelative
if (-not (Test-Path -LiteralPath $configPath) -or $oldHashes.ContainsKey($configRelative)) {
    $desired[$configRelative] = Read-Text (Join-Path $script:LibraryRoot 'adapters/codex/templates/config.toml')
}
foreach ($old in $oldHashes.Keys) {
    if (-not $desired.Contains($old)) { throw "Componente antigo ausente na nova versao: $old. Remocao requer reconciliacao manual." }
}
# Verifique TODOS os conflitos antes de criar pastas.
foreach ($relative in $desired.Keys) {
    $path = Resolve-Child $target $relative
    Assert-NoLinks $path
    if (Test-Path -LiteralPath $path -PathType Container) { throw "Destino de arquivo e pasta: $relative" }
    if (Test-Path -LiteralPath $path -PathType Leaf) {
        $currentHash = Get-ByteHash ([IO.File]::ReadAllBytes($path))
        if ($oldHashes.ContainsKey($relative)) {
            if ($currentHash -ne $oldHashes[$relative]) { throw "Arquivo gerenciado alterado localmente: $relative" }
        } elseif ($currentHash -ne (Get-TextHash $desired[$relative])) { throw "Colisao com arquivo nao gerenciado: $relative" }
    }
}
$begin = '<!-- agent-library:begin -->'
$end = '<!-- agent-library:end -->'
$block = (@(
    $begin,
    '# Desenvolvimento com a biblioteca global',
    'Atue como orquestrador seguindo .agent-library/agents/orchestrator.md.',
    'No inicio de cada sessao, leia BRAIN.md na raiz do projeto; recupere historico por .agent-library/scripts/memory.ps1 -Action Read -ProjectPath . quando necessario.',
    'Registre decisoes, acoes comprovadas e checkpoint via memory.ps1. Em paralelo, somente o orquestrador escreve; especialistas retornam deltas.',
    'Leia .agent-library/profiles/active.json e PROJECT_CONTEXT.md do projeto quando existir.',
    'Regras essenciais: .agent-library/rules/core/engineering.md, .agent-library/rules/core/quality.md e .agent-library/rules/execution/permissions.md.',
    'Consulte .agent-library/registry para selecionar apenas skills e regras aplicaveis.',
    'Delegue explicitamente partes independentes de tarefas complexas aos especialistas global-* disponiveis; sem ferramentas de subagentes, execute os papeis sequencialmente.',
    'Respeite instrucoes locais mais especificas, autorizacao do usuario e limites efetivos da sessao.',
    $end
) -join $script:NL)
$agentsPath = Resolve-Child $target 'AGENTS.md'
Assert-NoLinks $agentsPath
if (Test-Path -LiteralPath $agentsPath -PathType Container) { throw 'AGENTS.md e uma pasta.' }
$existing = if (Test-Path -LiteralPath $agentsPath) { Read-Text $agentsPath } else { '' }
$beginCount = [regex]::Matches($existing, [regex]::Escape($begin)).Count
$endCount = [regex]::Matches($existing, [regex]::Escape($end)).Count
if ($beginCount -ne $endCount -or $beginCount -gt 1) { throw 'Marcadores invalidos em AGENTS.md.' }
$match = [regex]::Match($existing, '(?s)' + [regex]::Escape($begin) + '.*?' + [regex]::Escape($end))
if ($beginCount -eq 1 -and -not $match.Success) { throw 'Ordem dos marcadores invalida.' }
if ($match.Success) {
    if (-not $previous) { throw 'Bloco de biblioteca sem manifesto; reconciliar antes de instalar.' }
    if ((Get-TextHash $match.Value) -ne $previous.agentsBlockHash) { throw 'Bloco gerenciado de AGENTS.md alterado localmente.' }
    $newAgents = $existing.Substring(0, $match.Index) + $block + $existing.Substring($match.Index + $match.Length)
} else {
    if ($previous) { throw 'Bloco gerenciado removido de AGENTS.md.' }
    $separator = if ($existing.Length -and -not $existing.EndsWith($script:NL)) { $script:NL + $script:NL } elseif ($existing.Length) { $script:NL } else { '' }
    $newAgents = $existing + $separator + $block + $script:NL
}
$hashes = @()
foreach ($relative in $desired.Keys) { $hashes += @{path=$relative; hash=(Get-TextHash $desired[$relative])} }
$manifest = @{
    schemaVersion=1; libraryVersion=(Read-Text (Join-Path $script:LibraryRoot 'VERSION')).Trim()
    profile=$Profile; files=$hashes; agentsBlockHash=(Get-TextHash $block)
}
$brainPath = Resolve-Child $target 'BRAIN.md'
Assert-NoLinks $brainPath
if (Test-Path -LiteralPath $brainPath -PathType Container) { throw 'BRAIN.md e uma pasta.' }
# Memoria e propriedade do projeto: inicializar somente se ausente e nao incluir nos hashes gerenciados.
if (-not (Test-Path -LiteralPath $brainPath)) { $desired['BRAIN.md'] = Read-Text (Join-Path $script:LibraryRoot 'templates/brain.md') }
$desired['AGENTS.md'] = $newAgents
$desired['.agent-library/manifest.json'] = ($manifest | ConvertTo-Json -Depth 20) + $script:NL
$changed = @($desired.Keys | Where-Object {
    $p = Resolve-Child $target $_
    -not (Test-Path -LiteralPath $p) -or (Get-ByteHash ([IO.File]::ReadAllBytes($p))) -ne (Get-TextHash $desired[$_])
})
if ($changed.Count -eq 0) { Write-Output "Sem alteracoes: $target ($Profile)."; return }
if (-not $PSCmdlet.ShouldProcess($target, "Sincronizar perfil $Profile ($($changed.Count) arquivos)")) { return }
$originals = @{}
$written = New-Object 'System.Collections.Generic.List[string]'
try {
    foreach ($relative in $changed) {
        $path = Resolve-Child $target $relative
        $originals[$relative] = if (Test-Path -LiteralPath $path) { [IO.File]::ReadAllBytes($path) } else { $null }
        $null = [IO.Directory]::CreateDirectory((Split-Path $path -Parent))
        $written.Add($relative)
        [IO.File]::WriteAllText($path, $desired[$relative], $script:Utf8)
    }
} catch {
    $failure = $_
    foreach ($relative in $written) {
        $path = Resolve-Child $target $relative
        if ($null -ne $originals[$relative]) { [IO.File]::WriteAllBytes($path, $originals[$relative]) }
        elseif (Test-Path -LiteralPath $path -PathType Leaf) { Remove-Item -LiteralPath $path -Force }
    }
    throw $failure
}
Write-Output "Sincronizado: $target; perfil=$Profile; arquivos alterados=$($changed.Count)."
Write-Output 'Abra nova sessao Codex no projeto para conferir descoberta. Configuracao preexistente foi preservada.'
