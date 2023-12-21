import time
from typing import Optional, Any

from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QSizePolicy

from survey.base import BaseSurvey
from source.widget import DecoratedWebEngineView


class WebMission(BaseSurvey):
    def __init__(self, title: str, url: str, signals: dict[str, pyqtSignal], check_condition: Optional[str] = None):
        super().__init__()

        self.check_condition = check_condition
        self.default_url = url
        self.signals = signals  # TODO: default None ?

        # set layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # data collection
        self.initial_time = time.time()
        self.collect_urls: list[tuple[float, str]] = []  # list of urls that the user went by

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
        self.web_view = DecoratedWebEngineView()
        self._layout.addWidget(self.web_view)
        self.web_view.urlChanged.connect(self._on_url_changed)  # NOQA: connect exist

        self.web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

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

    def on_show(self) -> None:
        self.web_view.setUrl(QUrl(self.default_url))

        if self.check_condition is not None:
            # enable the timer
            self.timer_check.start()

        else:
            # call directly the success signal
            if "success" in self.signals:
                self.signals["success"].emit()  # NOQA: emit exist

    def on_hide(self) -> None:
        self.timer_check.stop()

    # data collection

    def get_collected_data(self) -> dict:
        # TODO: more data to collect
        return {
            "collect_urls": self.collect_urls
        }

    def _on_url_changed(self):
        self.collect_urls.append((time.time() - self.initial_time, self.web_view.url()))

    # condition

    def check(self) -> None:
        """
        Check if the checking condition have been completed
        """

        def check_callback(result: bool):
            if result and "success" in self.signals:
                self.signals["success"].emit()  # NOQA: emit exist

        page = self.web_view.page()
        page.runJavaScript(self.check_condition, resultCallback=check_callback)
