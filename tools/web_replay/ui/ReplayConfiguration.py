from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QFrame, QHBoxLayout, QComboBox, QFileDialog


class ReplayConfiguration(QWidget):
    signal_start_replay = pyqtSignal([str, str])

    def __init__(self, missions: list[str]):
        super().__init__()

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # replay path
        self.frame_path = QFrame()
        layout.addWidget(self.frame_path)

        layout_path = QHBoxLayout()
        self.frame_path.setLayout(layout_path)

        self.entry_path = QLineEdit()
        layout_path.addWidget(self.entry_path)

        self.button_path = QPushButton()
        layout_path.addWidget(self.button_path)
        self.button_path.setText("...")
        self.button_path.clicked.connect(self.select_replay)  # NOQA: connect exist

        # mission
        self.frame_mission = QFrame()
        layout.addWidget(self.frame_mission)

        layout_mission = QHBoxLayout()
        self.frame_mission.setLayout(layout_mission)

        self.listbox_mission = QComboBox()
        layout_mission.addWidget(self.listbox_mission)

        for mission in missions:
            self.listbox_mission.addItem(mission)

        # button
        self.button_confirm = QPushButton()
        layout.addWidget(self.button_confirm)
        self.button_confirm.setText("Replay")
        self.button_confirm.clicked.connect(self._start_replay)  # NOQA: connect exist

    def select_replay(self):
        # prompt the user for a file
        file, raw_filetype = QFileDialog.getOpenFileName(
            caption="Select the file to replay.",
            filter="Replay (*.rsl)"
        )

        # if no file were selected, ignore
        if not file:
            return

        self.entry_path.setText(file)

    def _start_replay(self):
        self.signal_start_replay.emit(self.entry_path.text(), self.listbox_mission.currentText())  # NOQA: emit
