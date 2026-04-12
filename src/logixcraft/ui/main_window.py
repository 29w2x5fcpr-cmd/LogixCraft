import logging

from pathlib import Path
from functools import partial

from PySide6.QtCore import QFile, QIODevice, QObject, QEvent, Qt, QSize
from PySide6.QtGui import QAction, QIcon, QPixmap, QFontDatabase, QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QLabel, QPushButton, QMenu, QStatusBar, QStackedWidget, QWidget

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

        self.btnHome = self.window.findChild(QPushButton, "btnHome")

        self.homeAppVersion.setText(f"v{APP_VERSION}")

        self.btnHome = self.window.findChild(QPushButton, "btnHome")
        self.btnPLC = self.window.findChild(QPushButton, "btnPLC")

        self.sidebarStack = self.window.findChild(QStackedWidget, "sidebarStack")
        self.mainStack = self.window.findChild(QStackedWidget, "mainStack")

        self.page_sidebar_home = self.window.findChild(QWidget, "page_sidebar_home")
        self.page_main_home = self.window.findChild(QWidget, "page_main_home")

        self.page_sidebar_plc = self.window.findChild(QWidget, "page_sidebar_plc")
        self.page_main_plc = self.window.findChild(QWidget, "page_main_plc")

        self.nav_config = {
            "home": {
                "button": self.btnHome,
                "sidebar_page": self.page_sidebar_home,
                "main_page": self.page_main_home,
                "active": True,
            },
            "plc": {
                "button": self.btnPLC,
                "sidebar_page": self.page_sidebar_plc,
                "main_page": self.page_main_plc,
                "active": True,
            },
        }
        self.connect_navigation()
        image_path = ASSETS_ROOT / "icons" / "app" / "logo.png"

        self.btnHome.setText("")
        self.btnHome.setIcon(QIcon(str(ASSETS_ROOT / "icons" / "app" / "logo_symbol.png")))
        self.btnHome.setIconSize(QSize(25, 25))
        pixmap = QPixmap(str(image_path))
        self.homeImage.setPixmap(
            pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.action_preferences.triggered.connect(self.open_settings_dialog)
        self.window.installEventFilter(self)
        self.navigate("home")
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

    def show_home_page(self) -> None:
        self.sidebarStack.setCurrentWidget(self.page_sidebar_home)
        self.mainStack.setCurrentWidget(self.page_main_home)

        if self.status_bar is not None:
            self.status_bar.showMessage("Home page opened", 3000)

    def show_plc_page(self) -> None:
        self.sidebarStack.setCurrentWidget(self.page_sidebar_plc)
        self.mainStack.setCurrentWidget(self.page_main_plc)
        self.set_active_button(self.btnPLC)
        if self.status_bar is not None:
            self.status_bar.showMessage("PLC page opened", 3000)

    def validate_nav_config(self) -> None:
        missing = []

        for key, item in self.nav_config.items():
            for field in ("button", "sidebar_page", "main_page"):
                if item.get(field) is None:
                    missing.append(f"{key}.{field}")

        if self.sidebarStack is None:
            missing.append("sidebarStack")

        if self.mainStack is None:
            missing.append("mainStack")

        if missing:
            raise RuntimeError(f"Missing navigation UI widgets: {', '.join(missing)}")

    def connect_navigation(self) -> None:
        for key, item in self.nav_config.items():
            button = item["button"]
            button.clicked.connect(partial(self.navigate, key))

    def reset_active_buttons(self) -> None:
        for item in self.nav_config.values():
            button = item["button"]
            button.setProperty("active", False)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

    def set_active_button(self, button: QPushButton) -> None:
        self.reset_active_buttons()

        button.setProperty("active", True)
        button.style().unpolish(button)
        button.style().polish(button)
        button.update()

    def navigate(self, key: str) -> None:
        item = self.nav_config[key]

        sidebar_page = item["sidebar_page"]
        main_page = item["main_page"]
        button = item["button"]
        should_activate = item.get("active", True)

        self.sidebarStack.setCurrentWidget(sidebar_page)
        self.mainStack.setCurrentWidget(main_page)

        if should_activate:
            self.set_active_button(button)
        else:
            self.reset_active_buttons()

        if self.status_bar is not None:
            self.status_bar.showMessage(f"Opened {key}", 3000)
