import sys

from PyQt6.QtCore import QTranslator, QLocale
from PyQt6.QtWidgets import QApplication

from source import assets_path
from source.widget import MyMainWindow


if __name__ == "__main__":
    # create the application
    application = QApplication(sys.argv)

    # get the user language
    local = QLocale()
    language_code: str = local.languageToCode(local.language())

    # load the translator to support multiple languages
    translator = QTranslator()
    application.installTranslator(translator)
    translator.load(str(assets_path / f"language/{language_code}.qm"))

    # create the window
    window = MyMainWindow()
    window.show()

    # start the application
    application.exec()
