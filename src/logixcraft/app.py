import logging
import sys

from PySide6.QtWidgets import QApplication

from logixcraft.core.config import APP_NAME, APP_VERSION, LOGS_ROOT
from logixcraft.core.logging_config import setup_logging
from logixcraft.core.settings import SettingsManager
from logixcraft.ui.main_window import MainWindow


def run() -> int:
    setup_logging(LOGS_ROOT)
    logger = logging.getLogger(__name__)
    logger.info("Starting %s v%s", APP_NAME, APP_VERSION)

    settings = SettingsManager()
    settings.load()

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)

    window = MainWindow(settings=settings)
    window.show()

    return app.exec()
