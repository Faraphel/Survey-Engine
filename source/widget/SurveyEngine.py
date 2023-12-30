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
from PyQt6.QtWidgets import QVBoxLayout, QProgressBar, QWidget

from source import translate
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
        self.collected_datas: dict[str, dict] = {
            "time": time.time(),  # get the time of the start of the survey
            "language": translate.get_language(),  # get the user language
            "surveys": {}  # prepare the individual surveys data
        }
        self.discord_webhook_result_url = discord_webhook_result_url
        self.current_survey_index = 0

        # load the survey screens
        # TODO: create dynamically
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

        # set the layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # prepare the frame for the survey elements
        self.frame_survey: BaseSurvey = Empty()
        self._layout.addWidget(self.frame_survey)

        # progress bar
        self.progress = QProgressBar()
        self._layout.addWidget(self.progress)
        self.progress.setStyleSheet("QProgressBar::chunk { background-color: #03A9FC; }")
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        self.progress.setMaximum(len(surveys_data))

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
        # on abandon, quit the survey
        self.quit()

    def _on_signal_skip(self):
        # on skip, skip to the next survey
        self.next_survey()

    def _on_signal_success(self):
        # on success, go to the next survey
        self.next_survey()

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

        filename: str = f"{uuid.uuid4()}.rsl"

        # save the result in a local file
        self.result_save_file(result_path / filename)

        # if set, try to send the result to a discord webhook
        if self.discord_webhook_result_url is not None:
            try:
                self.result_upload_discord(filename=filename)
            except nextcord.HTTPException:
                # TODO: say to send manually the local file
                raise

        self.quit()

    def get_result_data(self) -> bytes:
        """
        Return the compressed result data
        """

        return zlib.compress(json.dumps(self.collected_datas, ensure_ascii=False).encode("utf-8"))

    def result_save_file(self, destination: Path | str) -> None:
        """
        Save the result data to a file
        :param destination: the path to the file
        """

        with open(destination, "wb") as file:
            file.write(self.get_result_data())

    def result_upload_discord(self, filename: str = "result.rsl") -> None:
        """
        Upload the result to a discord webhook
        """

        # create a session
        with requests.Session() as session:
            # load the configured webhook
            webhook = nextcord.SyncWebhook.from_url(
                self.discord_webhook_result_url,
                session=session
            )

            # send the message to discord
            message = webhook.send(
                file=nextcord.File(
                    fp=BytesIO(self.get_result_data()),
                    filename=filename),
                wait=True
            )

    def quit(self):
        # quit the application by closing and deleting the window
        self.window().close()
        self.window().deleteLater()
