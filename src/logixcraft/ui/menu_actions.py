import logging

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu

from logixcraft.core.theme import ThemeManager
from logixcraft.ui.dialog_manager import DialogManager
from logixcraft.ui.license_dialog import LicenseDialog
from logixcraft.ui.settings_dialog import SettingsDialog
from logixcraft.ui.software_dialog import SoftwareDialog
from logixcraft.ui.terminal_dialog import TerminalDialog

logger = logging.getLogger(__name__)


class MenuActionController:
    def __init__(self, window, settings, font_manager, dialog_manager: DialogManager) -> None:
        self.window = window
        self.settings = settings
        self.font_manager = font_manager
        self.dialog_manager = dialog_manager
        self.theme_manager = ThemeManager()

        self.action_preferences = self._find_preferences_action()
        self.action_terminal = self._require_action("actionTerminal")
        self.action_license = self._require_action("actionLicense")
        self.action_software = self._require_action("actionSoftware")

        self.connect_actions()

    def _require_action(self, object_name: str) -> QAction:
        action = self.window.findChild(QAction, object_name)
        if action is None:
            raise RuntimeError(f"Could not find QAction '{object_name}'")
        return action

    def _find_preferences_action(self) -> QAction:
        menu_settings = self.window.findChild(QMenu, "menuSettings")
        if menu_settings is None:
            raise RuntimeError("Could not find QMenu 'menuSettings'")

        logger.info(
            "menuSettings actions: %s",
            [(action.objectName(), action.text()) for action in menu_settings.actions()],
        )

        action = next(
            (
                menu_action
                for menu_action in menu_settings.actions()
                if menu_action.objectName() == "actionPreferences"
            ),
            None,
        )

        if action is not None:
            return action

        all_actions = self.window.findChildren(QAction)
        logger.info(
            "all window actions: %s",
            [(window_action.objectName(), window_action.text()) for window_action in all_actions],
        )

        action = next(
            (
                window_action
                for window_action in all_actions
                if window_action.objectName() == "actionPreferences"
                or window_action.text().replace("&", "") == "Preferences"
            ),
            None,
        )

        if action is None:
            raise RuntimeError(
                "Could not find QAction 'actionPreferences'. "
                "Check the QAction objectName in Qt Designer."
            )

        return action

    def connect_actions(self) -> None:
        self.action_preferences.triggered.connect(self.open_settings_dialog)
        self.action_terminal.triggered.connect(self.open_terminal_dialog)
        self.action_license.triggered.connect(self.open_license_dialog)
        self.action_software.triggered.connect(self.open_software_dialog)

    def open_settings_dialog(self) -> None:
        dialog = SettingsDialog(
            settings=self.settings,
            theme_manager=self.theme_manager,
            font_manager=self.font_manager,
            parent=self.window,
        )

        if dialog.exec():
            theme = self.settings.get("appearance", "theme", default="dark")

            app = QApplication.instance()
            if app is not None:
                self.theme_manager.apply_theme(app, theme)
                logger.info("Re-applied app theme after settings dialog: %s", theme)

            width = self.settings.get("window", "width", default=1200)
            height = self.settings.get("window", "height", default=800)
            self.window.resize(width, height)

    def open_terminal_dialog(self) -> None:
        self.dialog_manager.show_single("terminal", TerminalDialog)

    def open_license_dialog(self) -> None:
        self.dialog_manager.show_single("license", LicenseDialog)

    def open_software_dialog(self) -> None:
        self.dialog_manager.show_single("software", SoftwareDialog)
