[CmdletBinding()]
param()
. (Join-Path $PSScriptRoot 'common.ps1')
$testRoot = Resolve-Child $script:LibraryRoot ('.work/memory-' + [guid]::NewGuid().ToString('N'))
$memory = Join-Path $PSScriptRoot 'memory.ps1'
function Assert-True([bool]$Condition,[string]$Message) { if (-not $Condition) { throw "TEST FAIL: $Message" } }
function Expect-Failure([scriptblock]$Action,[string]$Pattern) {
    $failed = $false
    try { & $Action | Out-Null } catch {
        $failed = $true
        if ($_.Exception.Message -notmatch $Pattern) { throw "Falha inesperada: $($_.Exception.Message)" }
    }
    Assert-True $failed "Esperava falha: $Pattern"
}
& $memory -Action Init -ProjectPath $testRoot -WhatIf
Assert-True (-not (Test-Path -LiteralPath $testRoot)) 'Preview escreveu memoria.'
Expect-Failure { & $memory -Action Read -ProjectPath $testRoot } 'ausente'
Assert-True (-not (Test-Path -LiteralPath $testRoot)) 'Leitura criou arquivo.'
& $memory -Action Init -ProjectPath $testRoot | Out-Null
$brainPath = Join-Path $testRoot 'BRAIN.md'
$eventsPath = Join-Path $testRoot 'memory/events.jsonl'
[IO.File]::AppendAllText($brainPath, $script:NL + 'Preferencia curada: preservar meus dados.', $script:Utf8)
& $memory -Action Record -ProjectPath $testRoot -Kind decision -Id decision-1 -Content 'Manter a stack existente.' -Evidence 'Pedido do usuario.' | Out-Null
$before = Read-Text $eventsPath
& $memory -Action Record -ProjectPath $testRoot -Kind decision -Id decision-1 -Content 'Manter a stack existente.' -Evidence 'Pedido do usuario.' | Out-Null
Assert-True ((Read-Text $eventsPath) -eq $before) 'ID identico duplicou evento.'
Expect-Failure { & $memory -Action Record -ProjectPath $testRoot -Kind decision -Id decision-1 -Content 'Conteudo diferente.' } 'conteudo diferente'
Expect-Failure { & $memory -Action Record -ProjectPath $testRoot -Kind action -Content 'Teste passou.' -Confidence confirmed } 'exige Evidence'
Expect-Failure { & $memory -Action Record -ProjectPath $testRoot -Kind correction -Content 'Correcao.' } 'exige Supersedes'
Expect-Failure { & $memory -Action Record -ProjectPath $testRoot -Kind correction -Supersedes missing -Content 'Correcao.' } 'evento existente'
Assert-True ((Read-Text $eventsPath) -eq $before) 'Registro invalido alterou historico.'
& $memory -Action Record -ProjectPath $testRoot -Kind correction -Id correction-1 -Supersedes decision-1 -Content 'A stack pode ser ajustada conforme pedido atual.' -Evidence 'Nova decisao do usuario.' | Out-Null
Assert-True ((Read-Text $brainPath).Contains('decision-1 | decision | substituido')) 'Correcao nao marcou original.'
Assert-True ((Read-Text $brainPath).Contains('Preferencia curada: preservar meus dados.')) 'Resumo curado foi sobrescrito.'
& $memory -Action Record -ProjectPath $testRoot -Kind checkpoint -Id markers -Content '<!-- memory:end --> texto de teste' | Out-Null
& $memory -Action Record -ProjectPath $testRoot -Kind checkpoint -Id after-markers -Content 'Continuidade preservada.' | Out-Null
$parsed = & $memory -Action Read -ProjectPath $testRoot -Search 'stack' | ConvertFrom-Json
Assert-True (@($parsed.events).Count -eq 2) 'Busca nao recuperou contexto.'
# Historico valido sem quebra final deve aceitar registro sem concatenar JSON.
[IO.File]::WriteAllText($eventsPath, (Read-Text $eventsPath).TrimEnd([char]10,[char]13), $script:Utf8)
& $memory -Action Record -ProjectPath $testRoot -Kind action -Id action-1 -Confidence confirmed -Content 'Verificacao executada.' -Evidence 'Teste local descartavel.' | Out-Null
$parsed = & $memory -Action Read -ProjectPath $testRoot | ConvertFrom-Json
Assert-True (@($parsed.events).Count -eq 5) 'Eventos foram perdidos ao recompor quebra final.'
& $memory -Action Record -ProjectPath $testRoot -Kind decision -Id old-framework -Content 'Escolher React.' | Out-Null
& $memory -Action Record -ProjectPath $testRoot -Kind correction -Id new-framework -Supersedes old-framework -Content 'Escolher Vue.' | Out-Null
$found = & $memory -Action Read -ProjectPath $testRoot -Search 'React' | ConvertFrom-Json
Assert-True (@($found.events).Count -eq 2) 'Busca omitiu correcao com texto diferente.'
Assert-True ($found.events[0].effectiveState -eq 'superseded') 'Busca retornou fato substituido como vigente.'
# Outro escritor possui a trava: tentativa falha sem sobrescrever.
$lockPath = Join-Path $testRoot 'memory/.writer.lock'
$held = [IO.File]::Open($lockPath,[IO.FileMode]::Open,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
try { Expect-Failure { & $memory -Action Record -ProjectPath $testRoot -Content 'Nao escrever.' } 'outro escritor' }
finally { $held.Dispose() }
$held = [IO.File]::Open($lockPath,[IO.FileMode]::Open,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
try { Expect-Failure { & $memory -Action Read -ProjectPath $testRoot } 'outro escritor' }
finally { $held.Dispose() }
# Decisoes e checkpoint continuam recuperaveis fora da janela recente.
& $memory -Action Record -ProjectPath $testRoot -Kind checkpoint -Id resume-point -Content 'Retomar validacao visual, pendente.' | Out-Null
& $memory -Action Record -ProjectPath $testRoot -Kind correction -Id resume-corrected -Supersedes resume-point -Content 'Retomar mobile antes de desktop.' | Out-Null
foreach ($number in 1..22) {
    & $memory -Action Record -ProjectPath $testRoot -Kind action -Id ('later-' + $number) -Content 'Evento posterior.' | Out-Null
}
$snapshot = & $memory -Action Read -ProjectPath $testRoot -Limit 1 | ConvertFrom-Json
Assert-True ($snapshot.checkpoint.id -eq 'resume-corrected') 'Checkpoint corrigido sumiu da janela curta.'
Assert-True (@($snapshot.decisions | Where-Object id -eq 'new-framework').Count -eq 1) 'Decisao corrigida sumiu da janela curta.'
Assert-True ((Read-Text $brainPath).Contains('[new-framework]')) 'Resumo perdeu decisao corrigida.'
Assert-True ((Read-Text $brainPath).Contains('## Checkpoint atual')) 'Resumo nao fixa checkpoint.'
Assert-True (@($snapshot.decisions | Where-Object id -eq 'old-framework').Count -eq 0) 'Decisao substituida ainda ativa.'
# UTF-8 e multiline persistem; backup recupera texto curado e journal atual.
& $memory -Action Record -ProjectPath $testRoot -Kind decision -Id unicode-decision -Content "Animação e comunicação.`nSegunda linha." | Out-Null
& $memory -Action Record -ProjectPath $testRoot -Id after-unicode -Content 'Preservar backup com decisao.' | Out-Null
$snapshot = & $memory -Action Read -ProjectPath $testRoot -Limit 1 | ConvertFrom-Json
Assert-True ($snapshot.decisions[-1].content -ceq "Animação e comunicação.`nSegunda linha.") 'UTF-8/multiline alterados.'
$durableHistory = Read-Text $eventsPath
[IO.File]::WriteAllText($brainPath,'Resumo interrompido.', $script:Utf8)
Expect-Failure { & $memory -Action Read -ProjectPath $testRoot } 'marcadores'
& $memory -Action Recover -ProjectPath $testRoot | Out-Null
Assert-True ((Read-Text $brainPath).Contains('Preferencia curada: preservar meus dados.')) 'Backup perdeu texto curado.'
Assert-True ((Read-Text $brainPath).Contains('after-unicode')) 'Recuperacao nao refez journal mais recente.'
Assert-True ((Read-Text $eventsPath) -ceq $durableHistory) 'Recover alterou eventos.'
Assert-True (@(Get-ChildItem -LiteralPath $testRoot -Recurse -Filter '*.tmp').Count -eq 0) 'Temporarios abandonados em operacao normal.'
$brainBeforeMissing = Read-Text $brainPath
[IO.File]::WriteAllText($eventsPath, '', $script:Utf8)
Expect-Failure { & $memory -Action Read -ProjectPath $testRoot } 'Journal ausente ou vazio'
Expect-Failure { & $memory -Action Record -ProjectPath $testRoot -Content 'Nao apagar resumo sem historico.' } 'Journal ausente ou vazio'
Assert-True ((Read-Text $brainPath) -ceq $brainBeforeMissing) 'Journal perdido apagou resumo.'
[IO.File]::WriteAllText($eventsPath, $durableHistory, $script:Utf8)
$brainBefore = Read-Text $brainPath
[IO.File]::AppendAllText($eventsPath, 'invalid-json' + $script:NL, $script:Utf8)
Expect-Failure { & $memory -Action Record -ProjectPath $testRoot -Content 'Nao escrever em historico corrompido.' } 'Historico JSON invalido'
Assert-True ((Read-Text $brainPath) -eq $brainBefore) 'Corrupcao alterou resumo.'
Write-Output "OK: recuperacao de backup, checkpoint duravel, UTF-8, preservacao, busca, idempotencia, correcao, evidencias, trava de leitura/escrita, marcadores e corrupcao. Artefatos: $testRoot"

