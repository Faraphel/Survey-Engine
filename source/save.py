from io import BytesIO
from pathlib import Path
from typing import Optional

import nextcord
import requests
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication

result_path = Path("./results/")


def save_all(
        data: bytes,
        filename: str,
        discord_webhook_url: Optional[str] = None,
        signal_warning: Optional[pyqtSignal] = None
):
    # save to a file
    save_file(data, filename)

    # upload to a discord webhook
    if discord_webhook_url is not None:
        upload_discord(data, discord_webhook_url, filename, signal_warning)


def save_file(
        data: bytes,
        filename: str
) -> None:
    """
    Save the result data to a file
    """

    result_path.mkdir(parents=True, exist_ok=True)
    (result_path / filename).write_bytes(data)


def upload_discord(
        data: bytes,
        discord_webhook_url: str,
        filename: str,
        signal_warning: Optional[pyqtSignal] = None
) -> None:
    """
    Upload the result to a discord webhook
    """

    # create a session
    with requests.Session() as session:
        # load the configured webhook
        webhook = nextcord.SyncWebhook.from_url(discord_webhook_url, session=session)

        try:
            # send the message to discord
            message = webhook.send(
                file=nextcord.File(fp=BytesIO(data), filename=filename),
                wait=True
            )

        except Exception as exc:
            if signal_warning is not None:
                application = QApplication.instance()
                signal_warning.emit(application.tr("COULD NOT UPLOAD THE DATA"))  # NOQA: emit exist
            else:
                raise exc
