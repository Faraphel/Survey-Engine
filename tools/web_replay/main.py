import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication

from tools.web_replay.ui import ReplayWindow


if __name__ == "__main__":
    # create the application
    application = QApplication(sys.argv)

    # TODO: cmd arguments ?
    from source.utils import compress
    with open(r"C:\Users\RC606\PycharmProjects\M1-Recherche\results\c3376670-548d-4494-b963-dc2facf7a3d1.rsl", "rb") as file:
        data = compress.uncompress_data(file.read())

    # create the window
    window = ReplayWindow(
        datetime.fromtimestamp(data["time"]),
        data["surveys"]["mission-language"]["event"]
    )
    window.show()

    # start the application
    application.exec()
