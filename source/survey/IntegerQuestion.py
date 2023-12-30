from typing import Any, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QSpinBox

from source import translate
from source.survey.base import BaseSurvey


class IntegerQuestion(BaseSurvey):
    def __init__(
            self,
            title: translate.Translatable,
            default: Optional[int] = None,
            minimum: Optional[int] = None,
            maximum: Optional[int] = None,
            signals: dict[str, pyqtSignal] = None
    ):
        super().__init__()

        default = default if default is not None else 0
        minimum = minimum if minimum is not None else 0
        maximum = maximum if maximum is not None else 100
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

        # response
        self.entry_response = QSpinBox()
        self.entry_response.setMinimum(minimum)
        self.entry_response.setMaximum(maximum)
        self.entry_response.setValue(default)
        self._layout.addWidget(self.entry_response)

    @classmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "IntegerQuestion":
        return cls(
            title=data["title"],
            default=data.get("default"),
            minimum=data.get("minimum"),
            maximum=data.get("maximum"),
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
