from pathlib import Path

from PyQt6.QtCore import QTranslator
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication

from source import ui, assets_path, __icon_png__, __appname__

icon_path = assets_path / "icon.png"


class SurveyWindow(QMainWindow):
    def __init__(self, survey_path: Path | str):
        super().__init__()

        self.translator = QTranslator()
        QApplication.instance().installTranslator(self.translator)

        # window style
        self.setWindowIcon(QIcon(__icon_png__))
        self.setWindowTitle(__appname__)

        # start by asking the user his language
        self.language_selection = ui.LanguageSelection(
            parent=self,
            # after the language is selected, start the survey
            after=lambda: self.setCentralWidget(ui.SurveyEngine.from_file(survey_path))
        )
        self.setCentralWidget(self.language_selection)

    def quit(self):
        # quit the application by closing and deleting the window
        self.window().close()
        self.window().deleteLater()
