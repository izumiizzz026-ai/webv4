# QR ATTENDANCE SYSTEM - DESKTOP APPLICATION

## ✅ Complete Setup Done!

Your QR Attendance System is now ready to be built as a desktop application.

## Quick Start

### 1. **Build the Executable** (One-time)

```powershell
cd "C:\Users\Lem Jasper\OneDrive\Desktop\Portfolio\QR Attendance"
pyinstaller QRAttendance.spec --clean
```

**What this does:**
- Creates standalone Windows executable
- Bundles Python, Flask, and all dependencies
- No Python installation needed for users
- Output: `dist/QRAttendance.exe`

**Build time:** 2-5 minutes (first time)

### 2. **Test the Executable**

```powershell
.\dist\QRAttendance.exe
```

**Expected:**
- Starts Flask server automatically
- Opens browser to login page
- Works exactly like web version

### 3. **Create Windows Installer** (Optional)

**Requirements:**
- NSIS: Download from https://nsis.sourceforge.io/Download
- Install NSIS (default settings)

**Build Installer:**

```powershell
makensis QRAttendance.nsi
```

**Output:** `QRAttendance-Setup-1.0.0.exe`

**What installer does:**
- Professional Windows setup wizard
- Creates Start Menu shortcuts
- Adds to Add/Remove Programs
- One-click uninstall

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `desktop_main.py` | Main entry point for desktop app |
| `QRAttendance.spec` | PyInstaller configuration |
| `QRAttendance.nsi` | NSIS installer script |
| `BUILD_GUIDE.md` | Detailed build documentation |
| `build.ps1` | Automated build script |

---

## 🎯 How It Works

### On User's Computer:

1. **User runs:** `QRAttendance.exe` (or runs installer first)
2. **App starts:**
   - Embedded Flask server boots up (localhost:5000)
   - SQLite database created automatically
   - Browser opens automatically
3. **User sees:** Login page (same as web version)
4. **Full functionality:**
   - Login/signup
   - QR code scanning
   - Attendance tracking
   - Everything works locally!

### No Requirements:
- ❌ No Python installation needed
- ❌ No command line required
- ❌ No technical knowledge needed
- ✅ Just run the .exe file!

---

## 📦 Distribution Options

### Option 1: Portable EXE (Simplest)
- **File:** `dist/QRAttendance.exe` (150+ MB)
- **User action:** Double-click to run
- **Pros:** Single file, no installation
- **Best for:** USB drives, quick testing

### Option 2: Windows Installer (Professional)
- **File:** `QRAttendance-Setup-1.0.0.exe` (150+ MB)
- **User action:** Download → Run → Next → Finish
- **Pros:** Professional look, easy uninstall
- **Best for:** End users, organizations

### Option 3: Portable ZIP (Ultra-light)
- **File:** `dist/` folder (entire directory)
- **User action:** Extract → Run QRAttendance.exe
- **Pros:** Portable, can run from USB
- **Best for:** Portable/temporary deployment

---

## 🔧 Configuration

### Default Settings:
- Database: `attendance.db` (in app folder)
- Port: `localhost:5000`
- Secret Key: `dev-secret-key-change-in-production`

### To Change Settings:

Create `.env` file in app folder:
```
FLASK_SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///attendance.db
```

---

## ⚠️ Important Notes

### First-Time Launch:
- Antivirus might flag it (false positive for unknown exe)
- Database creates automatically
- Admin account: `admin@teacher` / `system123`

### Data Persistence:
- Database stored locally with app
- Data persists between launches
- **Backup `attendance.db` regularly**

### Performance:
- Runs locally (fast!)
- No internet required
- Works offline

---

## 🐛 Troubleshooting

**"Windows blocked this app"**
- Right-click → Properties → Unblock → OK

**"Port 5000 already in use"**
- Close other Flask/QR Attendance instances
- Or edit `desktop_main.py` line 10 to use different port

**"Database locked error"**
- Close app completely
- Delete `attendance.db-journal` if exists
- Restart app

**"Camera won't open"**
- Grant camera permissions in Windows Settings
- Close other camera apps
- Check USB webcam is connected

---

## 📊 File Sizes

| Output | Size |
|--------|------|
| `QRAttendance.exe` | ~150 MB |
| `dist/` folder | ~350 MB |
| Installer | ~150 MB |
| `attendance.db` | ~1-10 MB |

---

## 🚀 Next Steps

1. **Build executable:** `pyinstaller QRAttendance.spec --clean`
2. **Test:** `.\dist\QRAttendance.exe`
3. **Create installer (optional):** Install NSIS, then `makensis QRAttendance.nsi`
4. **Distribute:** Share `QRAttendance.exe` or installer with users

---

## 📞 Support

All functionality from web version is preserved:
- QR code generation
- Attendance scanning
- Student/Teacher panels
- Admin dashboard
- Database operations
- Mobile-responsive UI

See `BUILD_GUIDE.md` for detailed documentation.
