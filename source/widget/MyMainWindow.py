from PyQt6.QtWidgets import QMainWindow

from source import widget


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setCentralWidget(widget.FrameSurvey("./surveys.json"))
