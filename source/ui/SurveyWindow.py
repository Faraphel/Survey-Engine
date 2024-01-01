from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow

from source import ui, assets_path, __icon_png__

icon_path = assets_path / "icon.png"


class SurveyWindow(QMainWindow):
    def __init__(self, survey_path: Path | str):
        super().__init__()

        # window style
        self.setWindowIcon(QIcon(__icon_png__))
        self.setWindowTitle(self.tr("SURVEY"))

        # start by asking the user his language
        language_selection = ui.LanguageSelection(
            # after the language is selected, start the survey
            after=lambda: self.setCentralWidget(ui.SurveyEngine.from_file(survey_path))
        )
        self.setCentralWidget(language_selection)

    def quit(self):
        # quit the application by closing and deleting the window
        self.window().close()
        self.window().deleteLater()
