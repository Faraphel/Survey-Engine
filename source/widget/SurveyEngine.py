import json
import time
import uuid
import zlib
from io import BytesIO
from pathlib import Path
from typing import Optional

import nextcord
import requests
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar, QWidget

from source.survey.base import BaseSurvey
from source.survey import Empty, survey_get


result_path = Path("./results/")
result_path.mkdir(parents=True, exist_ok=True)


class SurveyEngine(QWidget):
    signal_abandon = pyqtSignal()
    signal_skip = pyqtSignal()
    signal_success = pyqtSignal()

    def __init__(self, surveys_data: dict, discord_webhook_result_url: Optional[str] = None):
        super().__init__()

        # signals
        self.signal_abandon.connect(self._on_signal_abandon)  # NOQA: connect exist
        self.signal_skip.connect(self._on_signal_skip)  # NOQA: connect exist
        self.signal_success.connect(self._on_signal_success)  # NOQA: connect exist

        # prepare the survey collected data
        self.collected_datas: dict[str, dict] = {"time": time.time(), "surveys": {}}
        self.discord_webhook_result_url = discord_webhook_result_url
        self.current_survey_index = 0

        # set the layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # prepare the frame for the survey elements
        self.frame_survey: BaseSurvey = Empty()
        self._layout.addWidget(self.frame_survey)

        # navigations actions
        self.frame_navigation = QFrame()
        self._layout.addWidget(self.frame_navigation)

        self._layout_navigation = QHBoxLayout()
        self.frame_navigation.setLayout(self._layout_navigation)

        self._layout_navigation.addStretch(0)  # add a stretch to put the buttons on the right

        self.button_abandon = QPushButton()
        self._layout_navigation.addWidget(self.button_abandon)
        self.button_abandon.setText(self.tr("ABANDON"))
        self.button_abandon.setStyleSheet("QPushButton { color : red; }")
        self.button_abandon.clicked.connect(self.quit)  # NOQA: connect exist

        self.button_skip = QPushButton()
        self._layout_navigation.addWidget(self.button_skip)
        self.button_skip.setText(self.tr("SKIP"))
        self.button_skip.clicked.connect(self.next_survey)  # NOQA: connect exist

        self.button_forward = QPushButton()
        self._layout_navigation.addWidget(self.button_forward)
        self.button_forward.setText(self.tr("NEXT"))
        self.button_forward.clicked.connect(self.next_survey)  # NOQA: connect exist

        # progress bar
        self.progress = QProgressBar()
        self._layout.addWidget(self.progress)
        self.progress.setStyleSheet("QProgressBar::chunk { background-color: #03A9FC; }")
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)

        # load the survey screens
        self.survey_screens = [
            (
                survey_id,
                survey_get(
                    survey_data,
                    signals={
                        "abandon": self.signal_abandon,
                        "skip": self.signal_skip,
                        "success": self.signal_success,
                    }
                )
            )
            for survey_id, survey_data in surveys_data.items()
        ]

        # update the progress bar
        self.progress.setMaximum(len(self.survey_screens))

        # finalize the initialisation
        self.update_survey()

    @classmethod
    def from_dict(cls, data: dict) -> "SurveyEngine":
        return cls(
            surveys_data=data["surveys"],
            discord_webhook_result_url=data.get("discord_webhook_result"),
        )

    @classmethod
    def from_file(cls, path: Path | str) -> "SurveyEngine":
        with open(path, encoding="utf-8") as file:
            data = json.load(file)

        return cls.from_dict(data)

    # events

    def _on_signal_abandon(self):
        # on success, show the button to give up
        self.button_abandon.show()

    def _on_signal_skip(self):
        # on success, show the button to skip
        self.button_skip.show()

    def _on_signal_success(self):
        # on success, show the button to go forward
        self.button_forward.show()

    def next_survey(self):
        # get the collected data from the survey
        collected_data = self.frame_survey.get_collected_data()
        if collected_data is not None:
            # if there is data, get the current survey id
            survey_id, survey = self.survey_screens[self.current_survey_index]
            # save the response in the data
            self.collected_datas["surveys"][survey_id] = collected_data

        self.current_survey_index += 1
        self.progress.setValue(self.current_survey_index)

        if self.current_survey_index < len(self.survey_screens):
            self.update_survey()
        else:
            self.finish_survey()

    def update_survey(self):
        # disable the buttons
        self.button_abandon.hide()
        self.button_skip.hide()
        self.button_forward.hide()

        # mark the actual survey as the old one
        old_frame_survey = self.frame_survey
        # call the old survey event
        old_frame_survey.on_hide()
        # get the currently selected survey
        survey_id, survey = self.survey_screens[self.current_survey_index]
        # update it to the new one
        self.frame_survey = survey
        # change the widget on the layout
        self._layout.replaceWidget(old_frame_survey, self.frame_survey)
        # adjust the size of the widgets
        self.window().adjustSize()
        # call the new survey event
        survey.on_show()
        # delete the old frame
        old_frame_survey.deleteLater()

    def finish_survey(self):
        # TODO: page with indication and progress bar for upload
        # TODO: split into save_file() and upload_file()

        # encode and compress the data
        data: bytes = zlib.compress(json.dumps(self.collected_datas, ensure_ascii=False).encode("utf-8"))

        # save the result in a local file
        (result_path / f"{uuid.uuid4()}.rsl").write_bytes(data)

        # if set, try to send the result to a discord webhook
        if self.discord_webhook_result_url is not None:
            with requests.Session() as session:
                webhook = nextcord.SyncWebhook.from_url(self.discord_webhook_result_url, session=session)
                message = webhook.send(file=nextcord.File(fp=BytesIO(data), filename="result.rsl"), wait=True)

        self.quit()

    def quit(self):
        # quit the application by closing and deleting the window
        self.window().close()
        self.window().deleteLater()
