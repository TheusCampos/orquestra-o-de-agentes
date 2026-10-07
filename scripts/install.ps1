[CmdletBinding(SupportsShouldProcess)]
param([Parameter(Mandatory)][string]$ProjectPath, [string]$Profile = 'general')
& (Join-Path $PSScriptRoot 'sync-project.ps1') -ProjectPath $ProjectPath -Profile $Profile -WhatIf:$WhatIfPreference
