from logixcraft.core.config import PROJECT_ROOT, SETTINGS_FILE
from logixcraft.core.settings import SettingsManager
from logixcraft.core.settings.defaults import DEFAULT_SETTINGS


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


def test_corrupted_settings_file_is_backed_up_before_defaults_are_saved(tmp_path) -> None:
    settings_file = tmp_path / "settings.json"
    settings_file.write_text("{not valid json", encoding="utf-8")

    settings = SettingsManager(settings_file=settings_file)
    settings.load()

    backups = list(tmp_path.glob("settings.corrupt-*.json"))
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == "{not valid json"
    assert settings.get("appearance", "theme") == DEFAULT_SETTINGS["appearance"]["theme"]

    recovered = SettingsManager(settings_file=settings_file)
    recovered.load()
    assert recovered.get("appearance", "theme") == DEFAULT_SETTINGS["appearance"]["theme"]


def test_invalid_settings_root_is_backed_up_before_defaults_are_saved(tmp_path) -> None:
    settings_file = tmp_path / "settings.json"
    settings_file.write_text("[1, 2, 3]", encoding="utf-8")

    settings = SettingsManager(settings_file=settings_file)
    settings.load()

    backups = list(tmp_path.glob("settings.corrupt-*.json"))
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == "[1, 2, 3]"
