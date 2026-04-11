import logging
import sys

from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QAction, QIcon, QPixmap, QFontDatabase, QFont
from logixcraft.core.config import APP_NAME, APP_VERSION, LOGS_ROOT
from logixcraft.core.logging_config import setup_logging
from logixcraft.core.settings import SettingsManager
from logixcraft.core.theme import ThemeManager
from logixcraft.ui.main_window import MainWindow

from logixcraft.core.config import (
    APP_NAME,
    APP_VERSION,
    PROJECT_ROOT,
    ASSETS_ROOT,
    ICONS_ROOT,
    MAIN_WINDOW_UI,
    NAV_BUTTONS,
)


def run() -> int:
    setup_logging(LOGS_ROOT)
    logger = logging.getLogger(__name__)
    logger.info("Starting %s v%s", APP_NAME, APP_VERSION)

    # Load settings
    settings = SettingsManager()
    settings.load()

    # Create app
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)

    # Apply theme
    theme_manager = ThemeManager()
    theme_name = settings.get("appearance", "theme", default="dark")

    theme_manager.apply_theme(app, theme_name)

    app_icon = ICONS_ROOT / "app" / "logo_symbol.png"
    app.setWindowIcon(QIcon(str(app_icon)))

    # Create main window
    window = MainWindow(settings=settings)
    window.show()

    return app.exec()
