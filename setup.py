import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
    base = "Win32GUI"  

executables = [Executable("x.py", base=base, icon="Logo.ico", target_name="ValoArt.exe")]

packages = ["tkinter", "pygame"]
includes = ["tkinter.ttk", "json"]
excludes = []
include_files = ["data.json","cuack.mp3","logo.ico"] 

options = {
    'build_exe': {
        'packages': packages,
        'includes': includes,
        'excludes': excludes,
        'include_files': include_files,
    },
}

setup(
    name="ValoArt",
    options=options,
    version="1.0",
    description="Crear Valorant copy pastes",
    executables=executables,
)
