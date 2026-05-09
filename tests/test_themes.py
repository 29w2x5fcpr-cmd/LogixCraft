from logixcraft.core.theme.manager import ThemeManager
from logixcraft.core.theme.stylesheet import build_stylesheet
from logixcraft.core.theme.themes import ALL_THEMES, DARK_THEME


def test_theme_catalog_has_at_least_ten_themes() -> None:
    theme_manager = ThemeManager()

    assert len(theme_manager.available_themes()) >= 10


def test_theme_token_groups_match() -> None:
    reference = DARK_THEME

    for theme in ALL_THEMES.values():
        assert theme.keys() == reference.keys()

        for group in ("color", "radius", "size", "font"):
            assert theme[group].keys() == reference[group].keys()


def test_stylesheet_uses_theme_tokens() -> None:
    stylesheet = build_stylesheet(DARK_THEME)

    assert DARK_THEME["color"]["panel_bg_emphasis"] in stylesheet
    assert DARK_THEME["radius"]["navbar"] in stylesheet
    assert DARK_THEME["size"]["home_button"] in stylesheet
    assert DARK_THEME["font"]["nav_button_size"] in stylesheet
    assert "QWidget#centralwidget" in stylesheet


def test_all_themes_render_stylesheets() -> None:
    for theme in ALL_THEMES.values():
        stylesheet = build_stylesheet(theme)

        assert theme["color"]["app_bg"] in stylesheet
        assert theme["color"]["panel_bg_emphasis"] in stylesheet
        assert theme["radius"]["navbar"] in stylesheet
