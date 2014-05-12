import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os", "re", "sys",
"PyQt5.QtNetwork","PyQt5.QtWidgets",
"PyQt5.QtGui","PyQt5.QtCore","PyQt5.QtMultimedia"], "excludes": []}
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(name='musicPlayer',
      version = '1.0',
      description = 'musicPlayer',
      options = {"build_exe": build_exe_options},
      executables = [Executable("run.pyw", base=base,icon="img/icon/05.ico")])