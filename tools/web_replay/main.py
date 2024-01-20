import json
import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QFileDialog

from tools.web_replay.ui import ReplayWindow


if __name__ == "__main__":
    # create the application
    application = QApplication(sys.argv)

    # create the window
    window = ReplayWindow("surveys.json")
    window.show()

    # start the application
    application.exec()
