from abc import abstractmethod
from typing import Any, Type

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QButtonGroup, QLineEdit, QAbstractButton

from source import translate, widget
from source.survey.base import BaseSurvey


class BaseChoiceQuestion(BaseSurvey):
    """
    Base for a question that contains multiple options
    """

    @classmethod
    @abstractmethod
    def get_button_choice_class(cls) -> Type[QAbstractButton]:
        """
        The class for the button representing the choices
        """

    @classmethod
    @abstractmethod
    def are_buttons_exclusive(cls) -> bool:
        """
        Are the buttons exclusive ?
        """

    def __init__(
            self,
            title: translate.Translatable,
            choices: dict,
            signals: dict[str, pyqtSignal] = None
    ):
        super().__init__()

        signals = signals if signals is not None else {}

        # set layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # question title
        self.label_question = QLabel()
        self._layout.addWidget(self.label_question)
        self.label_question.setText(translate.translate(title))
        self.label_question.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_title = self.label_question.font()
        font_title.setPointSize(24)
        font_title.setWeight(QFont.Weight.Bold)
        self.label_question.setFont(font_title)

        # prepare navigation
        self.navigation = widget.SurveyNavigation(signals=signals)

        # responses
        self.frame_responses = QFrame()
        self._layout.addWidget(self.frame_responses)

        self._layout_responses = QVBoxLayout()
        self.frame_responses.setLayout(self._layout_responses)

        self.group_responses = QButtonGroup()
        self.group_responses.setExclusive(self.are_buttons_exclusive())

        # checking any button allow the user to go to the next step
        self.group_responses.buttonClicked.connect(self.navigation.show_forward)  # NOQA: connect and emit exists

        self.buttons_responses: dict[QAbstractButton, dict] = {}
        button_choice_class = self.get_button_choice_class()

        for choice_id, choice_data in choices.items():
            # create a radio button for that choice
            button = button_choice_class()
            button.setText(translate.translate(choice_data["text"]))

            # add the button to the frame
            self._layout_responses.addWidget(button)

            # add the button to the group
            self.group_responses.addButton(button)

            # if the choice should ask the user for details
            entry = None
            if choice_data.get("ask_details", False):
                entry = QLineEdit()
                self._layout_responses.addWidget(entry)
                entry.setEnabled(False)

                # toggling the button should also toggle the entry
                button.toggled.connect(entry.setEnabled)  # NOQA: connect exist

            # save the button and some data
            self.buttons_responses[choice_id] = {
                "button": button,
                "entry": entry
            }

        # add the navigation
        self._layout.addWidget(self.navigation)

        if not self.are_buttons_exclusive():
            # if the buttons are not exclusive, allow to select no options
            self.navigation.show_forward()

    @classmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "BaseChoiceQuestion":
        return cls(
            title=data["title"],
            choices=data["choices"],
            signals=signals,
        )

    def get_collected_data(self) -> dict:
        collected_data = {
            "choices": {
                choice_id: {
                    "checked": choice_data["button"].isEnabled(),
                    "details": entry.text() if (entry := choice_data["entry"]) is not None else None
                }
                for choice_id, choice_data in self.buttons_responses.items()
            }
        }

        return collected_data
