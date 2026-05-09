from logixcraft.core.theme.stylesheet import build_stylesheet
from logixcraft.core.theme.themes import ALL_THEMES, LIGHT_THEME


class ThemeManager:
    def __init__(self) -> None:
        self._themes = ALL_THEMES

    def apply_theme(self, app, theme_name: str) -> None:
        theme = self._themes.get(theme_name, LIGHT_THEME)
        app.setStyleSheet(build_stylesheet(theme))

    def get_theme(self, theme_name: str) -> dict:
        return self._themes.get(theme_name, LIGHT_THEME)

    def available_themes(self) -> list[str]:
        return list(self._themes.keys())

    def has_theme(self, theme_name: str) -> bool:
        return theme_name in self._themes
