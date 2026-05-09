import logging

from logixcraft.core.config import (
    ASSETS_ROOT,
    DEFAULT_SETTINGS_FILE,
    FONTS_ROOT,
    ICONS_ROOT,
    LOGS_ROOT,
    MAIN_WINDOW_UI,
    PROJECT_ROOT,
    SETTINGS_FILE,
)
from logixcraft.core.resources import require_directory, require_file

logger = logging.getLogger(__name__)


class StartupCheckError(RuntimeError):
    pass


def run_startup_checks() -> None:
    checks = [
        lambda: require_directory(PROJECT_ROOT, "project root"),
        lambda: require_directory(ASSETS_ROOT, "assets directory"),
        lambda: require_directory(ICONS_ROOT, "icons directory"),
        lambda: require_directory(FONTS_ROOT, "fonts directory"),
        lambda: require_file(MAIN_WINDOW_UI, "main window UI file"),
        lambda: require_file(DEFAULT_SETTINGS_FILE, "default settings file"),
        lambda: require_file(ICONS_ROOT / "app" / "logo.png", "application logo"),
        lambda: require_file(ICONS_ROOT / "app" / "logo_symbol.png", "application icon"),
    ]

    failures = []
    for check in checks:
        try:
            check()
        except Exception as exc:
            failures.append(str(exc))

    try:
        LOGS_ROOT.mkdir(parents=True, exist_ok=True)
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        failures.append(f"Could not create runtime directory: {exc}")

    if failures:
        details = "\n".join(f"- {failure}" for failure in failures)
        raise StartupCheckError(f"Startup checks failed:\n{details}")

    logger.info("Startup checks passed")
