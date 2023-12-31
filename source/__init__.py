from pathlib import Path

assets_path = Path("./assets/")

__appname__ = "Survey Engine"
__version__ = (1,0,0)
__str_version__ = ".".join(map(str, __version__))
__author__ = "Faraphel"
__mail__ = "rc60650@hotmail.com"
__description__ = "An engine to create survey."
__icon_png__ = str(assets_path / "icon.png")
__icon_ico__ = str(assets_path / "icon.ico")
