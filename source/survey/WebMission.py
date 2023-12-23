import time
from pathlib import Path
from typing import Optional, Any

from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QUrl, QEvent, QObject
from PyQt6.QtGui import QFont, QMouseEvent, QResizeEvent, QKeyEvent
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QSizePolicy

from source import assets_path
from source.survey.base import BaseSurvey
from source.widget import Browser

page_success_path: Path = assets_path / "web/success.html"


class WebMission(BaseSurvey):
    def __init__(self, title: str, url: str, signals: dict[str, pyqtSignal], check_condition: Optional[str] = None):
        super().__init__()

        self.check_condition = check_condition
        self.default_url = url
        self.signals = signals if signals is not None else {}

        self._finished = False

        # set layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # data collection
        self.start_time = time.time()
        self._collected_events: list[dict[str, Any]] = []

        # mission title
        self.label_title = QLabel()
        self._layout.addWidget(self.label_title)
        self.label_title.setText(title)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_title = self.label_title.font()
        font_title.setPointSize(24)
        font_title.setWeight(QFont.Weight.Bold)
        self.label_title.setFont(font_title)

        # web page
        self.browser = Browser()
        self._layout.addWidget(self.browser)
        self.browser.web.focusProxy().installEventFilter(self)  # capture the event in eventFilter
        self.browser.web.urlChanged.connect(self._on_url_changed)  # NOQA: connect exist

        self.browser.web.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # setup the timer for the check
        if self.check_condition is not None:
            self.timer_check = QTimer()
            self.timer_check.setInterval(1000)
            self.timer_check.timeout.connect(self.check)  # NOQA: connect exist

    @classmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "WebMission":
        return cls(
            title=data["title"],
            url=data.get("url"),
            check_condition=data.get("check"),

            signals=signals
        )

    # events

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj is self.browser.web.focusProxy() and not self._finished:
            # if the object is the content of the web engine widget
            match event.type():
                case QEvent.Type.MouseMove:
                    # if this is a mouse movement
                    event: QMouseEvent
                    position = event.position()

                    self._save_event(
                        type="mouse_move",
                        position=(position.x(), position.y()),
                    )

                case QEvent.Type.MouseButtonPress:
                    # if this is a mouse click press
                    event: QMouseEvent
                    position = event.position()

                    self._save_event(
                        type="mouse_press",
                        position=(position.x(), position.y()),
                        button=event.button(),
                    )

                case QEvent.Type.MouseButtonRelease:
                    # if this is a mouse click release
                    event: QMouseEvent
                    position = event.position()

                    self._save_event(
                        type="mouse_release",
                        position=(position.x(), position.y()),
                        button=event.button(),
                    )

                case QEvent.Type.MouseButtonDblClick:
                    # if this is a mouse double click
                    event: QMouseEvent
                    position = event.position()

                    self._save_event(
                        type="mouse_double_click",
                        position=(position.x(), position.y()),
                    )

                case QEvent.Type.KeyPress:
                    # when the keyboard is pressed
                    event: QKeyEvent

                    self._save_event(
                        type="keyboard_press",
                        key=event.key(),
                    )

                case QEvent.Type.KeyRelease:
                    # when the keyboard is released
                    event: QKeyEvent

                    self._save_event(
                        type="keyboard_release",
                        key=event.key(),
                    )

                case QEvent.Type.Resize:
                    # if the window got resized
                    event: QResizeEvent
                    size = event.size()

                    self._save_event(
                        type="resize",
                        size=(size.width(), size.height()),
                    )

        return super().eventFilter(obj, event)

    def on_show(self) -> None:
        # initialize the start time
        self.start_time = time.time()

        # set the web view to the default url
        self.browser.web.setUrl(QUrl(self.default_url))

        # enable the full screen mode
        self.window().showFullScreen()

        if self.check_condition is not None:
            # enable the timer
            self.timer_check.start()

        else:
            self._success()  # call directly the success method

    def on_hide(self) -> None:
        # disable full screen mode
        self.window().showMinimized()

        # stop the checking loop
        self.timer_check.stop()

    def _success(self):
        if self._finished:
            return

        # mark the mission as finished
        self._finished = True

        # mark the success in the events
        self._save_event(type="check")

        # emit on the success signal
        if "success" in self.signals:
            self.signals["success"].emit()  # NOQA: emit exist

        # change the content of the page to the success message
        self.browser.web.load(QUrl.fromLocalFile(str(page_success_path.absolute())))

    # condition

    def check(self) -> None:
        """
        Check if the checking condition have been completed
        """

        def check_callback(result: bool):
            if result:
                self._success()

        page = self.browser.web.page()
        page.runJavaScript(self.check_condition, resultCallback=check_callback)

    # data collection

    def _save_event(self, **data) -> None:
        # save the data of the event and add the current time
        data["time"] = round(time.time() - self.start_time, 3)
        self._collected_events.append(data)

    def get_collected_data(self) -> dict:
        return {
            "event": self._collected_events,
        }

    def _on_url_changed(self):
        # log the new url
        self._save_event(
            type="url",
            url=self.browser.web.url().toString()
        )
