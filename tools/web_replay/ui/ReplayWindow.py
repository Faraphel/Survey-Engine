from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow

from tools.web_replay.ui import ReplayEngine


class ReplayWindow(QMainWindow):
    def __init__(self, replay_data: dict):
        super().__init__()

        self.replay_engine = ReplayEngine(replay_data)
        self.setCentralWidget(self.replay_engine)

        # TODO: TEST REMOVE
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.replay_engine.next)  # NOQA: connect exist
        self.timer.start()
