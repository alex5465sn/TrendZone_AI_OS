param(
    [string]$Destino = "C:\Backups\TrendZone"
)

$data = Get-Date -Format "yyyyMMdd_HHmmss"
$pastaDestino = Join-Path $Destino $data
New-Item -ItemType Directory -Force -Path $pastaDestino | Out-Null

Copy-Item -Path "$PSScriptRoot\..\backend\trendzone.db" -Destination $pastaDestino -ErrorAction SilentlyContinue
Copy-Item -Path "$PSScriptRoot\..\.env" -Destination $pastaDestino -ErrorAction SilentlyContinue

Write-Output "Backup criado em: $pastaDestino"
