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

        self.surveys_data = surveys_data
        self.discord_webhook_result_url = discord_webhook_result_url
        self._current_survey_index = 0

        self.collected_datas: dict[str, dict] = {
            "time": time.time(),  # get the time of the start of the survey
            "language": translate.get_language(),  # get the user language
            "surveys": {}  # prepare the individual surveys data
        }

        # signals
        self.signal_abandon.connect(self._on_signal_abandon)  # NOQA: connect exist
        self.signal_skip.connect(self._on_signal_skip)  # NOQA: connect exist
        self.signal_success.connect(self._on_signal_success)  # NOQA: connect exist

        # set the layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # prepare the frame for the survey elements
        self.survey: BaseSurvey = Empty()
        self._layout.addWidget(self.survey)

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

    # property

    @property
    def current_survey_index(self):
        return self._current_survey_index

    @current_survey_index.setter
    def current_survey_index(self, value: int):
        self._current_survey_index = value
        self.progress.setValue(self.current_survey_index)

    @property
    def current_survey_id(self) -> str:
        return list(self.surveys_data.keys())[self.current_survey_index]

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
        collected_data = self.survey.get_collected_data()
        if collected_data is not None:
            # save the response in the data
            self.collected_datas["surveys"][self.current_survey_id] = collected_data

        # go to the next survey
        self.current_survey_index += 1

        if self.current_survey_index < len(self.surveys_data):
            # if there are still survey to do, show it
            self.update_survey()
        else:
            # otherwise end the survey
            self.finish_survey()

    def update_survey(self):

        # mark the actual survey as the old one
        old_survey = self.survey

        # finalize the old_survey
        old_survey.on_finalize()

        # get the currently selected survey
        new_survey = survey_get(
            self.surveys_data[self.current_survey_id],
            signals={
                "abandon": self.signal_abandon,
                "skip": self.signal_skip,
                "success": self.signal_success,
            }
        )

        # update it to the new one
        self.survey = new_survey
        # change the widget on the layout
        self._layout.replaceWidget(old_survey, self.survey)

        # delete the old frame
        old_survey.deleteLater()

        # mark the new survey as ready
        self.survey.on_ready()

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
