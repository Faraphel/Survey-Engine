from typing import Type

from PyQt6.QtCore import pyqtSignal

from . import Text, SingleChoiceQuestion, MultipleChoiceQuestion, WebMission, Empty, TextQuestion, IntegerQuestion
from .base import BaseSurvey


all_survey: dict[str, Type[BaseSurvey]] = {
    # base
    "empty": Empty,
    "text": Text,
    # questions
    "question-single-choice": SingleChoiceQuestion,
    "question-multiple-choice": MultipleChoiceQuestion,
    "question-text": TextQuestion,
    "question-integer": IntegerQuestion,
    # missions
    "mission-web": WebMission,
}


def survey_get(data: dict[str, ...], signals: dict[str, pyqtSignal]) -> BaseSurvey:
    """
    Return a Survey object from the data
    :param data: the data of the survey
    :param signals: signal that the survey survey can react to
    :return: a Survey object
    """

    survey_class = all_survey[data["type"]]
    return survey_class.from_dict(data, signals=signals)
