from pathlib import Path

from platformdirs import user_config_dir

APP_NAME = "LogixCraft"
APP_VERSION = "0.1.0"

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_ROOT = PROJECT_ROOT / "src"
UI_ROOT = PROJECT_ROOT / "ui"
ASSETS_ROOT = PROJECT_ROOT / "assets"
DOCS_ROOT = PROJECT_ROOT / "docs"
TESTS_ROOT = PROJECT_ROOT / "tests"
TOOLS_ROOT = PROJECT_ROOT / "tools"
BUILDS_ROOT = PROJECT_ROOT / "builds"
LOGS_ROOT = PROJECT_ROOT / "logs"

CONFIG_ROOT = PROJECT_ROOT / "config"
DEFAULT_SETTINGS_FILE = CONFIG_ROOT / "settings.json"
USER_CONFIG_ROOT = Path(user_config_dir(APP_NAME, appauthor=False))
SETTINGS_FILE = USER_CONFIG_ROOT / "settings.json"

MAIN_WINDOW_UI = UI_ROOT / "main_window.ui"

ICONS_ROOT = ASSETS_ROOT / "icons"
FONTS_ROOT = ASSETS_ROOT / "fonts"
NAV_BUTTONS = ICONS_ROOT / "nav_buttons"
