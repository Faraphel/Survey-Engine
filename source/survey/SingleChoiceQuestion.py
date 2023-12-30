from typing import Type

from PyQt6.QtWidgets import QAbstractButton, QRadioButton

from source.survey.base import BaseChoiceQuestion


class SingleChoiceQuestion(BaseChoiceQuestion):
    @classmethod
    def get_button_choice_class(cls) -> Type[QAbstractButton]:
        return QRadioButton

    @classmethod
    def are_buttons_exclusive(cls) -> bool:
        return True
