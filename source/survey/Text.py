from typing import Optional, Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QLabel

from survey.base import BaseSurvey


class Text(BaseSurvey):
    def __init__(self, title: str, description: Optional[str], signals: dict[str, pyqtSignal]):
        super().__init__()

        self.signals = signals

        # set the layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # prepare the title
        self.label_title = QLabel()
        self._layout.addWidget(self.label_title)
        self.label_title.setText(title)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_title = self.label_title.font()
        font_title.setPointSize(32)
        font_title.setWeight(QFont.Weight.Bold)
        self.label_title.setFont(font_title)

        if description is not None:
            # prepare the description
            self.label_description = QLabel()
            self._layout.addWidget(self.label_description)
            self.label_description.setText(description)
            self.label_description.setAlignment(Qt.AlignmentFlag.AlignCenter)

    @classmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "Text":
        return cls(
            title=data["title"],
            description=data.get("description"),

            signals=signals
        )

    def on_show(self) -> None:
        if "success" in self.signals:
            # the user can skip a text whenever he wants to, directly signal a success
            self.signals["success"].emit()  # NOQA: emit exist


