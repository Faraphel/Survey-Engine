from typing import Optional, Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QLabel

from source import translate, widget
from source.survey.base import BaseSurvey


class Text(BaseSurvey):
    def __init__(
            self,
            title: translate.Translatable,
            description: Optional[translate.Translatable],
            abandonable: bool = None,
            signals: dict[str, pyqtSignal] = None
    ):
        super().__init__()

        self.abandonable = abandonable if abandonable is not None else False

        # set the layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # prepare the title
        self.label_title = QLabel()
        self._layout.addWidget(self.label_title)
        self.label_title.setText(translate.translate(title))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_title = self.label_title.font()
        font_title.setPointSize(32)
        font_title.setWeight(QFont.Weight.Bold)
        self.label_title.setFont(font_title)

        if description is not None:
            # prepare the description
            self.label_description = QLabel()
            self._layout.addWidget(self.label_description)
            self.label_description.setText(translate.translate(description))
            self.label_description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # navigation
        self.navigation = widget.SurveyNavigation(signals=signals)
        self._layout.addWidget(self.navigation)

        self.navigation.show_forward()  # always show forward
        if self.abandonable:
            self.navigation.show_abandon()  # if enabled, show abandon

    @classmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "Text":
        return cls(
            title=data["title"],
            description=data.get("description"),
            abandonable=data.get("abandonable"),

            signals=signals
        )
