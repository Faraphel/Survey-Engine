from typing import Optional

from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QProgressBar, QFrame, QHBoxLayout, QPushButton, QStyle


class DecoratedWebEngineView(QWidget):
    """
    A version of the QWebEngineView class with integrated progress bar and navigations bar.
    """

    def __init__(self, url: Optional[QUrl] = None):
        super().__init__()

        # layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # navigation bar
        self.frame_navigation = QFrame()
        self._layout.addWidget(self.frame_navigation, 0)
        self._layout_navigation = QHBoxLayout()
        self.frame_navigation.setLayout(self._layout_navigation)

        self.button_back = QPushButton()
        self._layout_navigation.addWidget(self.button_back)
        self.button_back.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack))

        self.button_reload = QPushButton()
        self._layout_navigation.addWidget(self.button_reload)
        self.button_reload.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))

        self.button_forward = QPushButton()
        self._layout_navigation.addWidget(self.button_forward)
        self.button_forward.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))

        # force the navigation buttons to be on the left by adding a stretching element
        self._layout_navigation.addStretch(0)

        # web widget
        self.web_view = QWebEngineView()
        self._layout.addWidget(self.web_view, 1)

        if url is not None:
            self.web_view.load(QUrl(url))

        # loading bar
        self.progress_bar = QProgressBar()
        self._layout.addWidget(self.progress_bar, 0)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximum(100)
        self.progress_bar.hide()

        # connect the signals
        self.web_view.loadStarted.connect(self._load_started)  # NOQA: connect exist
        self.web_view.loadProgress.connect(self._load_progress)  # NOQA: connect exist
        self.web_view.loadFinished.connect(self._load_finished)  # NOQA: connect exist

        self.button_back.clicked.connect(self.back)  # NOQA: connect exist
        self.button_reload.clicked.connect(self.reload)  # NOQA: connect exist
        self.button_forward.clicked.connect(self.forward)   # NOQA: connect exist

        # finalize the initialisation
        self.refresh_navigation_actions()

    def __getattr__(self, name):
        # if the member is not found in the class, look in the web view directly
        return getattr(self.web_view, name)

    # graphical methods

    def _load_started(self):
        # update the progress bar
        self.progress_bar.setValue(0)
        self.progress_bar.show()

    def _load_progress(self, value: int):
        # update the progress bar
        self.progress_bar.setValue(value)

    def _load_finished(self):
        # update the progress bar
        self.progress_bar.hide()
        # refresh the navigation buttons
        self.refresh_navigation_actions()

    def refresh_navigation_actions(self):
        history = self.web_view.history()
        # enable the navigation button depending on the history
        self.button_back.setEnabled(history.canGoBack())
        self.button_forward.setEnabled(history.canGoForward())
