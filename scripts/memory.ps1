[CmdletBinding(SupportsShouldProcess)]
param(
    [ValidateSet('Init','Read','Record','Recover')][string]$Action = 'Read',
    [string]$ProjectPath = '.',
    [ValidateSet('request','decision','action','checkpoint','correction')][string]$Kind = 'checkpoint',
    [ValidatePattern('^[a-zA-Z0-9_.-]{1,100}$')][string]$Actor = 'orchestrator',
    [string]$Content,
    [string]$Evidence = '',
    [ValidateSet('confirmed','reported','hypothesis')][string]$Confidence = 'reported',
    [ValidatePattern('^[a-zA-Z0-9_.-]{1,100}$')][string]$Id,
    [string]$Supersedes = '',
    [string]$Search = '',
    [ValidateRange(1,200)][int]$Limit = 20
)
. (Join-Path $PSScriptRoot 'common.ps1')
$root = [IO.Path]::GetFullPath($ProjectPath)
Assert-NoLinks $root
if (Test-Path -LiteralPath $root -PathType Leaf) { throw 'Projeto e um arquivo.' }
$brainPath = Resolve-Child $root 'BRAIN.md'
$eventsPath = Resolve-Child $root 'memory/events.jsonl'
$lockPath = Resolve-Child $root 'memory/.writer.lock'
$backupPath = Resolve-Child $root 'memory/BRAIN.previous.md'
foreach ($p in @($brainPath,$eventsPath,$lockPath,$backupPath)) {
    Assert-NoLinks $p
    if (Test-Path -LiteralPath $p -PathType Container) { throw "Arquivo de memoria e pasta: $p" }
}
function Write-Atomic([string]$Path, [string]$Text, [string]$Backup = '') {
    $temporary = $Path + '.' + [guid]::NewGuid().ToString('N') + '.tmp'
    try {
        $bytes = $script:Utf8.GetBytes($Text)
        $stream = [IO.File]::Open($temporary,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
        try { $stream.Write($bytes,0,$bytes.Length); $stream.Flush($true) } finally { $stream.Dispose() }
        if (Test-Path -LiteralPath $Path) {
            $backupArgument = if ($Backup) { $Backup } else { [System.Management.Automation.Language.NullString]::Value }
            for ($attempt = 1; $attempt -le 3; $attempt++) {
                try { [IO.File]::Replace($temporary,$Path,$backupArgument); break }
                catch [IO.IOException] {
                    if ($attempt -eq 3 -or -not (Test-Path -LiteralPath $temporary)) { throw }
                    Start-Sleep -Milliseconds 100
                }
            }
        } else { [IO.File]::Move($temporary,$Path) }
    } finally {
        if (Test-Path -LiteralPath $temporary) { Remove-Item -LiteralPath $temporary -Force }
    }
}
function Read-History {
    if (-not (Test-Path -LiteralPath $eventsPath)) { return }
    $ids = @{}
    foreach ($line in [IO.File]::ReadAllLines($eventsPath, $script:Utf8)) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        try { $event = $line | ConvertFrom-Json } catch { throw 'Historico JSON invalido; preservar arquivo e reparar antes de registrar.' }
        foreach ($name in @('schemaVersion','id','timestampUtc','actor','kind','content','evidence','confidence','supersedes')) {
            if ($event.PSObject.Properties.Name -notcontains $name) { throw "Evento sem campo: $name" }
        }
        if ($event.schemaVersion -ne 1 -or $event.id -notmatch '^[a-zA-Z0-9_.-]{1,100}$') { throw 'Evento incompativel.' }
        if ($ids.ContainsKey($event.id)) { throw 'Historico possui IDs duplicados.' }
        if ($event.kind -notin @('request','decision','action','checkpoint','correction') -or $event.confidence -notin @('confirmed','reported','hypothesis')) { throw 'Tipo ou confianca de evento invalido.' }
        if ($event.supersedes -and -not $ids.ContainsKey($event.supersedes)) { throw 'Supersedes deve apontar para evento anterior existente.' }
        $ids[$event.id] = $true
        Write-Output $event
    }
}
function Get-MemoryBlock([string]$Text) {
    $begin = '<!-- memory:begin -->'; $end = '<!-- memory:end -->'
    if ([regex]::Matches($Text,[regex]::Escape($begin)).Count -ne 1 -or [regex]::Matches($Text,[regex]::Escape($end)).Count -ne 1) {
        throw 'BRAIN.md precisa de um par de marcadores memory:begin/end.'
    }
    $match = [regex]::Match($Text,'(?s)' + [regex]::Escape($begin) + '.*?' + [regex]::Escape($end))
    if (-not $match.Success) { throw 'Marcadores de memoria fora de ordem.' }
    $match
}
function Set-EffectiveKinds($History) {
    $byId = @{}
    foreach ($event in $History) { $byId[$event.id] = $event }
    foreach ($event in $History) {
        $origin = $event
        while ($origin.kind -eq 'correction' -and $origin.supersedes) { $origin = $byId[$origin.supersedes] }
        $event | Add-Member -NotePropertyName effectiveKind -NotePropertyValue $origin.kind -Force
    }
}
function Assert-HistoryPresent([string]$Brain, $History) {
    $block = Get-MemoryBlock $Brain
    if (@($History).Count -eq 0 -and $block.Value -match '(?m)^### [a-zA-Z0-9_.-]+ \|') {
        throw 'Journal ausente ou vazio para BRAIN.md com eventos; preservar resumo e restaurar historico antes de registrar.'
    }
}
if ($Action -eq 'Read') {
    $readLock = $null
    try {
    if (Test-Path -LiteralPath $lockPath) {
        try { $readLock = [IO.File]::Open($lockPath,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::Read) }
        catch { throw 'Memoria em uso por outro escritor ou trava inacessivel; tente novamente apos o escritor concluir.' }
    }
    if (-not (Test-Path -LiteralPath $brainPath -PathType Leaf)) { throw 'BRAIN.md ausente; use -Action Init.' }
    $brain = Read-Text $brainPath
    $null = Get-MemoryBlock $brain
    $history = @(Read-History)
    Assert-HistoryPresent $brain $history
    $allEvents = @($history)
    Set-EffectiveKinds $allEvents
    $supersededBy = @{}
    foreach ($event in $allEvents) {
        if ($event.supersedes) {
            if (-not $supersededBy.ContainsKey($event.supersedes)) { $supersededBy[$event.supersedes] = @() }
            $supersededBy[$event.supersedes] += $event.id
        }
    }
    if ($Search) {
        $selectedIds = @{}
        foreach ($event in $allEvents) {
            if (($event.content + ' ' + $event.evidence + ' ' + $event.id).IndexOf($Search,[StringComparison]::OrdinalIgnoreCase) -ge 0) {
                $selectedIds[$event.id] = $true
            }
        }
        # Inclua correcoes mesmo quando o texto novo nao contem o termo pesquisado.
        do {
            $added = $false
            foreach ($event in $allEvents) {
                if ($event.supersedes -and $selectedIds.ContainsKey($event.supersedes) -and -not $selectedIds.ContainsKey($event.id)) {
                    $selectedIds[$event.id] = $true
                    $added = $true
                }
            }
        } while ($added)
        $history = @($allEvents | Where-Object { $selectedIds.ContainsKey($_.id) })
    }
    foreach ($event in $history) {
        $state = if ($supersededBy.ContainsKey($event.id)) { 'superseded' } else { $event.confidence }
        $replacements = if ($supersededBy.ContainsKey($event.id)) { @($supersededBy[$event.id]) } else { @() }
        $event | Add-Member -NotePropertyName effectiveState -NotePropertyValue $state -Force
        $event | Add-Member -NotePropertyName supersededBy -NotePropertyValue $replacements -Force
    }
    $active = @($allEvents | Where-Object { -not $supersededBy.ContainsKey($_.id) })
    [ordered]@{brain=$brain; checkpoint=($active | Where-Object effectiveKind -eq 'checkpoint' | Select-Object -Last 1); decisions=@($active | Where-Object effectiveKind -eq 'decision'); events=@($history | Select-Object -Last $Limit)} | ConvertTo-Json -Depth 12
    } finally { if ($readLock) { $readLock.Dispose() } }
    return
}
if ($Action -eq 'Record') {
    if ([string]::IsNullOrWhiteSpace($Content)) { throw 'Content obrigatorio para Record.' }
    if ($Content.Length -gt 16384 -or $Evidence.Length -gt 2048) { throw 'Registro muito grande; resuma antes de registrar.' }
    if ($Kind -eq 'action' -and $Confidence -eq 'confirmed' -and [string]::IsNullOrWhiteSpace($Evidence)) { throw 'Acao confirmada exige Evidence.' }
    if ($Kind -eq 'correction' -and -not $Supersedes) { throw 'Correction exige Supersedes.' }
    if (-not $Id) { $Id = [guid]::NewGuid().ToString('N') }
}
if (-not $PSCmdlet.ShouldProcess($root, "Memoria: $Action")) { return }
$null = [IO.Directory]::CreateDirectory((Split-Path $eventsPath -Parent))
$lock = $null
try {
    try { $lock = [IO.File]::Open($lockPath, [IO.FileMode]::OpenOrCreate, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None) }
    catch { throw 'Memoria em uso por outro escritor ou trava inacessivel; tente novamente apos o escritor concluir.' }
    if ($Action -eq 'Recover') {
        if (-not (Test-Path -LiteralPath $backupPath -PathType Leaf)) { throw 'Backup de BRAIN.md ausente; preservar arquivos e reparar manualmente.' }
        $brain = Read-Text $backupPath
    } else {
        $brain = if (Test-Path -LiteralPath $brainPath) { Read-Text $brainPath } else { Read-Text (Join-Path $script:LibraryRoot 'templates/brain.md') }
    }
    $match = Get-MemoryBlock $brain
    $history = @(Read-History)
    Assert-HistoryPresent $brain $history
    $seen = @{}
    foreach ($event in $history) {
        if ($seen.ContainsKey($event.id)) { throw 'Historico possui IDs duplicados.' }
        $seen[$event.id] = $event
    }
    if ($Action -eq 'Record') {
        if ($Supersedes -and -not $seen.ContainsKey($Supersedes)) { throw 'Supersedes deve apontar para evento existente.' }
        if ($Supersedes -eq $Id) { throw 'Evento nao pode substituir a si mesmo.' }
        if ($seen.ContainsKey($Id)) {
            $old = $seen[$Id]
            if ($old.kind -ne $Kind -or $old.actor -ne $Actor -or $old.content -cne $Content -or $old.evidence -cne $Evidence -or $old.confidence -ne $Confidence -or $old.supersedes -ne $Supersedes) {
                throw 'ID existente com conteudo diferente.'
            }
            Write-Output "Evento ja registrado: $Id"
        } else {
            $event = [ordered]@{
                schemaVersion=1; id=$Id; timestampUtc=[DateTime]::UtcNow.ToString('o')
                actor=$Actor; kind=$Kind; content=$Content; evidence=$Evidence; confidence=$Confidence; supersedes=$Supersedes
            }
            $history += [pscustomobject]$event
            $serialized = (@($history | ForEach-Object { $_ | ConvertTo-Json -Depth 8 -Compress }) -join $script:NL) + $script:NL
            Write-Atomic $eventsPath $serialized
            Write-Output "Registrado: $Id"
        }
    }
    $superseded = @{}
    foreach ($event in $history) { if ($event.supersedes) { $superseded[$event.supersedes] = $true } }
    Set-EffectiveKinds $history
    $lines = New-Object 'System.Collections.Generic.List[string]'
    $lines.Add('<!-- memory:begin -->')
    $lines.Add('## Decisoes ativas (independentes da janela de eventos)')
    foreach ($event in @($history | Where-Object { $_.effectiveKind -eq 'decision' -and -not $superseded.ContainsKey($_.id) })) {
        $lines.Add("- [$($event.id)] $($event.confidence): " + $event.content.Replace('<!-- memory:', '&lt;!-- memory:').Replace("`n",' '))
    }
    $checkpoint = $history | Where-Object { $_.effectiveKind -eq 'checkpoint' -and -not $superseded.ContainsKey($_.id) } | Select-Object -Last 1
    if ($checkpoint) {
        $lines.Add('## Checkpoint atual')
        $lines.Add("[$($checkpoint.id)] " + $checkpoint.content.Replace('<!-- memory:', '&lt;!-- memory:'))
    }
    $lines.Add('## Eventos recentes (historico completo: memory/events.jsonl)')
    foreach ($event in @($history | Select-Object -Last 20)) {
        $state = if ($superseded.ContainsKey($event.id)) { 'substituido' } else { $event.confidence }
        $lines.Add('')
        $lines.Add("### $($event.id) | $($event.kind) | $state | $($event.actor)")
        $lines.Add("Data UTC: $($event.timestampUtc)")
        if ($event.supersedes) { $lines.Add("Substitui: $($event.supersedes)") }
        foreach ($line in ($event.content -split '\r?\n')) { $lines.Add('> ' + $line.Replace('<!-- memory:', '&lt;!-- memory:')) }
        if ($event.evidence) {
            foreach ($line in ($event.evidence -split '\r?\n')) { $lines.Add('> Fonte/evidencia: ' + $line.Replace('<!-- memory:', '&lt;!-- memory:')) }
        }
    }
    if ($history.Count -eq 0) { $lines.Add('Sem eventos registrados.') }
    $lines.Add('<!-- memory:end -->')
    $updated = $brain.Substring(0,$match.Index) + ($lines -join $script:NL) + $brain.Substring($match.Index + $match.Length)
    # Historico e a fonte duravel: se falhar esta escrita, proximo Record/Init reconstroi o bloco.
    # Recover nao substitui o backup bom pelo resumo danificado.
    if ($Action -eq 'Recover') { Write-Atomic $brainPath $updated }
    else { Write-Atomic $brainPath $updated $backupPath }
    Write-Output "Memoria pronta: $brainPath"
} finally {
    if ($lock) { $lock.Dispose() }
}

