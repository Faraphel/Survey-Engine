import sys

from PyQt6.QtWidgets import QApplication

from ui import ReplayWindow


if __name__ == "__main__":
    # create the application
    application = QApplication(sys.argv)

    # create the window
    window = ReplayWindow("surveys.json")
    window.show()

    # start the application
    application.exec()
