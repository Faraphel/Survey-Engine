import sys
from PyQt6.QtWidgets import QApplication

from source.widget import MyMainWindow


if __name__ == "__main__":
    application = QApplication(sys.argv)

    window = MyMainWindow()
    window.show()

    application.exec()
