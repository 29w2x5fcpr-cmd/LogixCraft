import logging

from PySide6.QtCore import QUrl
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtWidgets import QApplication, QMenu

from logixcraft.core.config import LOGS_ROOT
from logixcraft.core.safe_call import run_safely
from logixcraft.core.theme import ThemeManager
from logixcraft.ui.about_dialog import AboutDialog
from logixcraft.ui.dialog_manager import DialogManager
from logixcraft.ui.help_viewer_dialog import HelpViewerDialog
from logixcraft.ui.license_dialog import LicenseDialog
from logixcraft.ui.settings_dialog import SettingsDialog
from logixcraft.ui.terminal_dialog import TerminalDialog

logger = logging.getLogger(__name__)


class MenuActionController:
    def __init__(self, window, settings, font_manager, dialog_manager: DialogManager) -> None:
        self.window = window
        self.settings = settings
        self.font_manager = font_manager
        self.dialog_manager = dialog_manager
        self.theme_manager = ThemeManager()

        self.menu_settings = self._require_menu("menuSettings")
        self.menu_settings.setTitle("Settings")

        self.action_preferences = self._find_preferences_action()
        self.action_terminal = self._require_action("actionTerminal")
        self.action_open_logs_folder = self._find_or_create_developer_action(
            object_name="actionOpenLogsFolder",
            text="Open Logs Folder",
        )
        self.action_license = self._require_action("actionLicense")
        self.action_help_viewer = self._find_or_create_menu_action(
            menu_object_name="menuAbout",
            object_name="actionHelpViewer",
            text="Help Viewer",
        )
        self.action_about = self._find_or_create_menu_action(
            menu_object_name="menuAbout",
            object_name="actionAbout",
            text="About LogixCraft",
        )

        self.connect_actions()

    def _require_action(self, object_name: str) -> QAction:
        action = self.window.findChild(QAction, object_name)
        if action is None:
            raise RuntimeError(f"Could not find QAction '{object_name}'")
        return action

    def _require_menu(self, object_name: str) -> QMenu:
        menu = self.window.findChild(QMenu, object_name)
        if menu is None:
            raise RuntimeError(f"Could not find QMenu '{object_name}'")
        return menu

    def _find_or_create_developer_action(self, object_name: str, text: str) -> QAction:
        return self._find_or_create_menu_action("menuDeveloper", object_name, text)

    def _find_or_create_menu_action(
        self, menu_object_name: str, object_name: str, text: str
    ) -> QAction:
        action = self.window.findChild(QAction, object_name)
        if action is not None:
            return action

        menu = self.window.findChild(QMenu, menu_object_name)
        if menu is None:
            raise RuntimeError(f"Could not find QMenu '{menu_object_name}'")

        action = QAction(text, self.window)
        action.setObjectName(object_name)
        menu.addAction(action)
        return action

    def _find_preferences_action(self) -> QAction:
        logger.info(
            "menuSettings actions: %s",
            [(action.objectName(), action.text()) for action in self.menu_settings.actions()],
        )

        action = next(
            (
                menu_action
                for menu_action in self.menu_settings.actions()
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
        self.action_preferences.triggered.connect(
            lambda: run_safely("Open Preferences", self.open_settings_dialog)
        )
        self.action_terminal.triggered.connect(
            lambda: run_safely("Open Terminal", self.open_terminal_dialog)
        )
        self.action_open_logs_folder.triggered.connect(
            lambda: run_safely("Open Logs Folder", self.open_logs_folder)
        )
        self.action_license.triggered.connect(
            lambda: run_safely("Open License", self.open_license_dialog)
        )
        self.action_help_viewer.triggered.connect(
            lambda: run_safely("Open Help Viewer", self.open_help_viewer_dialog)
        )
        self.action_about.triggered.connect(
            lambda: run_safely("Open About", self.open_about_dialog)
        )

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

    def open_logs_folder(self) -> None:
        LOGS_ROOT.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(LOGS_ROOT)))

    def open_license_dialog(self) -> None:
        self.dialog_manager.show_single("license", LicenseDialog)

    def open_help_viewer_dialog(self) -> None:
        self.dialog_manager.show_single("help_viewer", HelpViewerDialog)

    def open_about_dialog(self) -> None:
        self.dialog_manager.show_single("about", AboutDialog)
