from typing import Type

from PyQt6.QtWidgets import QAbstractButton, QCheckBox

from source.survey.base import BaseChoiceQuestion


class MultipleChoiceQuestion(BaseChoiceQuestion):
    @classmethod
    def get_button_choice_class(cls) -> Type[QAbstractButton]:
        return QCheckBox

    @classmethod
    def are_buttons_exclusive(cls) -> bool:
        return False
