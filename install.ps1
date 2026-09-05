Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "🇧🇪 Lancement de l'auto-configuration de The Agency..." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Host "[ERREUR] Python n'est pas détecté sur votre système." -ForegroundColor Red
    Write-Host "Veuillez installer Python depuis https://www.python.org/downloads/ ou via le Microsoft Store."
    exit 1
}

& $pythonCmd.Source "$PSScriptRoot\install.py" $args
