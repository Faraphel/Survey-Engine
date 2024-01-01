from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton


class SurveyNavigation(QWidget):
    def __init__(self, signals: dict[str, pyqtSignal] = None):
        super().__init__()

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)

        # force the element to be on the right with a stretch
        self._layout.addStretch()

        # abandon button

        self._button_abandon = QPushButton()
        self._layout.addWidget(self._button_abandon)
        self._button_abandon.setText(self.tr("ABANDON"))
        self._button_abandon.setStyleSheet("QPushButton { color : red; }")

        if signals is not None and "abandon" in signals:
            self._button_abandon.clicked.connect(signals["abandon"].emit)  # NOQA: connect and emit exist

        # skip button

        self._button_skip = QPushButton()
        self._layout.addWidget(self._button_skip)
        self._button_skip.setText(self.tr("SKIP"))

        if signals is not None and "skip" in signals:
            self._button_skip.clicked.connect(signals["skip"].emit)  # NOQA: connect and emit exist

        # forward button

        self._button_forward = QPushButton()
        self._layout.addWidget(self._button_forward)
        self._button_forward.setText(self.tr("NEXT"))

        if signals is not None and "success" in signals:
            self._button_forward.clicked.connect(signals["success"].emit)  # NOQA: connect and emit exist

        # get all buttons
        self._buttons = [
            self._button_abandon,
            self._button_skip,
            self._button_forward
        ]

        # hide every button per default
        self.hide_all()

    def show_abandon(self):
        self._button_abandon.setVisible(True)

    def hide_abandon(self):
        self._button_abandon.setVisible(False)

    def show_skip(self):
        self._button_skip.setVisible(True)

    def hide_skip(self):
        self._button_skip.setVisible(False)

    def show_forward(self):
        self._button_forward.setVisible(True)

    def hide_forward(self):
        self._button_forward.setVisible(False)

    def show_all(self):
        for button in self._buttons:
            button.setVisible(True)

    def hide_all(self):
        for button in self._buttons:
            button.setVisible(False)
