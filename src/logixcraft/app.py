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
from logixcraft.core.error_handling import install_exception_hook, install_qt_message_handler
from logixcraft.core.fonts import DEFAULT_FONT_FAMILY, FontManager
from logixcraft.core.logging_config import setup_logging
from logixcraft.core.resources import require_file
from logixcraft.core.settings import SettingsManager
from logixcraft.core.startup_validation import run_startup_validation
from logixcraft.core.theme import ThemeManager
from logixcraft.ui.main_window import MainWindow
from logixcraft.ui.splash_screen import SplashScreen


def run() -> int:
    setup_logging(LOGS_ROOT)
    install_exception_hook()
    install_qt_message_handler()
    logger = logging.getLogger(__name__)
    logger.info("Starting %s v%s", APP_NAME, APP_VERSION)

    # Load settings
    settings = SettingsManager()
    settings.load()

    # Create app
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)

    splash = SplashScreen()
    splash.show()
    splash.show_status("Validating startup environment...")
    run_startup_validation()

    splash.show_status("Loading fonts...")
    font_manager = FontManager()
    font_manager.load_fonts()
    font_family = settings.get("appearance", "font_family", default=DEFAULT_FONT_FAMILY)
    applied_font = font_manager.apply_font(app, font_family)
    if applied_font != font_family:
        settings.set("appearance", "font_family", value=applied_font)

    # Apply theme
    splash.show_status("Applying theme...")
    theme_manager = ThemeManager()
    theme_name = settings.get("appearance", "theme", default="dark")

    theme_manager.apply_theme(app, theme_name)

    app_icon = require_file(ICONS_ROOT / "app" / "logo_symbol.png", "application icon")
    app.setWindowIcon(QIcon(str(app_icon)))

    # Create main window
    splash.show_status("Opening workspace...")
    window = MainWindow(settings=settings, font_manager=font_manager)
    window.show()
    splash.finish(window.window)

    return app.exec()
