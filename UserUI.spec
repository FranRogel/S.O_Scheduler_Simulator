# -- coding: utf-8 --
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None  # Definir block_cipher como None

a = Analysis(
    ['UserUI.py'],
    pathex=['.'],
    binaries=[],
    datas=[('process_set/*.json', 'process_set')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='UserUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    cipher=block_cipher,
)

