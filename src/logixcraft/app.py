import logging
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from logixcraft.core.config import (
    APP_NAME,
    APP_VERSION,
    ICONS_ROOT,
    LOGS_ROOT,
)
from logixcraft.core.fonts import FontManager
from logixcraft.core.logging_config import setup_logging
from logixcraft.core.settings import SettingsManager
from logixcraft.core.theme import ThemeManager
from logixcraft.ui.main_window import MainWindow


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

    font_manager = FontManager()
    font_manager.load_fonts()
    font_family = settings.get("appearance", "font_family", default="Segoe UI")
    applied_font = font_manager.apply_font(app, font_family)
    if applied_font != font_family:
        settings.set("appearance", "font_family", value=applied_font)

    # Apply theme
    theme_manager = ThemeManager()
    theme_name = settings.get("appearance", "theme", default="dark")

    theme_manager.apply_theme(app, theme_name)

    app_icon = ICONS_ROOT / "app" / "logo_symbol.png"
    app.setWindowIcon(QIcon(str(app_icon)))

    # Create main window
    window = MainWindow(settings=settings, font_manager=font_manager)
    window.show()

    return app.exec()
