import json
from pathlib import Path

from PyQt6.QtWidgets import QMainWindow

from tools.web_replay.ui import ReplayConfiguration, ReplayEngine


class ReplayWindow(QMainWindow):
    def __init__(self, survey_path: Path | str):
        super().__init__()

        # get the survey configuration
        with open(survey_path, encoding="utf-8") as file:
            survey_configuration: dict = json.load(file)

        # get all the missions available in the survey that can be replayed
        missions: list[str] = [
            mission_id
            for mission_id, mission in survey_configuration["surveys"].items()
            if mission["type"] == "mission-web"
        ]

        # decoration
        self.setWindowTitle("Survey Engine - Web Replay")

        # show the configuration
        self.replay_engine = None
        self.replay_configuration = ReplayConfiguration(missions=missions)
        self.setCentralWidget(self.replay_configuration)
        self.replay_configuration.signal_start_replay.connect(self.start_replay)

    def start_replay(self, replay_path: str, mission: str):
        # start the replay
        self.replay_engine = ReplayEngine(replay_path, mission)
        self.setCentralWidget(self.replay_engine)
        self.showFullScreen()
        self.replay_engine.next()
