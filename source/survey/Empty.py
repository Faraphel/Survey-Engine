from typing import Any

from PyQt6.QtCore import pyqtSignal
from source.survey.base import BaseSurvey


class Empty(BaseSurvey):
    @classmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "BaseSurvey":
        return Empty()
