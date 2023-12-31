import sys

from cx_Freeze import setup, Executable

from source import __appname__, __str_version__, __author__, __mail__, __description__, __icon_ico__


# Win32GUI should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None


setup(
    name=__appname__,
    version=__str_version__,
    description=__description__,
    author=__author__,
    author_email=__mail__,
    url='',
    license='',

    options={
        "build_exe": {
            "include_msvcr": True,
            "include_files": [
                ("./assets/", "./assets/"),
                ("./README.md", "./README.md"),
            ]
        }
    },

    executables=[Executable(
        "main.py",
        base=base,
        target_name=__appname__,
        icon=__icon_ico__
    )]
)