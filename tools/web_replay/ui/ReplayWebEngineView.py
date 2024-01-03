from datetime import datetime

from PyQt6.QtCore import QObject, QEvent, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView


class ReplayWebEngineView(QWebEngineView):
    def __init__(self, start_time: datetime):
        super().__init__()

        self.start_time = start_time

        self.loadFinished.connect(self._initialize_proxy_event)  # NOQA: connect exist

    # event filter

    def setUrl(self, url: QUrl) -> None:
        # get the archive.org link corresponding to that time
        archive_time: str = self.start_time.strftime("%Y%m%d%H%M%S")
        archive_url = f"https://web.archive.org/web/{archive_time}/{url.toString()}"

        # call the super function with the archive url instead
        super().setUrl(QUrl(archive_url))

        # clean the archive header popup that will appear
        self.loadFinished.connect(self._clean_archive_header)  # NOQA: connect exist

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

    def _initialize_proxy_event(self, ok: bool):
        # prevent the event from being enabled another time
        self.loadFinished.disconnect(self._initialize_proxy_event)  # NOQA: disconnect exist

        # make self.eventFilter intercept all focusProxy events
        self.focusProxy().installEventFilter(self)

    def _clean_archive_header(self, ok: bool):
        # prevent the event from being enabled another time
        self.loadFinished.disconnect(self._clean_archive_header)  # NOQA: disconnect exist

        # hide archive.org header to avoid mouse movement being shifted
        self.page().runJavaScript("document.getElementById('wm-ipp-base').style.display = 'none';")
