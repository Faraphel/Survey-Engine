import typing
import uuid
from io import BytesIO
from pathlib import Path
from typing import Optional

import nextcord
import requests
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QProgressBar, QVBoxLayout, QLabel, QMessageBox

from source import widget
from source.utils.compress import compress_data


result_path = Path("./results/")


class SavingScreen(QWidget):
    def __init__(
            self,
            collected_datas: dict,
            discord_webhook_url: Optional[str] = None
    ):
        super().__init__()

        self.compressed_collected_datas = compress_data(collected_datas)
        self.discord_webhook_url = discord_webhook_url

        # layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # prepare the title
        self.label_title = QLabel()
        self._layout.addWidget(self.label_title)
        self.label_title.setText(self.tr("UPLOADING DATA"))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_title = self.label_title.font()
        font_title.setPointSize(24)
        font_title.setWeight(QFont.Weight.Bold)
        self.label_title.setFont(font_title)

        # progress
        self.progress = QProgressBar()
        self._layout.addWidget(self.progress)

        # prepare the filename
        filename: str = f"{uuid.uuid4()}.rsl"

        # start a thread for the saving
        thread = QThread()
        thread.started.connect(lambda: self.save(filename))  # NOQA: connect exist
        thread.start()

    def save(self, filename: str):
        # save to a file
        self.result_save_file(filename)

        # upload to a discord webhook
        if self.discord_webhook_url is not None:
            try:
                self.result_upload_discord(filename)
            except nextcord.HTTPException:
                # if there is an error while uploading, show a graphical warning to the user
                QMessageBox.warning(
                    self,
                    title=self.tr("WARNING"),
                    text=self.tr("COULD NOT UPLOAD TO DISCORD, SEND MANUALLY"),
                )

        # quit the application
        window = typing.cast(widget.SurveyWindow, self.window())
        window.quit()

    def result_save_file(self, filename: str) -> None:
        """
        Save the result data to a file
        """

        result_path.mkdir(parents=True, exist_ok=True)
        (result_path / filename).write_bytes(self.compressed_collected_datas)

    def result_upload_discord(self, filename: str) -> None:
        """
        Upload the result to a discord webhook
        """

        # create a session
        with requests.Session() as session:
            # load the configured webhook
            webhook = nextcord.SyncWebhook.from_url(self.discord_webhook_url, session=session)

            # send the message to discord
            message = webhook.send(
                file=nextcord.File(fp=BytesIO(self.compressed_collected_datas), filename=filename),
                wait=True
            )
