@echo off
REM QR Attendance Desktop App - Build Script
REM This script automates the build process for Windows

echo ========================================
echo QR ATTENDANCE - DESKTOP APP BUILD
echo ========================================
echo.

REM Check if PyInstaller is installed
echo Checking for PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
)
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1
echo Done.
echo.

REM Build the executable
echo Building executable...
echo This may take 2-5 minutes...
echo.
pyinstaller QRAttendance.spec --clean

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo EXECUTABLE BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Location: %cd%\dist\QRAttendance.exe
    echo Size: 150+ MB
    echo.
    echo Test: Run .\dist\QRAttendance.exe
    echo.
) else (
    echo.
    echo BUILD FAILED!
    echo Check the errors above.
    echo.
    pause
    exit /b 1
)

REM Check for NSIS
echo.
echo Checking for NSIS installer...
if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
    echo NSIS found. Build installer? (y/n)
    set /p choice=
    if /i "%choice%"=="y" (
        echo Building installer...
        "C:\Program Files (x86)\NSIS\makensis.exe" QRAttendance.nsi
        if %errorlevel% equ 0 (
            echo.
            echo INSTALLER BUILD SUCCESSFUL!
            echo Location: %cd%\QRAttendance-Setup-1.0.0.exe
            echo.
        )
    )
) else (
    echo NSIS not found. Skipping installer build.
    echo To build installer, install NSIS from: https://nsis.sourceforge.io/
    echo.
)

echo ========================================
echo BUILD COMPLETE!
echo ========================================
pause
