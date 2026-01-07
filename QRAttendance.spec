# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for QR Attendance Desktop App
Run: pyinstaller QRAttendance.spec
"""

import sys
import os

block_cipher = None

a = Analysis(
    ['desktop_main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('CSS', 'CSS'),
        ('JS', 'JS'),
        ('index.html', '.'),
        ('teacher.html', '.'),
        ('student.html', '.'),
        ('admin.html', '.'),
        ('accountcreate.html', '.'),
        ('desktop_config.json', '.'),
        ('testscanner.py', '.'),
        ('app.py', '.'),
        ('db_manager.py', '.'),
        ('LYFJRSHS_logo.jpg', '.'),
        ('LYFJRSHS_logo.ico', '.'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtWebEngineCore',
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_bcrypt',
        'cv2',
        'qrcode',
        'PIL',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='QRAttendance',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window - clean desktop app
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='LYFJRSHS_logo.ico',
)
