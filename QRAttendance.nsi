; QR Attendance System - Windows Installer
; Build with: makensis QRAttendance.nsi

; Ensure NSIS include path is available (some shells don’t export NSISDIR)
!ifmacrodef NSISDIR
  !addincludedir "${NSISDIR}\Include"
!else
  !addincludedir "C:\\Program Files (x86)\\NSIS\\Include"
!endif
!include "MUI2.nsh"
!include "nsDialogs.nsh"

; Installer icons
!define MUI_ICON "LYFJRSHS_logo.ico"
!define MUI_UNICON "LYFJRSHS_logo.ico"
Icon "LYFJRSHS_logo.ico"
UninstallIcon "LYFJRSHS_logo.ico"

; Application details
!define APP_NAME "QR Attendance System"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "Your Organization"
!define APP_URL "https://yourwebsite.com"
!define INSTALL_DIR "$PROGRAMFILES\QR Attendance System"

; Installer settings
Name "${APP_NAME} ${APP_VERSION}"
OutFile "QRAttendance-Setup-${APP_VERSION}.exe"
InstallDir "${INSTALL_DIR}"
InstallDirRegKey HKCU "Software\QR Attendance System" ""

; Request admin privileges for installation
RequestExecutionLevel admin

; MUI2 Interface Settings
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

; Installer sections
Section "Install"
  SetOutPath "$INSTDIR"
  
  ; Copy the executable and supporting files
  File "dist\QRAttendance.exe"
  
  ; Create Start Menu shortcuts
  SetOutPath "$SMPROGRAMS\QR Attendance System"
  CreateShortcut "$SMPROGRAMS\QR Attendance System\QR Attendance.lnk" "$INSTDIR\QRAttendance.exe"
  CreateShortcut "$SMPROGRAMS\QR Attendance System\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  
  ; Create Desktop shortcut (optional)
  CreateShortcut "$DESKTOP\QR Attendance.lnk" "$INSTDIR\QRAttendance.exe"
  
  ; Create Uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  ; Register in Control Panel
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\QR Attendance System" "DisplayName" "${APP_NAME} ${APP_VERSION}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\QR Attendance System" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\QR Attendance System" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\QR Attendance System" "InstallLocation" "$INSTDIR"
  
  ; Registry key for installation path
  WriteRegStr HKCU "Software\QR Attendance System" "" "$INSTDIR"
SectionEnd

; Uninstaller section
Section "Uninstall"
  ; Remove files
  Delete "$INSTDIR\QRAttendance.exe"
  Delete "$INSTDIR\Uninstall.exe"
  
  ; Remove shortcuts
  Delete "$SMPROGRAMS\QR Attendance System\QR Attendance.lnk"
  Delete "$SMPROGRAMS\QR Attendance System\Uninstall.lnk"
  Delete "$DESKTOP\QR Attendance.lnk"
  
  ; Remove directories
  RMDir "$SMPROGRAMS\QR Attendance System"
  RMDir "$INSTDIR"
  
  ; Remove registry keys
  DeleteRegKey HKCU "Software\QR Attendance System"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\QR Attendance System"
SectionEnd
