from logixcraft.core.config import PROJECT_ROOT, SETTINGS_FILE
from logixcraft.core.settings import SettingsManager


def test_runtime_settings_file_is_outside_project_root() -> None:
    assert not SETTINGS_FILE.is_relative_to(PROJECT_ROOT)


def test_settings_manager_saves_to_configured_file(tmp_path) -> None:
    settings_file = tmp_path / "settings.json"
    settings = SettingsManager(settings_file=settings_file)

    settings.set("appearance", "theme", value="graphite")
    settings.save()

    loaded = SettingsManager(settings_file=settings_file)
    loaded.load()

    assert loaded.get("appearance", "theme") == "graphite"
