# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/markemus/dev/economy/economy'],
             binaries=[],
             datas=[('/home/markemus/dev/economy/boynames', '.'), ('/home/markemus/dev/economy/girlnames', '.'), ('/home/markemus/dev/economy/businessnames', '.'), ('/home/markemus/dev/economy/lastnames', '.'), ('/home/markemus/dev/economy/images/greenWheat.gif', './images'), ('/home/markemus/dev/economy/images/nightWheat.gif', './images'), ('/home/markemus/dev/economy/images/parchment.gif', './images'), ('/home/markemus/dev/economy/images/jonestown.gif', './images')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Jonestown',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Jonestown')
