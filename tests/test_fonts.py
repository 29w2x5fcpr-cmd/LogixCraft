from logixcraft.core.fonts import FontManager


def test_font_manager_includes_system_default() -> None:
    font_manager = FontManager()

    assert "Roboto" in font_manager.available_families()
    assert font_manager.has_family("Roboto")
    assert "Segoe UI" in font_manager.available_families()
    assert font_manager.has_family("Segoe UI")
