# Build script for QR Attendance Desktop Application
# Run: .\build.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "QR ATTENDANCE - DESKTOP APP BUILD" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nChecking dependencies..." -ForegroundColor Yellow
$py311 = "C:\Users\Lem Jasper\AppData\Local\Programs\Python\Python311\python.exe"
if (-not (Test-Path $py311)) {
    Write-Host "Python 3.11 not found at $py311. Install Python 3.11 and retry." -ForegroundColor Red
    exit 1
}
Write-Host "Using Python: $py311" -ForegroundColor Yellow
& $py311 --version
$pyinstaller_check = & $py311 -m pip show pyinstaller 2>$null
if (-not $pyinstaller_check) {
    Write-Host "Installing PyInstaller into Python 3.11..." -ForegroundColor Yellow
    & $py311 -m pip install pyinstaller
}

$nsis_path = "C:\Program Files (x86)\NSIS\makensis.exe"
$nsis_available = Test-Path $nsis_path
if (-not $nsis_available) {
    Write-Host "WARNING: NSIS not found. Installer (.nsi) will not be compiled." -ForegroundColor Red
    Write-Host "To install NSIS, download from: https://nsis.sourceforge.io/Download" -ForegroundColor Yellow
}
else {
    Write-Host "NSIS found" -ForegroundColor Green
}

Write-Host "`nCleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") {
    try { Remove-Item -Recurse -Force "build" -ErrorAction Stop }
    catch { Write-Host "Skipping build clean (in use): $($_.Exception.Message)" -ForegroundColor DarkYellow }
}
if (Test-Path "dist") {
    try { Remove-Item -Recurse -Force "dist" -ErrorAction Stop }
    catch { Write-Host "Skipping dist clean (in use): $($_.Exception.Message)" -ForegroundColor DarkYellow }
}

Write-Host "`nBuilding executable (Python 3.11)..." -ForegroundColor Yellow
& $py311 -m PyInstaller QRAttendance.spec --clean --noconfirm

if ($LASTEXITCODE -eq 0) {
    Write-Host "Executable built successfully." -ForegroundColor Green
    Write-Host "Location: .\dist\QRAttendance.exe" -ForegroundColor Green
}
else {
    Write-Host "Build failed." -ForegroundColor Red
    exit 1
}

if ($nsis_available) {
    Write-Host "`nBuilding installer..." -ForegroundColor Yellow
    & $nsis_path "QRAttendance.nsi"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Installer created successfully." -ForegroundColor Green
        Write-Host "Location: .\QRAttendance-Setup-1.0.0.exe" -ForegroundColor Green
    }
    else {
        Write-Host "Installer build failed." -ForegroundColor Red
    }
}
else {
    Write-Host "Skipping NSIS installer build (NSIS not installed)." -ForegroundColor Yellow
}

Write-Host "`nDone." -ForegroundColor Cyan
