# QR Attendance System - Desktop Application Build Guide

## Overview

This guide explains how to build the QR Attendance System as a standalone Windows desktop application with an installer.

## Prerequisites

### Required
- Python 3.11+ (already installed)
- PyInstaller: `pip install pyinstaller`

### Optional (for installer)
- NSIS (Nullsoft Scriptable Install System) - [Download](https://nsis.sourceforge.io/Download)

## Project Structure

```
QR Attendance/
├── desktop_main.py          # Desktop app entry point
├── app.py                   # Flask application (unchanged)
├── QRAttendance.spec        # PyInstaller configuration
├── QRAttendance.nsi         # NSIS installer script
├── build.ps1                # Build script (Windows PowerShell)
├── HTML files               # All static pages
├── CSS/                     # Stylesheets
├── JS/                      # JavaScript files
└── requirements.txt         # Python dependencies
```

## Build Instructions

### Step 1: Install Dependencies

```powershell
# Install PyInstaller
pip install pyinstaller

# Install NSIS (optional, for installer)
# Download from: https://nsis.sourceforge.io/Download
# Or use Chocolatey: choco install nsis
```

### Step 2: Build the Executable

**Option A: Using the Build Script (Recommended)**

```powershell
# Navigate to project directory
cd "C:\Users\Lem Jasper\OneDrive\Desktop\Portfolio\QR Attendance"

# Run build script
.\build.ps1
```

**Option B: Manual Build with PyInstaller**

```powershell
pyinstaller QRAttendance.spec --clean
```

### Step 3: Test the Executable

```powershell
# Run the generated executable
.\dist\QRAttendance.exe
```

**Expected behavior:**
1. Console window opens showing startup messages
2. Browser automatically opens to the app
3. Login page appears
4. All functions work exactly as before

### Step 4: Create Installer (Optional)

If NSIS is installed:

```powershell
# Build installer
makensis QRAttendance.nsi
```

This creates: `QRAttendance-Setup-1.0.0.exe`

## Distribution

### Option 1: Portable Executable
- Located at: `dist/QRAttendance.exe`
- Users can run directly without installation
- Single file, no dependencies
- Recommended for USB/portable distribution

### Option 2: Windows Installer
- Located at: `QRAttendance-Setup-1.0.0.exe`
- Users download and run installer
- Creates Start Menu shortcuts
- Registers in Control Panel/Add Remove Programs
- Uninstall support

## How the App Works

1. **Launch:** User runs `QRAttendance.exe` or installer
2. **Server Starts:** Flask server begins on `localhost:5000`
3. **Browser Opens:** Automatically opens the web interface
4. **Database Created:** SQLite database created if needed
5. **Normal Operation:** All web features work as before

## Important Notes

### Environment Variables
The app uses default settings:
- Database: `attendance.db` (in app directory)
- Flask Secret Key: `dev-secret-key-change-in-production`
- Port: `5000`

To customize, create a `.env` file in the app directory:
```
FLASK_SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///attendance.db
```

### Database
- SQLite database is created automatically
- Located in the app installation directory
- Persists between app launches
- Backup `attendance.db` before uninstalling

### Permissions
- No admin privileges required to run app
- Admin privileges needed for installation

## Troubleshooting

### "Port 5000 already in use"
- Another Flask server is running
- Close any other QR Attendance windows
- Or modify port in `desktop_main.py`

### "Browser won't open"
- Check firewall settings
- Try manual access: http://localhost:5000

### Database locked error
- Ensure only one instance is running
- Close the app completely
- Delete `attendance.db-journal` if it exists

### Camera not working
- Grant camera permissions in Windows Settings
- Close other apps using camera
- Check if USB webcam is connected

## Building Updates

To create an updated installer:

1. Update code as needed
2. Test with `desktop_main.py` directly
3. Run `.\build.ps1` again
4. This creates a new executable and installer

## Advanced Customization

### Add App Icon
1. Create a 256×256 PNG file named `app_icon.ico`
2. Place in project root
3. PyInstaller will use it automatically

### Change App Name/Version
Edit `QRAttendance.nsi`:
```
!define APP_VERSION "1.1.0"
!define APP_PUBLISHER "Your Organization"
```

### Modify Installer Behavior
Edit `QRAttendance.nsi` to customize:
- License file
- Installation folder
- Start Menu location
- Registry entries
- Uninstaller behavior

## System Requirements

**Minimum:**
- Windows 7 SP1 or later (64-bit)
- 512 MB RAM
- 200 MB disk space
- Camera for QR scanning (optional)

**Recommended:**
- Windows 10/11 (64-bit)
- 2 GB RAM
- 500 MB disk space
- USB 3.0 or integrated camera

## Security Notes

For production deployment:

1. **Change Flask Secret Key:**
   - Set `FLASK_SECRET_KEY` environment variable
   - Use a strong random string (32+ characters)

2. **Database Security:**
   - Use PostgreSQL instead of SQLite
   - Set `DATABASE_URL` environment variable
   - Encrypt database files

3. **Admin Credentials:**
   - Login: `admin@teacher` / `system123`
   - Change password after first login
   - Update hardcoded credentials in `app.py`

4. **HTTPS/SSL:**
   - For production, implement SSL certificates
   - Don't use `debug=True` in production

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Flask logs in console window
3. Check `attendance.db` exists and is writable
4. Verify all Python dependencies are installed

## License

[Your License Here]
