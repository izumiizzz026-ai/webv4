param([string]$Action = "run")

# Create venv if missing
if (-not (Test-Path .\venv)) {
    python -m venv .\venv
}

# Activate venv in this script session
. .\venv\Scripts\Activate.ps1

# Install requirements (no-op if already installed)
pip install -r requirements.txt

if ($Action -eq "test") {
    Write-Host "Running tests..."
    python .\tests\test_db.py
    exit $LASTEXITCODE
} else {
    Write-Host "Starting app..."
    $env:FLASK_SECRET_KEY = 'dev'
    python .\app.py
}
