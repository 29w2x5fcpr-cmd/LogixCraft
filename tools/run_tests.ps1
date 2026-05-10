param(
    [switch]$Fast
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    $Python = "python"
}

$env:QT_QPA_PLATFORM = "offscreen"

Push-Location $ProjectRoot
try {
    & $Python -m ruff check src\logixcraft tests

    if ($Fast) {
        & $Python -m pytest tests\test_smoke.py tests\test_navigation.py tests\test_menu_actions.py tests\test_app_startup.py -q
    }
    else {
        Get-ChildItem tests -Filter "test_*.py" | Sort-Object Name | ForEach-Object {
            & $Python -m pytest $_.FullName -q
            if ($LASTEXITCODE -ne 0) {
                exit $LASTEXITCODE
            }
        }
    }
}
finally {
    Pop-Location
}
