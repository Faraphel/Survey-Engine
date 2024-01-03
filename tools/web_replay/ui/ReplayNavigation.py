from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ReplayNavigation(QWidget):
    def __init__(self):
        super().__init__()

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # information of the replay
        self._description = QLabel()
        layout.addWidget(self._description)
        self._description.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_description(self, text: str):
        self._description.setText(text)
