# -*- mode: python -*-

block_cipher = None


a = Analysis(['post_send.py'],
             pathex=['C:\\python27', 'E:\\block_han\\mydata\\my_python\\my_learn\\tk_learn\\py_to_exe'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='post_send',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='2.ico')
