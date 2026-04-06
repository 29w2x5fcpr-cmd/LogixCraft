import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication

from logixcraft.core.config import UI_ROOT

logger = logging.getLogger(__name__)


class ThemeManager:
    def __init__(self) -> None:
        self.themes_dir = UI_ROOT / "themes"

    def apply_theme(self, app: QApplication, theme_name: str) -> None:
        theme_file = self.themes_dir / f"{theme_name}.qss"

        if not theme_file.exists():
            logger.warning("Theme file not found: %s", theme_file)
            app.setStyleSheet("")
            return

        stylesheet = theme_file.read_text(encoding="utf-8")
        app.setStyleSheet(stylesheet)
        logger.info("Applied theme: %s", theme_name)

    def theme_exists(self, theme_name: str) -> bool:
        return (self.themes_dir / f"{theme_name}.qss").exists()

    def available_themes(self) -> list[str]:
        if not self.themes_dir.exists():
            return []
        return sorted(path.stem for path in self.themes_dir.glob("*.qss"))
