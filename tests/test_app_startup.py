from __future__ import annotations


class FakeSettings:
    def __init__(self) -> None:
        self.values = {
            ("appearance", "font_family"): "Missing Font",
            ("appearance", "theme"): "dark",
        }
        self.loaded = False

    def load(self) -> None:
        self.loaded = True

    def get(self, *keys: str, default=None):
        return self.values.get(tuple(keys), default)

    def set(self, *keys: str, value) -> None:
        self.values[tuple(keys)] = value


class FakeApp:
    instance_ref: FakeApp | None = None

    def __init__(self, argv) -> None:
        self.argv = argv
        self.application_name = None
        self.application_version = None
        self.stylesheet = None
        self.font = None
        self.window_icon = None
        FakeApp.instance_ref = self

    @staticmethod
    def instance():
        return FakeApp.instance_ref

    @staticmethod
    def processEvents() -> None:
        return None

    def setApplicationName(self, name: str) -> None:
        self.application_name = name

    def setApplicationVersion(self, version: str) -> None:
        self.application_version = version

    def setStyleSheet(self, stylesheet: str) -> None:
        self.stylesheet = stylesheet

    def setFont(self, font) -> None:
        self.font = font

    def setWindowIcon(self, icon) -> None:
        self.window_icon = icon

    def exec(self) -> int:
        return 23


class FakeSplash:
    def __init__(self) -> None:
        self.messages: list[str] = []
        self.finished_with = None

    def show(self) -> None:
        return None

    def show_status(self, message: str) -> None:
        self.messages.append(message)

    def finish(self, window) -> None:
        self.finished_with = window


class FakeFontManager:
    def __init__(self) -> None:
        self.loaded = False

    def load_fonts(self) -> None:
        self.loaded = True

    def apply_font(self, app, family: str | None) -> str:
        app.applied_font_request = family
        return "Roboto"


class FakeThemeManager:
    def apply_theme(self, app, theme_name: str) -> None:
        app.applied_theme = theme_name
        app.setStyleSheet("theme applied")


class FakeMainWindow:
    def __init__(self, settings, font_manager) -> None:
        self.settings = settings
        self.font_manager = font_manager
        self.window = object()
        self.shown = False

    def show(self) -> None:
        self.shown = True


def test_app_run_performs_basic_startup_sequence(monkeypatch, tmp_path) -> None:
    from logixcraft import app as app_module
    from logixcraft.core.config import APP_NAME, APP_VERSION

    created = {}

    def fake_setup_logging(logs_root) -> None:
        created["logs"] = logs_root

    def fake_install_exception_hook() -> None:
        created["exception_hook"] = True

    def fake_install_qt_message_handler() -> None:
        created["qt_hook"] = True

    def fake_settings_manager() -> FakeSettings:
        return created.setdefault("settings", FakeSettings())

    def fake_splash_screen() -> FakeSplash:
        return created.setdefault("splash", FakeSplash())

    def fake_startup_validation() -> None:
        created["validated"] = True

    def fake_font_manager() -> FakeFontManager:
        return created.setdefault("fonts", FakeFontManager())

    monkeypatch.setattr(app_module, "LOGS_ROOT", tmp_path / "logs")
    monkeypatch.setattr(app_module, "setup_logging", fake_setup_logging)
    monkeypatch.setattr(app_module, "install_exception_hook", fake_install_exception_hook)
    monkeypatch.setattr(app_module, "install_qt_message_handler", fake_install_qt_message_handler)
    monkeypatch.setattr(app_module, "SettingsManager", fake_settings_manager)
    monkeypatch.setattr(app_module, "QApplication", FakeApp)
    monkeypatch.setattr(app_module, "SplashScreen", fake_splash_screen)
    monkeypatch.setattr(app_module, "run_startup_validation", fake_startup_validation)
    monkeypatch.setattr(app_module, "FontManager", fake_font_manager)
    monkeypatch.setattr(app_module, "ThemeManager", lambda: FakeThemeManager())
    monkeypatch.setattr(app_module, "require_file", lambda path, description: path)
    monkeypatch.setattr(app_module, "QIcon", lambda path: f"icon:{path}")
    monkeypatch.setattr(
        app_module,
        "MainWindow",
        lambda settings, font_manager: created.setdefault(
            "window", FakeMainWindow(settings, font_manager)
        ),
    )

    exit_code = app_module.run()

    fake_app = FakeApp.instance_ref
    assert exit_code == 23
    assert created["logs"] == tmp_path / "logs"
    assert created["exception_hook"] is True
    assert created["qt_hook"] is True
    assert created["settings"].loaded is True
    assert created["validated"] is True
    assert created["fonts"].loaded is True
    assert created["settings"].get("appearance", "font_family") == "Roboto"
    assert created["window"].shown is True
    assert created["splash"].finished_with is created["window"].window
    assert fake_app.application_name == APP_NAME
    assert fake_app.application_version == APP_VERSION
    assert fake_app.applied_theme == "dark"
    assert fake_app.stylesheet == "theme applied"
    assert fake_app.window_icon is not None
