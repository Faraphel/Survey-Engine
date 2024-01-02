import sys

from PyQt6.QtWidgets import QApplication

from tools.web_replay.ui import ReplayWindow


if __name__ == "__main__":
    # create the application
    application = QApplication(sys.argv)

    from source.utils import compress
    with open(r"C:\Users\RC606\Downloads\41a6268b-72e5-47a9-8106-6c15a0be366e.rsl", "rb") as file:
        data = compress.uncompress_data(file.read())

    # create the window
    window = ReplayWindow(data["surveys"]["mission-gift-card"]["event"])
    window.show()

    # start the application
    application.exec()
