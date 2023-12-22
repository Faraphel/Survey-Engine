from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QRadioButton, QButtonGroup

from source.survey.base import BaseSurvey


class ChoiceQuestion(BaseSurvey):
    def __init__(self, title: str, choices: dict[Any, str], signals: dict[str, pyqtSignal]):
        super().__init__()

        # set layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # question title
        self.label_question = QLabel()
        self._layout.addWidget(self.label_question)
        self.label_question.setText(title)
        self.label_question.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_title = self.label_question.font()
        font_title.setPointSize(24)
        font_title.setWeight(QFont.Weight.Bold)
        self.label_question.setFont(font_title)

        # responses
        self.frame_responses = QFrame()
        self._layout.addWidget(self.frame_responses)

        self._layout_responses = QVBoxLayout()
        self.frame_responses.setLayout(self._layout_responses)

        self.group_responses = QButtonGroup()

        if "success" in signals:
            # checking any button allow the user to go to the next step
            self.group_responses.buttonClicked.connect(signals["success"].emit)  # NOQA: connect and emit exists

        for choice_id, choice_text in choices.items():
            # create a radio button for that choice
            button = QRadioButton()
            button.setText(choice_text)

            # add the button to the frame
            self._layout_responses.addWidget(button)

            # add the button to the group
            self.group_responses.addButton(button, int(choice_id))

    @classmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "ChoiceQuestion":
        return cls(
            title=data["title"],
            choices=data["choices"],

            signals=signals,
        )

    def get_collected_data(self) -> dict:
        return {
            "choice": self.group_responses.checkedId()
        }
