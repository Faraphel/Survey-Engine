from PyQt6.QtCore import Qt, QUrl, QSize, QPointF
from PyQt6.QtGui import QKeyEvent, QMouseEvent
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication


class ReplayEngine(QWidget):
    """
    This widget allow to replay some event that occurred on a web page
    """

    def __init__(self, replay_data: dict):
        super().__init__()

        self.replay_data = replay_data
        self.iterator = iter(self.replay_data)

        # layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # cursor
        self.cursor = QLabel(self)
        self.cursor.setFixedSize(20, 20)
        self.cursor.setStyleSheet("background-color: red; border-radius: 10px;")

        # web
        self.web = QWebEngineView()
        self._layout.addWidget(self.web)

    def run_event(self, event: dict):
        match event["type"]:
            case "success":
                # success event
                print(f"success ! ({event['time']}s)")

            case "url":
                # changing url event
                self.web.setUrl(QUrl(event["url"]))

            case "resize":
                # changing widget size event
                self.web.resize(QSize(*event["size"]))

                # TODO: better way ?
                self.window().resize(QSize(*event["size"]))

            case "keyboard_press":
                # keyboard key pressed event
                key = QKeyEvent(
                    QKeyEvent.Type.KeyPress,
                    event["key"],
                    Qt.KeyboardModifier.NoModifier
                )
                QApplication.sendEvent(self.web.page(), key)

            case "keyboard_release":
                # keyboard key released event
                key = QKeyEvent(
                    QKeyEvent.Type.KeyRelease,
                    event["key"],
                    Qt.KeyboardModifier.NoModifier
                )
                QApplication.sendEvent(self.web.page(), key)

            case "mouse_press":
                # mouse pressed event
                key = QMouseEvent(
                    QMouseEvent.Type.KeyPress,
                    QPointF(*event["position"]),
                    Qt.MouseButton(event["button"]),
                    Qt.MouseButton.NoButton,
                    Qt.KeyboardModifier.NoModifier
                )
                QApplication.sendEvent(self.web.page(), key)

            case "mouse_release":
                # mouse pressed event
                key = QMouseEvent(
                    QMouseEvent.Type.KeyRelease,
                    QPointF(*event["position"]),
                    Qt.MouseButton(event["button"]),
                    Qt.MouseButton.NoButton,
                    Qt.KeyboardModifier.NoModifier
                )
                QApplication.sendEvent(self.web.page(), key)

            # NOTE: this event is redundant
            # case "mouse_double_click":
            #     # mouse double-clicked event
            #     key = QMouseEvent(QMouseEvent.Type.MouseButtonDblClick, event["position"], event["button"])
            #     QApplication.sendEvent(self.page(), key)

            case "mouse_move":
                # mouse moved event
                key = QMouseEvent(
                    QMouseEvent.Type.KeyRelease,
                    QPointF(*event["position"]),
                    Qt.MouseButton.NoButton,
                    Qt.MouseButton.NoButton,
                    Qt.KeyboardModifier.NoModifier
                )
                QApplication.sendEvent(self.web.page(), key)

                # move the fake cursor
                self.cursor.move(QPointF(*event["position"]).toPoint() - self.cursor.rect().center())
                self.cursor.raise_()

            case "scroll":
                # scroll event
                x, y = event["position"]
                self.web.page().runJavaScript(f"window.scrollTo({x}, {y});")

    def next(self):
        try:
            event = next(self.iterator)
        except StopIteration:
            print("end of record")
            return

        self.run_event(event)
