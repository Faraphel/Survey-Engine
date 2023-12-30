from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QCheckBox, QLineEdit

from source import translate
from source.survey.base import BaseSurvey


class MultipleChoiceQuestion(BaseSurvey):
    def __init__(
            self,
            title: translate.Translatable,
            choices: dict[Any, translate.Translatable],
            details_choice_enabled: bool = None,
            details_choice_id: str = None,
            details_choice_text: translate.Translatable = None,
            signals: dict[str, pyqtSignal] = None
    ):
        super().__init__()

        self.details_choice_enabled = details_choice_enabled if details_choice_enabled is not None else None
        self.details_choice_id = details_choice_id if details_choice_id is not None else None
        self.details_choice_text = details_choice_text if details_choice_text is not None else None
        self.signals = signals if signals is not None else {}

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

        # responses
        self.frame_responses = QFrame()
        self._layout.addWidget(self.frame_responses)

        self._layout_responses = QVBoxLayout()
        self.frame_responses.setLayout(self._layout_responses)

        self.button_responses: dict[str, QCheckBox] = {}

        for choice_id, choice_text in choices.items():
            # create a radio button for that choice
            button = QCheckBox()
            button.setText(translate.translate(choice_text))

            # add the button to the frame
            self._layout_responses.addWidget(button)

            # save the button
            self.button_responses[choice_id] = button

        if self.details_choice_enabled:
            self.button_response_other = QCheckBox()
            self._layout_responses.addWidget(self.button_response_other)
            self.button_response_other.setText(translate.translate(self.details_choice_text))
            self.button_response_other.toggled.connect(self._on_response_other_check)  # NOQA: connect exist

            self.entry_response_other = QLineEdit()
            self._layout_responses.addWidget(self.entry_response_other)
            self.entry_response_other.setEnabled(False)

    @classmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "MultipleChoiceQuestion":
        return cls(
            title=data["title"],
            choices=data["choices"],
            details_choice_enabled=data.get("details_choice_enabled"),
            details_choice_id=data.get("details_choice_id"),
            details_choice_text=data.get("details_choice_text"),

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
        collected_data = {
            "choice": [
                choice_id
                for choice_id, button in self.button_responses.items()
                if button.isChecked()
            ]
        }

        if self.details_choice_enabled:
            collected_data["choice"].append(self.details_choice_id)
            collected_data["other"] = self.entry_response_other.text()

        return collected_data
