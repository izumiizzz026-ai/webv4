# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['desktop_main.py'],
    pathex=[],
    binaries=[],
    datas=[('CSS', 'CSS'), ('JS', 'JS'), ('index.html', '.'), ('teacher.html', '.'), ('student.html', '.'), ('admin.html', '.'), ('accountcreate.html', '.'), ('app.py', '.'), ('pyproject.toml', '.'), ('LYFJRSHS_logo.jpg', '.'), ('LYFJRSHS_logo.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='desktop_main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='LYFJRSHS_logo.ico',
)
