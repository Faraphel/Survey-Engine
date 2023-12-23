from typing import Optional

from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QProgressBar, QStyle, QToolBar


class Browser(QWidget):
    """
    A version of the QWebEngineView class with integrated progress bar and navigations bar.
    """

    def __init__(self, url: Optional[QUrl] = None):
        super().__init__()

        # layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # navigation bar
        self.navigation = QToolBar()
        self._layout.addWidget(self.navigation, 0)

        style = self.style()

        self._action_back = self.navigation.addAction(
            style.standardIcon(QStyle.StandardPixmap.SP_ArrowBack),
            "Back"
        )
        self._action_reload = self.navigation.addAction(
            style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload),
            "Reload"
        )
        self._action_forward = self.navigation.addAction(
            style.standardIcon(QStyle.StandardPixmap.SP_ArrowForward),
            "Forward"
        )

        # web widget
        self.web = QWebEngineView()
        self._layout.addWidget(self.web, 1)

        if url is not None:
            self.web.load(QUrl(url))

        # loading bar
        self.progress = QProgressBar()
        self._layout.addWidget(self.progress, 0)
        self.progress.setFixedHeight(6)
        self.progress.setTextVisible(False)
        self.progress.setMaximum(100)
        self.progress.hide()

        # connect the signals
        self.web.loadStarted.connect(self._load_started)  # NOQA: connect exist
        self.web.loadProgress.connect(self._load_progress)  # NOQA: connect exist
        self.web.loadFinished.connect(self._load_finished)  # NOQA: connect exist

        self._action_back.triggered.connect(self.web.back)  # NOQA: connect exist
        self._action_reload.triggered.connect(self.web.reload)  # NOQA: connect exist
        self._action_forward.triggered.connect(self.web.forward)  # NOQA: connect exist

        # finalize the initialisation
        self.refresh_navigation_actions()

    # graphical methods

    def _load_started(self):
        # update the progress bar
        self.progress.setValue(0)
        self.progress.show()

    def _load_progress(self, value: int):
        # update the progress bar
        self.progress.setValue(value)

    def _load_finished(self):
        # update the progress bar
        self.progress.hide()
        # refresh the navigation buttons
        self.refresh_navigation_actions()

    def refresh_navigation_actions(self):
        history = self.web.history()
        # enable the navigation button depending on the history
        self._action_back.setEnabled(history.canGoBack())
        self._action_forward.setEnabled(history.canGoForward())
