import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMenu

from logixcraft.ui.dialog_manager import DialogManager
from logixcraft.ui.menu_actions import MenuActionController


class FakeSettings:
    def get(self, *_keys, default=None):
        return default


class FakeFontManager:
    def available_families(self) -> list[str]:
        return ["Roboto"]


def build_window_with_menus() -> QMainWindow:
    window = QMainWindow()
    menu_bar = window.menuBar()

    menu_settings = QMenu("Settings", window)
    menu_settings.setObjectName("menuSettings")
    action_preferences = menu_settings.addAction("Preferences")
    action_preferences.setObjectName("actionPreferences")
    menu_bar.addMenu(menu_settings)

    menu_developer = QMenu("Developer", window)
    menu_developer.setObjectName("menuDeveloper")
    action_terminal = menu_developer.addAction("Terminal")
    action_terminal.setObjectName("actionTerminal")
    menu_bar.addMenu(menu_developer)

    menu_about = QMenu("About", window)
    menu_about.setObjectName("menuAbout")
    action_license = menu_about.addAction("License")
    action_license.setObjectName("actionLicense")
    action_software = menu_about.addAction("Software")
    action_software.setObjectName("actionSoftware")
    menu_bar.addMenu(menu_about)

    return window


def test_menu_actions_adds_open_logs_folder_action() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    window = build_window_with_menus()

    controller = MenuActionController(
        window=window,
        settings=FakeSettings(),
        font_manager=FakeFontManager(),
        dialog_manager=DialogManager(parent=window),
    )

    assert controller.action_open_logs_folder.objectName() == "actionOpenLogsFolder"
    assert controller.action_open_logs_folder.text() == "Open Logs Folder"
    assert app is not None


def test_open_logs_folder_creates_directory(monkeypatch, tmp_path) -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    window = build_window_with_menus()
    opened_urls = []

    controller = MenuActionController(
        window=window,
        settings=FakeSettings(),
        font_manager=FakeFontManager(),
        dialog_manager=DialogManager(parent=window),
    )

    monkeypatch.setattr("logixcraft.ui.menu_actions.LOGS_ROOT", tmp_path / "logs")
    monkeypatch.setattr(
        "logixcraft.ui.menu_actions.QDesktopServices.openUrl",
        lambda url: opened_urls.append(url),
    )

    controller.open_logs_folder()

    assert (tmp_path / "logs").is_dir()
    assert opened_urls
    assert app is not None
