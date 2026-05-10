import logging
from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from logixcraft.core.config import FONTS_ROOT

logger = logging.getLogger(__name__)

DEFAULT_FONT_FAMILY = "Roboto"
FALLBACK_FONT_FAMILY = "Segoe UI"
DEFAULT_FONT_POINT_SIZE = 10


@dataclass
class FontLoadResult:
    loaded_files: list[Path] = field(default_factory=list)
    failed_files: list[Path] = field(default_factory=list)
    families: list[str] = field(default_factory=list)


class FontManager:
    def __init__(self, fonts_root: Path = FONTS_ROOT) -> None:
        self.fonts_root = fonts_root
        self._families = [DEFAULT_FONT_FAMILY, FALLBACK_FONT_FAMILY]
        self._loaded_files: set[Path] = set()

    def load_fonts(self) -> FontLoadResult:
        result = FontLoadResult()
        if not self.fonts_root.exists():
            logger.warning("Fonts root does not exist: %s", self.fonts_root)
            result.families = self.available_families()
            return result

        families = set(self._families)

        for font_file in self.fonts_root.rglob("*.ttf"):
            font_file = font_file.resolve()
            if font_file in self._loaded_files:
                continue

            font_id = QFontDatabase.addApplicationFont(str(font_file))
            if font_id == -1:
                logger.warning("Could not load font: %s", font_file)
                result.failed_files.append(font_file)
                continue

            self._loaded_files.add(font_file)
            result.loaded_files.append(font_file)
            families.update(QFontDatabase.applicationFontFamilies(font_id))

        self._families = self._sort_families(families)
        result.families = self.available_families()
        logger.info("Loaded application fonts: %s", ", ".join(self._families))
        return result

    def available_families(self) -> list[str]:
        return list(self._families)

    def has_family(self, family: str) -> bool:
        return family in self._families

    def resolve_family(self, family: str | None) -> str:
        if family and self.has_family(family):
            return family
        if self.has_family(DEFAULT_FONT_FAMILY):
            return DEFAULT_FONT_FAMILY
        if self.has_family(FALLBACK_FONT_FAMILY):
            return FALLBACK_FONT_FAMILY
        return self._families[0]

    def apply_font(
        self,
        app: QApplication,
        family: str | None,
        point_size: int = DEFAULT_FONT_POINT_SIZE,
    ) -> str:
        selected_family = self.resolve_family(family)
        app.setFont(QFont(selected_family, point_size))
        return selected_family

    @staticmethod
    def _sort_families(families: set[str]) -> list[str]:
        preferred = [DEFAULT_FONT_FAMILY, FALLBACK_FONT_FAMILY]
        ordered = [family for family in preferred if family in families]
        ordered.extend(
            family
            for family in sorted(families, key=str.casefold)
            if family not in ordered
        )
        return ordered
