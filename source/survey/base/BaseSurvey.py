from abc import abstractmethod
from typing import Optional, Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget


class BaseSurvey(QWidget):
    """
    A type of survey survey that can be in the user interface
    """

    # initialisation

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "BaseSurvey":
        """
        Create an instance from a configuration dictionary
        :return: the instance
        """

    # data collection

    def get_collected_data(self) -> Optional[dict]:
        """
        Return the data collected for the survey
        :return: the data collected for the survey
        """

        return None

    # survey events

    def on_ready(self) -> None:
        """
        Called once the survey screen is ready to be used
        """

    def on_finalize(self) -> None:
        """
        Called once the survey screen is about to be finished
        """
