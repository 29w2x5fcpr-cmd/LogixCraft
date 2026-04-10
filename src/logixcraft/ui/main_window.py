import logging

from pathlib import Path

from PySide6.QtCore import QFile, QIODevice, QObject, QEvent, Qt
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QLabel, QPushButton, QMenu, QStatusBar

from logixcraft.core.config import (
    APP_NAME,
    APP_VERSION,
    PROJECT_ROOT,
    ASSETS_ROOT,
    ICONS_ROOT,
    MAIN_WINDOW_UI,
    NAV_BUTTONS,
)
from logixcraft.core.controller import AppController
from logixcraft.core.theme import ThemeManager
from logixcraft.ui.settings_dialog import SettingsDialog

logger = logging.getLogger(__name__)


class MainWindow(QObject):
    def __init__(self, settings) -> None:
        super().__init__()
        self.settings = settings
        self.theme_manager = ThemeManager()

        loader = QUiLoader()
        ui_file = QFile(str(MAIN_WINDOW_UI))
        self.controller = AppController()

        if not ui_file.open(QIODevice.ReadOnly):
            raise RuntimeError(f"Could not open UI file: {MAIN_WINDOW_UI}")

        self.window = loader.load(ui_file)
        ui_file.close()

        if self.window is None:
            raise RuntimeError(f"Could not load UI file: {MAIN_WINDOW_UI}")

        self.window.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")

        width = self.settings.get("window", "width", default=1200)
        height = self.settings.get("window", "height", default=800)
        self.window.resize(width, height)

        base_dir = Path(__file__).resolve().parents[1]
        app_icon = base_dir / "assets" / "icons" / "app" / "app.ico"

        self.menu_settings = self.window.findChild(QMenu, "menuSettings")
        if self.menu_settings is None:
            raise RuntimeError("Could not find QMenu 'menuSettings'")

        logger.info(
            "menuSettings actions: %s",
            [(a.objectName(), a.text()) for a in self.menu_settings.actions()],
        )

        self.action_preferences = next(
            (a for a in self.menu_settings.actions() if a.objectName() == "actionPreferences"),
            None,
        )

        if self.action_preferences is None:
            all_actions = self.window.findChildren(QAction)
            logger.info(
                "all window actions: %s",
                [(a.objectName(), a.text()) for a in all_actions],
            )

            self.action_preferences = next(
                (
                    a
                    for a in all_actions
                    if a.objectName() == "actionPreferences"
                    or a.text().replace("&", "") == "Preferences"
                ),
                None,
            )

        if self.action_preferences is None:
            raise RuntimeError(
                "Could not find QAction 'actionPreferences'. Check the QAction objectName in Qt Designer."
            )

        self.status_bar = self.window.findChild(QStatusBar, "statusbar")
        print("statusbar:", self.status_bar)
        if self.status_bar is not None:
            self.status_bar.showMessage("Ready")

        self.homeImage = self.window.findChild(QLabel, "homeImage")
        self.homeTitle = self.window.findChild(QLabel, "homeTitle")
        self.homeAppVersion = self.window.findChild(QLabel, "homeAppVersion")

        self.homeAppVersion.setText(f"v{APP_VERSION}")

        image_path = ASSETS_ROOT / "icons" / "app" / "logo.png"
        self.ui.btnHome.setIcon(QIcon(str(NAV_BUTTONS / "home.svg")))

        pixmap = QPixmap(str(image_path))
        self.homeImage.setPixmap(
            pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.action_preferences.triggered.connect(self.open_settings_dialog)
        self.window.installEventFilter(self)

        logger.info("Main window initialized")

    def eventFilter(self, obj, event):
        if obj == self.window and event.type() == QEvent.Close:
            width = self.window.width()
            height = self.window.height()

            self.settings.set("window", "width", value=width)
            self.settings.set("window", "height", value=height)
            self.settings.save()

            logger.info("Saved window size: %sx%s", width, height)

        return super().eventFilter(obj, event)

    def show(self) -> None:
        self.window.show()

    def open_settings_dialog(self):
        dialog = SettingsDialog(
            settings=self.settings,
            theme_manager=self.theme_manager,
            parent=self.window,
        )

        if dialog.exec():
            from PySide6.QtWidgets import QApplication

            theme = self.settings.get("appearance", "theme", default="dark")

            app = QApplication.instance()
            if app is not None:
                self.theme_manager.apply_theme(app, theme)
                logger.info("Re-applied app theme after settings dialog: %s", theme)

            width = self.settings.get("window", "width", default=1200)
            height = self.settings.get("window", "height", default=800)
            self.window.resize(width, height)
