from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QDoubleSpinBox, QSpinBox

from source.survey.base import BaseSurvey


class IntegerQuestion(BaseSurvey):
    def __init__(self, title: str, signals: dict[str, pyqtSignal] = None):
        super().__init__()

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

        # response
        self.entry_response = QSpinBox()
        self.entry_response.setMinimum(13)
        self.entry_response.setMaximum(200)
        self.entry_response.setValue(30)
        self._layout.addWidget(self.entry_response)

    @classmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "IntegerQuestion":
        return cls(
            title=data["title"],
            signals=signals,
        )

    # events

    def on_show(self) -> None:
        # immediately mark the survey as successful
        if "success" in self.signals:
            self.signals["success"].emit()  # NOQA: emit exist

    # data collection

    def get_collected_data(self) -> dict:
        return {
            "value": self.entry_response.value()
        }
