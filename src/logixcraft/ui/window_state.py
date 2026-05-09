import logging

logger = logging.getLogger(__name__)


class WindowState:
    def __init__(self, window, settings) -> None:
        self.window = window
        self.settings = settings

    def restore_size(self) -> None:
        width = self.settings.get("window", "width", default=1200)
        height = self.settings.get("window", "height", default=800)
        self.window.resize(width, height)

    def save_size(self) -> None:
        width = self.window.width()
        height = self.window.height()

        self.settings.set("window", "width", value=width)
        self.settings.set("window", "height", value=height)
        self.settings.save()

        logger.info("Saved window size: %sx%s", width, height)
