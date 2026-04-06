import logging
import sys

from PySide6.QtWidgets import QApplication

from logixcraft.core.config import LOGS_ROOT
from logixcraft.core.logging_config import setup_logging
from logixcraft.ui.main_window import MainWindow


def run() -> int:
    setup_logging(LOGS_ROOT)
    logger = logging.getLogger(__name__)
    logger.info("Starting LogixCraft")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()
