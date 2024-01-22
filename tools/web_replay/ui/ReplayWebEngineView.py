from datetime import datetime
from typing import Optional

from PyQt6.QtCore import QObject, QEvent, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView


class ReplayWebEngineView(QWebEngineView):
    def __init__(self, start_time: datetime):
        super().__init__()

        self.start_time = start_time
        self._last_url: Optional[QUrl] = None

        self.loadFinished.connect(self._initialize_proxy_event)  # NOQA: connect exist

    # event filter

    def setUrl(self, url: QUrl, archive: bool = True) -> None:
        if archive:
            # get the archive.org link corresponding to that time
            archive_time: str = self.start_time.strftime("%Y%m%d%H%M%S")
            url = QUrl(f"https://web.archive.org/web/{archive_time}/{url.toString()}")

        self._last_url = url

        # call the super function with the archive url instead
        super().setUrl(url)

        # clean the archive header popup that will appear
        self.loadFinished.connect(self._on_load_finished)  # NOQA: connect exist

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        match event.type():
            # allow scroll events (they are created automatically)
            case event.Type.Scroll:
                pass

            # allow timed events
            case event.Type.Timer:
                pass

            # ignore all other events
            case _:
                if not getattr(event, "custom", False):
                    return True

        return super().eventFilter(obj, event)

    # events

    def _initialize_proxy_event(self):
        # make self.eventFilter intercept all focusProxy events
        self.focusProxy().installEventFilter(self)

    def _on_load_finished(self, ok: bool):
        # prevent the event from being enabled another time
        self.loadFinished.disconnect(self._on_load_finished)  # NOQA: disconnect exist

        if ok:
            # hide archive.org header to avoid mouse movement being shifted
            self.page().runJavaScript("document.getElementById('wm-ipp-base').style.display = 'none';")
            self._initialize_proxy_event()

        else:
            self.setUrl(self._last_url, archive=False)
