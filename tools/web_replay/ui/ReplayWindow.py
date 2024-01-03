from datetime import datetime

from PyQt6.QtWidgets import QMainWindow

from tools.web_replay.ui import ReplayEngine


class ReplayWindow(QMainWindow):
    def __init__(self, start_time: datetime, replay_data: list):
        super().__init__()

        # decoration
        self.setWindowTitle("Survey Engine - Web Replay")

        # setup the engine
        self.replay_engine = ReplayEngine(start_time, replay_data)
        self.setCentralWidget(self.replay_engine)

        # show the window as fullscreen
        self.showFullScreen()

        # TODO: remove ?
        self.replay_engine.next()  # play the replay
