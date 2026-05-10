from logixcraft.core.fonts import DEFAULT_FONT_FAMILY, FALLBACK_FONT_FAMILY, FontManager


def test_font_manager_includes_system_default() -> None:
    font_manager = FontManager()

    assert DEFAULT_FONT_FAMILY in font_manager.available_families()
    assert font_manager.has_family(DEFAULT_FONT_FAMILY)
    assert FALLBACK_FONT_FAMILY in font_manager.available_families()
    assert font_manager.has_family(FALLBACK_FONT_FAMILY)


def test_font_manager_resolves_invalid_font_to_default() -> None:
    font_manager = FontManager()

    assert font_manager.resolve_family("Missing Font") == DEFAULT_FONT_FAMILY


def test_font_manager_sorts_preferred_fonts_first() -> None:
    sorted_families = FontManager._sort_families(
        {"Zed Font", FALLBACK_FONT_FAMILY, DEFAULT_FONT_FAMILY}
    )

    assert sorted_families[:2] == [DEFAULT_FONT_FAMILY, FALLBACK_FONT_FAMILY]


def test_font_manager_load_fonts_returns_result_without_font_root(tmp_path) -> None:
    font_manager = FontManager(fonts_root=tmp_path / "missing")

    result = font_manager.load_fonts()

    assert result.loaded_files == []
    assert result.failed_files == []
    assert DEFAULT_FONT_FAMILY in result.families
