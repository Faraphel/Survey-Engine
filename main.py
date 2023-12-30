import sys

from PyQt6.QtCore import QTranslator, QLocale
from PyQt6.QtWidgets import QApplication

from source import translate
from source import assets_path
from source.widget import SurveyWindow


if __name__ == "__main__":
    # create the application
    application = QApplication(sys.argv)

    # get the user language
    local = QLocale()
    language_code: str = local.languageToCode(local.language(), QLocale.LanguageCodeType.ISO639)

    # apply the language on the translator
    translate.set_language(language_code)

    # load the translator to support multiple languages
    translator = QTranslator()
    application.installTranslator(translator)
    translator.load(str(assets_path / f"language/{language_code}.qm"))

    # create the window
    window = SurveyWindow("./surveys.json")
    window.show()

    # start the application
    application.exec()
