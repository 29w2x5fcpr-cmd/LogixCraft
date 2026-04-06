import logging

from PySide6.QtCore import QFile, QIODevice, QObject, QEvent
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QLabel, QPushButton, QMenu

from logixcraft.core.config import APP_NAME, APP_VERSION, MAIN_WINDOW_UI
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

        self.label_status = self.window.findChild(QLabel, "label_status")
        self.button_test = self.window.findChild(QPushButton, "button_test")
        self.action_test_tools = self.window.findChild(QAction, "action_test_tools")

        self.menu_settings = self.window.findChild(QMenu, "menuSettings")
        if self.menu_settings is None:
            raise RuntimeError("Could not find QMenu 'menuSettings'")

        self.action_preferences = None
        for action in self.menu_settings.actions():
            if action.objectName() == "actionPreferences":
                self.action_preferences = action
                break

        if self.action_preferences is None:
            raise RuntimeError("Could not find QAction 'actionPreferences' inside 'menuSettings'")

        if self.label_status is None:
            raise RuntimeError("Could not find QLabel with objectName 'label_status'")
        if self.button_test is None:
            raise RuntimeError("Could not find QPushButton with objectName 'button_test'")
        if self.action_test_tools is None:
            raise RuntimeError("Could not find QAction with objectName 'action_test_tools'")

        self.button_test.clicked.connect(self.on_test_clicked)
        self.action_test_tools.triggered.connect(self.on_test_tools_triggered)
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

    def on_test_clicked(self) -> None:
        result = self.controller.handle_test_button()
        self.label_status.setText(result)

    def on_test_tools_triggered(self) -> None:
        result = self.controller.handle_test_button()
        self.label_status.setText(f"Menu triggered: {result}")

    def show(self) -> None:
        self.window.show()

    def open_settings_dialog(self):
        dialog = SettingsDialog(
            settings=self.settings, theme_manager=self.theme_manager, parent=self.window
        )

        if dialog.exec():
            from PySide6.QtWidgets import QApplication

            theme = self.settings.get("appearance", "theme", default="dark")

            app = QApplication.instance()
            if app:
                self.theme_manager.apply_theme(app, theme)

            width = self.settings.get("window", "width", default=1200)
            height = self.settings.get("window", "height", default=800)
            self.window.resize(width, height)
