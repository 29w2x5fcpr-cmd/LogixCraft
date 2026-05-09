import logging
from pathlib import Path

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from logixcraft.core.config import FONTS_ROOT

logger = logging.getLogger(__name__)


class FontManager:
    def __init__(self, fonts_root: Path = FONTS_ROOT) -> None:
        self.fonts_root = fonts_root
        self._families = ["Roboto", "Segoe UI"]

    def load_fonts(self) -> None:
        if not self.fonts_root.exists():
            logger.warning("Fonts root does not exist: %s", self.fonts_root)
            return

        families = set(self._families)

        for font_file in self.fonts_root.rglob("*.ttf"):
            font_id = QFontDatabase.addApplicationFont(str(font_file))
            if font_id == -1:
                logger.warning("Could not load font: %s", font_file)
                continue

            families.update(QFontDatabase.applicationFontFamilies(font_id))

        self._families = sorted(families, key=str.casefold)
        logger.info("Loaded application fonts: %s", ", ".join(self._families))

    def available_families(self) -> list[str]:
        return list(self._families)

    def has_family(self, family: str) -> bool:
        return family in self._families

    def apply_font(self, app: QApplication, family: str, point_size: int = 10) -> str:
        selected_family = family if self.has_family(family) else self._families[0]
        app.setFont(QFont(selected_family, point_size))
        return selected_family
