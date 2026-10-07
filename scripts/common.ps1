Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$script:LibraryRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$script:Utf8 = New-Object System.Text.UTF8Encoding($false)
$script:NL = [string][char]10
function Read-Text([string]$Path) { [IO.File]::ReadAllText($Path, $script:Utf8) }
function Read-Json([string]$Path) { Read-Text $Path | ConvertFrom-Json }
function Get-ByteHash([byte[]]$Bytes) {
    $sha = [Security.Cryptography.SHA256]::Create()
    try { ([BitConverter]::ToString($sha.ComputeHash($Bytes))).Replace('-', '').ToLowerInvariant() }
    finally { $sha.Dispose() }
}
function Get-TextHash([string]$Text) { Get-ByteHash ($script:Utf8.GetBytes($Text)) }
function Resolve-Child([string]$Root, [string]$Relative) {
    if ([IO.Path]::IsPathRooted($Relative) -or [string]::IsNullOrWhiteSpace($Relative)) { throw "Caminho relativo invalido: $Relative" }
    $base = [IO.Path]::GetFullPath($Root).TrimEnd('\', '/')
    $result = [IO.Path]::GetFullPath((Join-Path $base $Relative))
    if (-not $result.StartsWith($base + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw "Caminho fora do destino: $Relative" }
    $result
}
function Assert-NoLinks([string]$Path) {
    $cursor = [IO.Path]::GetFullPath($Path)
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            $item = Get-Item -LiteralPath $cursor -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Link ou junction nao permitido: $cursor" }
        }
        $parent = [IO.Path]::GetDirectoryName($cursor.TrimEnd('\', '/'))
        if (-not $parent -or $parent -eq $cursor) { break }
        $cursor = $parent
    }
}
function Get-Catalog([string]$Kind) {
    $data = Read-Json (Join-Path $script:LibraryRoot "registry/$Kind.json")
    foreach ($entry in $data) { Write-Output $entry }
}
function Get-Profile([string]$Name) {
    if ($Name -notmatch '^[a-z][a-z0-9-]*$') { throw "Perfil invalido: $Name" }
    $path = Resolve-Child $script:LibraryRoot "profiles/$Name.json"
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Perfil inexistente: $Name" }
    Read-Json $path
}
function Get-Selected($Catalog, $Ids) {
    foreach ($id in $Ids) {
        $found = @($Catalog | Where-Object { $_.id -eq $id })
        if ($found.Count -ne 1) { throw "Referencia ausente ou duplicada: $id" }
        $found[0]
    }
}
function Convert-ToTomlLiteral([string]$Value) {
    if ($Value.Contains("'''")) { throw 'Texto contem delimitador TOML nao suportado.' }
    "'''" + $Value + "'''"
}

