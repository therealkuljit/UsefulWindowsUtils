$ErrorActionPreference = 'Stop'

$profilePath = $PROFILE.CurrentUserCurrentHost
$profileDir = Split-Path -Parent $profilePath
New-Item -ItemType Directory -Path $profileDir -Force | Out-Null

@'
# UsefulWindowsUtils bundled PowerShell profile
Set-Alias ll Get-ChildItem
function which {
    param([Parameter(Mandatory = $true)][string]$Name)
    Get-Command $Name -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
}
if (Get-Module -ListAvailable PSReadLine) {
    Set-PSReadLineOption -EditMode Windows
    Set-PSReadLineOption -PredictionSource History -ErrorAction SilentlyContinue
}
'@ | Set-Content -Path $profilePath -Encoding UTF8

Write-Host "Installed bundled PowerShell profile: $profilePath"
