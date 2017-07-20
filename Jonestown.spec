# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/john/dev/python/3.3.2/economy'],
             binaries=[],
             datas=[('/home/john/dev/python/3.3.2/economy/boynames', '.'), ('/home/john/dev/python/3.3.2/economy/girlnames', '.'), ('/home/john/dev/python/3.3.2/economy/businessnames', '.'), ('/home/john/dev/python/3.3.2/economy/churchMusic.txt', '.'), ('/home/john/dev/python/3.3.2/economy/lastnames', '.'), ('/home/john/dev/python/3.3.2/economy/images/greenWheat.gif', './images'), ('/home/john/dev/python/3.3.2/economy/images/nightWheat.gif', './images'), ('/home/john/dev/python/3.3.2/economy/images/parchment.gif', './images'), ('/home/john/dev/python/3.3.2/economy/images/jonestown.gif', './images')],
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
