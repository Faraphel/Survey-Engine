from abc import abstractmethod
from typing import Optional, Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget


class BaseSurvey(QWidget):
    """
    A type of survey survey that can be in the user interface
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "BaseSurvey":
        """
        Create an instance from a configuration dictionary
        :return: the instance
        """

    def on_show(self) -> None:
        """
        Called when the survey is shown
        """

    def on_hide(self) -> None:
        """
        Called when the survey is hidden
        :return:
        """

    def get_collected_data(self) -> Optional[dict]:
        """
        Return the data collected for the survey
        :return: the data collected for the survey
        """

        return None
