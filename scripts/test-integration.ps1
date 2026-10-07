[CmdletBinding()]
param()
. (Join-Path $PSScriptRoot 'common.ps1')
$testRoot = Resolve-Child $script:LibraryRoot ('.work/integration-' + [guid]::NewGuid().ToString('N'))
$null = [IO.Directory]::CreateDirectory($testRoot)
function Assert-True([bool]$Condition, [string]$Message) { if (-not $Condition) { throw "TEST FAIL: $Message" } }
function Expect-Failure([scriptblock]$Action, [string]$Pattern) {
    $failed = $false
    try { & $Action | Out-Null } catch {
        $failed = $true
        if ($_.Exception.Message -notmatch $Pattern) { throw "Falha inesperada: $($_.Exception.Message)" }
    }
    Assert-True $failed "Esperava falha: $Pattern"
}
$sync = Join-Path $PSScriptRoot 'sync-project.ps1'
$preview = Join-Path $testRoot 'preview'
& (Join-Path $PSScriptRoot 'install.ps1') -ProjectPath $preview -Profile website -WhatIf
Assert-True (-not (Test-Path -LiteralPath $preview)) 'WhatIf escreveu no destino.'
$project = Join-Path $testRoot 'project'
$null = [IO.Directory]::CreateDirectory((Join-Path $project '.codex'))
$personal = 'Instrucao pessoal.' + [char]13 + [char]10
$configText = '# Config pessoal' + $script:NL
[IO.File]::WriteAllText((Join-Path $project 'AGENTS.md'), $personal, $script:Utf8)
[IO.File]::WriteAllText((Join-Path $project '.codex/config.toml'), $configText, $script:Utf8)
& $sync -ProjectPath $project -Profile website | Out-Null
$agentsPath = Join-Path $project 'AGENTS.md'
Assert-True (Test-Path -LiteralPath (Join-Path $project '.agents/skills/global-web-interface/references/motion-and-browser-qa.md')) 'Referencia de motion/QA nao instalada.'
Assert-True (Test-Path -LiteralPath (Join-Path $project '.agents/skills/global-web-interface/references/visual-direction.md')) 'Referencia de direcao visual nao instalada.'
Assert-True ((Read-Text $agentsPath).StartsWith($personal)) 'Instrucao pessoal perdida.'
Assert-True ((Read-Text (Join-Path $project '.codex/config.toml')) -eq $configText) 'Config pessoal alterada.'
$manifestPath = Join-Path $project '.agent-library/manifest.json'
$before = Read-Text $manifestPath
$brainPath = Join-Path $project 'BRAIN.md'
[IO.File]::AppendAllText($brainPath, $script:NL + 'Memoria pessoal que deve sobreviver.', $script:Utf8)
$brainBefore = Read-Text $brainPath
& $sync -ProjectPath $project -Profile website | Out-Null
Assert-True ((Read-Text $manifestPath) -eq $before) 'Sincronizacao nao idempotente.'
Assert-True ((Read-Text $brainPath) -eq $brainBefore) 'Memoria pessoal alterada na sincronizacao.'
[IO.File]::AppendAllText($agentsPath, $script:NL + 'Personalizacao adicional.' + $script:NL, $script:Utf8)
& $sync -ProjectPath $project -Profile website | Out-Null
Assert-True ((Read-Text $agentsPath).Contains('Personalizacao adicional.')) 'Conteudo externo ao bloco perdido.'
Expect-Failure { & $sync -ProjectPath $project -Profile api } 'Troca de perfil'
$skillPath = Join-Path $project '.agents/skills/global-testing/SKILL.md'
[IO.File]::AppendAllText($skillPath, $script:NL + 'Alteracao local.', $script:Utf8)
Expect-Failure { & $sync -ProjectPath $project -Profile website } 'alterado localmente'
Assert-True ((Read-Text $manifestPath) -eq $before) 'Conflito alterou manifesto.'
$collision = Join-Path $testRoot 'collision'
$null = [IO.Directory]::CreateDirectory((Join-Path $collision '.codex/agents'))
[IO.File]::WriteAllText((Join-Path $collision '.codex/agents/global-orchestrator.toml'), 'personal', $script:Utf8)
Expect-Failure { & $sync -ProjectPath $collision -Profile website } 'Colisao'
Assert-True (-not (Test-Path -LiteralPath (Join-Path $collision '.agent-library'))) 'Colisao gerou escrita parcial.'
$clean = Join-Path $testRoot 'clean'
& $sync -ProjectPath $clean -Profile fullstack | Out-Null
& (Join-Path $PSScriptRoot 'doctor.ps1') -ProjectPath $clean | Out-Null
Expect-Failure { Resolve-Child $clean '../escape' } 'fora do destino'
$malformed = Join-Path $testRoot 'malformed'
$null = [IO.Directory]::CreateDirectory($malformed)
[IO.File]::WriteAllText((Join-Path $malformed 'AGENTS.md'), '<!-- agent-library:end --><!-- agent-library:begin -->', $script:Utf8)
Expect-Failure { & $sync -ProjectPath $malformed -Profile general } 'Ordem'
# Atualizacao real a partir de uma copia isolada da biblioteca.
$fixture = Join-Path $testRoot 'library-fixture'
$null = [IO.Directory]::CreateDirectory($fixture)
foreach ($name in @('agents','skills','rules','profiles','registry','workflows','templates','adapters','scripts','VERSION')) {
    Copy-Item -LiteralPath (Join-Path $script:LibraryRoot $name) -Destination $fixture -Recurse
}
$agentRegistry = Join-Path $fixture 'registry/agents.json'
$originalRegistry = Read-Text $agentRegistry
$fixtureAgents = @(foreach ($entry in (Read-Json $agentRegistry)) { $entry })
$fixtureAgents[1].name = $fixtureAgents[0].name
[IO.File]::WriteAllText($agentRegistry, (ConvertTo-Json -InputObject $fixtureAgents -Depth 20), $script:Utf8)
Expect-Failure { & (Join-Path $fixture 'scripts/validate.ps1') } 'Nome de agente duplicado'
[IO.File]::WriteAllText($agentRegistry, $originalRegistry, $script:Utf8)
[IO.File]::AppendAllText((Join-Path $fixture 'rules/core/quality.md'), $script:NL + 'Regra adicional da versao de teste.', $script:Utf8)
[IO.File]::WriteAllText((Join-Path $fixture 'VERSION'), '0.2.1' + $script:NL, $script:Utf8)
$cleanBrainPath = Join-Path $clean 'BRAIN.md'
[IO.File]::AppendAllText($cleanBrainPath, $script:NL + 'Historico preservado na atualizacao.', $script:Utf8)
$cleanBrainBefore = Read-Text $cleanBrainPath
$fixtureSync = Join-Path $fixture 'scripts/sync-project.ps1'
& $fixtureSync -ProjectPath $clean -Profile fullstack | Out-Null
Assert-True ((Read-Json (Join-Path $clean '.agent-library/manifest.json')).libraryVersion -eq '0.2.1') 'Versao nao atualizada.'
Assert-True ((Read-Text $cleanBrainPath) -eq $cleanBrainBefore) 'Atualizacao sobrescreveu memoria.'
& (Join-Path $clean '.agent-library/scripts/memory.ps1') -Action Record -ProjectPath $clean -Kind checkpoint -Id integration-checkpoint -Content 'Checkpoint no projeto instalado.' | Out-Null
Assert-True (Test-Path -LiteralPath (Join-Path $clean 'memory/events.jsonl')) 'Script instalado nao registrou memoria.'
Assert-True ((Read-Text (Join-Path $clean '.agent-library/rules/core/quality.md')).Contains('Regra adicional da versao de teste.')) 'Regra nao atualizada.'
& (Join-Path $fixture 'scripts/doctor.ps1') -ProjectPath $clean | Out-Null
foreach ($profileFile in Get-ChildItem -LiteralPath (Join-Path $script:LibraryRoot 'profiles') -Filter '*.json') {
    $destination = Join-Path $testRoot ('profile-' + $profileFile.BaseName)
    & (Join-Path $PSScriptRoot 'install.ps1') -ProjectPath $destination -Profile $profileFile.BaseName | Out-Null
    & (Join-Path $PSScriptRoot 'doctor.ps1') -ProjectPath $destination | Out-Null
}
Write-Output "OK: atualizacao e todos os perfis; preview, instalacao, preservacao, idempotencia, conflitos, perfil, integridade e confinamento. Artefatos: $testRoot"
