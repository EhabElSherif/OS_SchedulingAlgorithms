# -*- mode: python -*-
import sys
sys.setrecursionlimit(5000)
block_cipher = None


a = Analysis(['Main.py'],
             pathex=['C:\\Users\\Ehab Rabie\\Documents\\Visual Studio 2017\\Projects\\miniOS1\\miniOS1'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
