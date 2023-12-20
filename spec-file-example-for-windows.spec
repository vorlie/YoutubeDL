# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['youtubedl-windows.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('PATH-TO-THIS-FOLDER\\assets', 'assets'),
        ('PATH-TO-THIS-ICON\\icon.ico', '.'),
        ('PATH-TO-THIS-FOLDER\\dependencies', '.')
	],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='YoutubeDL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
