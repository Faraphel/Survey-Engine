from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow

from source import widget, assets_path


icon_path = assets_path / "icon.png"


class SurveyWindow(QMainWindow):
    def __init__(self, survey_path: Path | str):
        super().__init__()

        self.setWindowIcon(QIcon(str(icon_path.resolve())))
        self.setWindowTitle(self.tr("SURVEY"))

        self.setCentralWidget(widget.SurveyEngine.from_file(survey_path))
