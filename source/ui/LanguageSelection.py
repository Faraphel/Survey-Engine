from typing import Callable

from PyQt6.QtCore import Qt, QLocale, QTranslator
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QApplication, QPushButton

from source import assets_path, translate


class LanguageSelection(QWidget):
    def __init__(self, after: Callable):
        super().__init__()

        self.after = after

        # layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # title
        self.title = QLabel()
        self._layout.addWidget(self.title)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # language selection
        self.select_language = QComboBox()
        self._layout.addWidget(self.select_language)

        language_default = QLocale().language()  # get the default locale

        for i, language_file in enumerate((assets_path / "language").glob("*.qm")):
            # add every translated language to the selection

            language_code: str = language_file.stem
            language = QLocale.codeToLanguage(language_code, QLocale.LanguageCodeType.ISO639)

            self.select_language.addItem(language.name, language_code)

            # if the added language is the default one, select it directly
            if language == language_default:
                self.select_language.setCurrentIndex(i)

        self.select_language.currentIndexChanged.connect(self.refresh_language)  # NOQA: connect exist

        # start button
        self.button_start = QPushButton()
        self._layout.addWidget(self.button_start)
        self.button_start.clicked.connect(self.start)  # NOQA: connect exist

        # refresh the texts
        self.refresh_language()

    def refresh_language(self):
        language_code = self.select_language.currentData()

        # load the correct translator
        translator = QTranslator()
        translator.load(str(assets_path / f"language/{language_code}.qm"))

        # apply the language on the custom translator
        translate.set_language(language_code)

        # install the translator on the application
        application = QApplication.instance()
        application.installTranslator(translator)

        # refresh the texts
        self.retranslate()

    def retranslate(self):
        self.title.setText(self.tr("SELECT YOUR LANGUAGE"))
        self.button_start.setText(self.tr("START"))

    def start(self) -> None:
        # call the after event
        self.after()

        # delete the language selection
        self.deleteLater()
