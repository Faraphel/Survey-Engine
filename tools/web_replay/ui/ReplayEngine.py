from datetime import datetime
from pathlib import Path
from typing import Callable

from PyQt6.QtCore import Qt, QUrl, QPointF, QTimer
from PyQt6.QtGui import QKeyEvent, QMouseEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel

from source.utils import compress
from . import ReplayWebEngineView, ReplayNavigation


class ReplayEngine(QWidget):
    """
    This widget allow to replay some event that occurred on a web page
    """

    def __init__(self, replay_path: Path | str, mission: str):
        super().__init__()

        # load the replay
        with open(replay_path, "rb") as file:
            replay_data = compress.uncompress_data(file.read())

        self.start_time = datetime.fromtimestamp(replay_data["time"])
        self.replay_events = replay_data["surveys"][mission]["event"]
        self.replay_index: int = 0
        self.replay_time: float = 0

        # layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # cursor
        self.cursor = QLabel(self)
        self.cursor.setFixedSize(20, 20)
        self.cursor.setStyleSheet("background-color: red; border-radius: 10px;")

        # web
        self.web = ReplayWebEngineView(self.start_time)
        self._layout.addWidget(self.web, 1)

        # information
        self.navigation = ReplayNavigation()
        self._layout.addWidget(self.navigation)

        # event timer
        self.timer = QTimer()

    def run_event(self, event: dict, callback: Callable):
        # TODO: check if click are done correctly, check position, if event are correct, ...

        match event["type"]:
            case "success":
                # success event
                print(f"success ! ({event['time']}s)")

                callback()

            case "url":
                # changing url event
                self.web.setUrl(QUrl(event["url"]))

                # callback
                self.web.loadFinished.connect(lambda ok: callback())  # NOQA: connect exist

            case "resize":
                # changing widget size event
                w, h = event["size"]
                zoom_factor: float = self.web.page().contentsSize().width() / w
                self.web.setZoomFactor(zoom_factor)

                # callback
                callback()

            case "keyboard_press":
                # keyboard key pressed event
                qevent = QKeyEvent(
                    QKeyEvent.Type.KeyPress,
                    event["key"],
                    Qt.KeyboardModifier.NoModifier
                )
                qevent.custom = True
                QApplication.postEvent(self.web.focusProxy(), qevent)

                # callback
                callback()

            case "keyboard_release":
                # keyboard key released event
                qevent = QKeyEvent(
                    QKeyEvent.Type.KeyRelease,
                    event["key"],
                    Qt.KeyboardModifier.NoModifier
                )
                qevent.custom = True
                QApplication.postEvent(self.web.focusProxy(), qevent)

                # callback
                callback()

            case "mouse_press":
                # mouse pressed event
                qevent = QMouseEvent(
                    QMouseEvent.Type.KeyPress,
                    QPointF(*event["position"]) / self.web.zoomFactor(),
                    Qt.MouseButton(event["button"]),
                    Qt.MouseButton.NoButton,
                    Qt.KeyboardModifier.NoModifier
                )
                qevent.custom = True
                QApplication.postEvent(self.web.focusProxy(), qevent)

                # callback
                callback()

            case "mouse_release":
                # mouse pressed event
                qevent = QMouseEvent(
                    QMouseEvent.Type.KeyRelease,
                    QPointF(*event["position"]) / self.web.zoomFactor(),
                    Qt.MouseButton(event["button"]),
                    Qt.MouseButton.NoButton,
                    Qt.KeyboardModifier.NoModifier
                )
                qevent.custom = True
                QApplication.postEvent(self.web.focusProxy(), qevent)

                # callback
                callback()

            case "mouse_move":
                # mouse moved event
                qevent = QMouseEvent(
                    QMouseEvent.Type.MouseMove,
                    QPointF(*event["position"]) / self.web.zoomFactor(),
                    Qt.MouseButton.NoButton,
                    Qt.MouseButton.NoButton,
                    Qt.KeyboardModifier.NoModifier
                )
                qevent.custom = True
                QApplication.postEvent(self.web.focusProxy(), qevent)

                # move the cursor
                self.cursor.move(QPointF(*event["position"]).toPoint())
                self.cursor.raise_()

                # callback
                callback()

            case "scroll":
                # scroll event
                x, y = event["position"]
                self.web.page().runJavaScript(
                    f"window.scrollTo({x}, {y});",
                    resultCallback=lambda result: callback()
                )

    def next(self):
        # get event information
        if self.replay_index >= len(self.replay_events):
            return

        event = self.replay_events[self.replay_index]
        self.replay_time = event["time"]
        self.replay_index = self.replay_index + 1

        # set text
        self.navigation.set_description(f"{event}")

        # run the event
        self.run_event(
            event,
            self._next_callback
        )

    def _next_callback(self):
        # prevent the web loading to call this function again
        try:
            self.web.loadFinished.disconnect(self._next_callback)  # NOQA: disconnect exist
        except TypeError:
            pass

        # if there are still events after this one
        if self.replay_index < len(self.replay_events):
            # next event
            next_event: dict = self.replay_events[self.replay_index]
            next_time: float = next_event["time"]

            # prepare the timer to play the event at the corresponding time
            self.timer.singleShot(
                round((next_time - self.replay_time) / 200),
                self.next
            )
