from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QCheckBox, QLineEdit

from source.survey.base import BaseSurvey


class MultipleChoiceQuestion(BaseSurvey):
    def __init__(
            self,
            title: str,
            choices: dict[Any, str],
            other_choice: bool = None,
            signals: dict[str, pyqtSignal] = None
    ):
        super().__init__()

        self.other_choice = other_choice if other_choice is not None else None
        self.signals = signals if signals is not None else {}

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

        self.button_responses: dict[str, QCheckBox] = {}

        for choice_id, choice_text in choices.items():
            # create a radio button for that choice
            button = QCheckBox()
            button.setText(choice_text)

            # add the button to the frame
            self._layout_responses.addWidget(button)

            # save the button
            self.button_responses[choice_id] = button

        if self.other_choice:
            self.button_response_other = QCheckBox()
            self._layout_responses.addWidget(self.button_response_other)
            self.button_response_other.setText("Autre")
            self.button_response_other.clicked.connect(self._on_response_other_check)  # NOQA: connect exist

            self.entry_response_other = QLineEdit()
            self._layout_responses.addWidget(self.entry_response_other)
            self.entry_response_other.setEnabled(False)

    @classmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "MultipleChoiceQuestion":
        return cls(
            title=data["title"],
            choices=data["choices"],
            other_choice=data.get("other_choice"),

            signals=signals,
        )

    def on_show(self) -> None:
        if "success" in self.signals:
            # the user can skip a text whenever he wants to, directly signal a success
            self.signals["success"].emit()  # NOQA: emit exist

    def _on_response_other_check(self):
        # refresh the other entry response status
        self.entry_response_other.setEnabled(self.button_response_other.isChecked())

    def get_collected_data(self) -> dict:
        return {
            "choice": {choice_id: button.isChecked() for choice_id, button in self.button_responses.items()},
            "other": (
                self.entry_response_other.text() if self.other_choice and self.button_response_other.isChecked()
                else None
            )
        }
