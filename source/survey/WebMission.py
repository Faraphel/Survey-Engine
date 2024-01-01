import time
from typing import Optional, Any

from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QUrl, QEvent, QObject, QPointF
from PyQt6.QtGui import QFont, QMouseEvent, QResizeEvent, QKeyEvent
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QSizePolicy

from source import translate, ui
from source.survey.base import BaseSurvey


class WebMission(BaseSurvey):
    def __init__(
            self,
            title: translate.Translatable,
            url: str,

            initial_js: Optional[str] = None,
            start_check_js: Optional[str] = None,
            check_js: Optional[str] = None,

            skip_time: Optional[float] = None,
            signals: dict[str, pyqtSignal] = None
    ):
        super().__init__()

        self.initial_js = initial_js if initial_js is not None else ""
        self.start_check_js = start_check_js if start_check_js is not None else "true"
        self.check_js = check_js if check_js is not None else "true"

        self.default_url = url
        self.skip_time = skip_time
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
        self.label_title.setText(translate.translate(title))
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_title = self.label_title.font()
        font_title.setPointSize(24)
        font_title.setWeight(QFont.Weight.Bold)
        self.label_title.setFont(font_title)

        # web page
        self.browser = ui.Browser()
        self._layout.addWidget(self.browser)

        self.browser.web.focusProxy().installEventFilter(self)  # capture the event in eventFilter
        self.browser.web.urlChanged.connect(self._on_url_changed)  # NOQA: connect exist

        self.browser.web.setUrl(QUrl(self.default_url))
        self.browser.web.loadFinished.connect(self._initialise_js)  # NOQA: connect exist

        self.browser.web.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # setup the events
        self.browser.web.page().scrollPositionChanged.connect(self._on_scroll_position_changed)

        # navigation
        self.navigation = ui.SurveyNavigation(signals=signals)
        self._layout.addWidget(self.navigation)

        # initialize the start time
        self.start_time = time.time()

        # initialise the timers
        self.timer_start_check: Optional[QTimer] = None
        self.timer_check: Optional[QTimer] = None
        self.timer_skip: Optional[QTimer] = None

        # skip timer
        if self.skip_time is not None:
            self.timer_skip = QTimer()
            self.timer_skip.setInterval(self.skip_time * 1000)
            self.timer_skip.timeout.connect(self._allow_time_skip)  # NOQA: connect exist

            self.timer_skip.start()

    @classmethod
    def from_dict(cls, data: dict[str, Any], signals: dict[str, pyqtSignal]) -> "WebMission":
        return cls(
            title=data["title"],
            url=data.get("url"),

            initial_js=data.get("initial_js"),
            start_check_js=data.get("start_check_js"),
            check_js=data.get("check_js"),

            skip_time=data.get("skip_time"),

            signals=signals
        )

    # events

    def _on_scroll_position_changed(self, position: QPointF):
        self._save_event(type="scroll", position=[position.x(), position.y()])

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
                        position=[position.x(), position.y()],
                    )

                case QEvent.Type.MouseButtonPress:
                    # if this is a mouse click press
                    event: QMouseEvent
                    position = event.position()

                    self._save_event(
                        type="mouse_press",
                        position=[position.x(), position.y()],
                        button=event.button().value,
                    )

                case QEvent.Type.MouseButtonRelease:
                    # if this is a mouse click release
                    event: QMouseEvent
                    position = event.position()

                    self._save_event(
                        type="mouse_release",
                        position=[position.x(), position.y()],
                        button=event.button().value,
                    )

                case QEvent.Type.MouseButtonDblClick:
                    # if this is a mouse double click
                    event: QMouseEvent
                    position = event.position()

                    self._save_event(
                        type="mouse_double_click",
                        position=[position.x(), position.y()],
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
                        size=[size.width(), size.height()],
                    )

        return super().eventFilter(obj, event)

    def _success(self):
        if self._finished:
            return

        # mark the success in the events
        self._save_event(type="check")

        # emit on the success signal
        if "success" in self.signals:
            self.signals["success"].emit()  # NOQA: emit exist

        # mark the mission as finished
        self._finished = True

    def _on_url_changed(self):
        # log the new url
        self._save_event(
            type="url",
            url=self.browser.web.url().toString()
        )

    def _allow_time_skip(self):
        # when the timer to allow skip have run out
        if "skip" in self.signals:
            self.navigation.show_skip()

    # condition

    def _preprocess_check(self, check: str) -> str:
        """
        Preprocess a check
        """

        check = check.replace("#LANGUAGE_CODE#", translate.get_language())
        check = check.replace("#START_TIME#", str(self.start_time))

        return check

    def _initialise_js(self, ok: bool):
        # prevent the event from being call a second time
        self.browser.web.loadFinished.disconnect(self._initialise_js)

        def callback(result: bool):
            self.timer_start_check = QTimer()
            self.timer_start_check.setInterval(100)
            self.timer_start_check.timeout.connect(self._start_check)  # NOQA: connect exist
            self.timer_start_check.start()

        # run the initial command
        self.browser.web.page().runJavaScript(
            self._preprocess_check(self.initial_js),
            resultCallback=callback
        )

    def _start_check(self) -> None:
        """
        Check if the real checking condition should start
        """

        # if the check evaluated to True, enable the normal check
        def callback(result: bool):
            if result:
                # stop this start check timer
                self.timer_start_check.stop()

                # create a new timer for the normal check
                self.timer_check = QTimer()
                self.timer_check.setInterval(100)
                self.timer_check.timeout.connect(self._check)  # NOQA: connect exist
                self.timer_check.start()

        # run the check
        self.browser.web.page().runJavaScript(
            self._preprocess_check(self.start_check_js),
            resultCallback=callback
        )

    def _check(self) -> None:
        """
        Check if the checking condition have been completed
        """

        # if the check evaluated to True, call the success method
        def callback(result: bool):
            if result:
                # stop this check timer
                self.timer_check.stop()
                # mark the test as successful
                self._success()

        # run the check
        self.browser.web.page().runJavaScript(
            self._preprocess_check(self.check_js),
            resultCallback=callback
        )

    # data collection

    def _save_event(self, **data) -> None:
        # if the mission is already finished, ignore
        if self._finished:
            return

        # save the data of the event and add the current time
        data["time"] = round(time.time() - self.start_time, 3)
        self._collected_events.append(data)

    def get_collected_data(self) -> dict:
        return {
            "event": self._collected_events,
        }

    # survey events

    def on_ready(self) -> None:
        # enable the maximized mode
        self.window().showMaximized()

    def on_finalize(self) -> None:
        # disable the maximized mode
        self.window().showNormal()
