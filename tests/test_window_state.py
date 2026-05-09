from logixcraft.core.settings import SettingsManager
from logixcraft.ui.window_state import WindowState


class FakeWindow:
    def __init__(self) -> None:
        self._width = 0
        self._height = 0

    def resize(self, width: int, height: int) -> None:
        self._width = width
        self._height = height

    def width(self) -> int:
        return self._width

    def height(self) -> int:
        return self._height


def test_window_state_restores_and_saves_size(tmp_path) -> None:
    settings = SettingsManager(settings_file=tmp_path / "settings.json")
    settings.set("window", "width", value=900)
    settings.set("window", "height", value=700)

    window = FakeWindow()
    window_state = WindowState(window=window, settings=settings)
    window_state.restore_size()

    assert window.width() == 900
    assert window.height() == 700

    window.resize(1000, 750)
    window_state.save_size()

    assert settings.get("window", "width") == 1000
    assert settings.get("window", "height") == 750
