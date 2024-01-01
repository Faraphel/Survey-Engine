import sys

from PyQt6.QtWidgets import QApplication

from source.ui import SurveyWindow


if __name__ == "__main__":
    # create the application
    application = QApplication(sys.argv)

    # create the window
    window = SurveyWindow("./surveys.json")
    window.show()

    # start the application
    application.exec()
