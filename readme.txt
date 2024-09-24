Link a un ejecutable: https://drive.google.com/drive/u/0/folders/1dpeDtylxNH8aZITofT5AoBRKWMEmbxUY
Descargado esta carpeta del drive se puede usar el programa directamente

En caso de querer crear un ejecutable se necesita:

1. Instalar la libreria pyinstaller, usando el comando pip install pyinstaller
2. Abre la terminal o el símbolo del sistema (cmd) y navega a la carpeta donde se encuentra UserUI.py
3. Crea un ejecutable con el comando: pyinstaller --onefile UserUI.py
4. Copia la carpeta "process_set" del proyecto en la nueva carpeta "dist".
5. Abre el archivo UserUI.spec y reemplaza su contenido por:
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
6.Abre la terminal o el símbolo del sistema (cmd) y navega a la carpeta donde se encuentra UserUI.spec
7.Utiliza el comando pyinstaller UserUI.spec para que los cambies del .spec se reflejen en el ejecutable
8.El ejecutable de la carpeta "dist" ya deberia ser funcional