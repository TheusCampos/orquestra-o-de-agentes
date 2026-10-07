[CmdletBinding()]
param([string]$ProjectPath)
. (Join-Path $PSScriptRoot 'common.ps1')
& (Join-Path $PSScriptRoot 'validate.ps1')
$command = Get-Command codex -ErrorAction SilentlyContinue
if ($command) { Write-Output "Codex encontrado: $($command.Source)" } else { Write-Output 'Codex CLI nao encontrado; app/IDE pode ter runtime proprio.' }
if (-not $ProjectPath) { Write-Output 'Informe -ProjectPath para verificar uma instalacao.'; return }
$target = [IO.Path]::GetFullPath($ProjectPath)
$manifestPath = Resolve-Child $target '.agent-library/manifest.json'
Assert-NoLinks $manifestPath
if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) { throw 'Projeto sem manifesto da biblioteca.' }
$manifest = Read-Json $manifestPath
if ($manifest.schemaVersion -ne 1) { throw 'Manifesto incompativel.' }
foreach ($file in $manifest.files) {
    $path = Resolve-Child $target $file.path
    Assert-NoLinks $path
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Arquivo ausente: $($file.path)" }
    if ((Get-ByteHash ([IO.File]::ReadAllBytes($path))) -ne $file.hash) { throw "Arquivo diverge do manifesto: $($file.path)" }
}
$agentsPath = Resolve-Child $target 'AGENTS.md'
Assert-NoLinks $agentsPath
$body = Read-Text $agentsPath
$match = [regex]::Match($body, '(?s)<!-- agent-library:begin -->.*?<!-- agent-library:end -->')
if (-not $match.Success -or (Get-TextHash $match.Value) -ne $manifest.agentsBlockHash) { throw 'Bloco AGENTS.md ausente ou alterado.' }
if (Test-Path -LiteralPath (Resolve-Child $target 'AGENTS.override.md')) { Write-Output 'ATENCAO: AGENTS.override.md pode substituir AGENTS.md no projeto.' }
$config = Resolve-Child $target '.codex/config.toml'
Assert-NoLinks $config
if (Test-Path -LiteralPath $config) {
    if ((Read-Text $config) -match '(?ms)^\[agents\]\s*(?:(?!^\[).)*?^\s*enabled\s*=\s*false') {
        Write-Output 'ATENCAO: agentes desativados na configuracao local.'
    }
}
Write-Output "OK: integridade de $(@($manifest.files).Count) arquivos; perfil=$($manifest.profile); versao=$($manifest.libraryVersion)."
$brainPath = Resolve-Child $target 'BRAIN.md'
Assert-NoLinks $brainPath
if (-not (Test-Path -LiteralPath $brainPath -PathType Leaf)) { Write-Output 'ATENCAO: BRAIN.md ausente; inicialize memoria antes de retomar.' }
else { Write-Output 'BRAIN.md presente; conteudo do projeto preservado fora dos hashes de sincronizacao.' }
Write-Output 'Diagnostico estatico. Em nova sessao, confirme instrucoes, skills e custom agents carregados; nao houve chamada ao modelo.'
