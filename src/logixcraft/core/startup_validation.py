import importlib.util
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree

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
from logixcraft.core.logging_config import BACKUP_LOG_COUNT, MAX_LOG_BYTES
from logixcraft.core.resources import ResourceError, require_directory, require_file

logger = logging.getLogger(__name__)


class StartupValidationError(RuntimeError):
    pass


@dataclass
class StartupValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)

    @property
    def passed(self) -> bool:
        return not self.has_errors

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def format(self) -> str:
        sections = []
        if self.errors:
            sections.append("Errors:\n" + "\n".join(f"- {error}" for error in self.errors))
        if self.warnings:
            sections.append("Warnings:\n" + "\n".join(f"- {warning}" for warning in self.warnings))
        return "\n\n".join(sections) if sections else "Startup validation passed."

    def log(self) -> None:
        if self.errors:
            logger.error("Startup validation errors:\n%s", "\n".join(self.errors))
        if self.warnings:
            logger.warning("Startup validation warnings:\n%s", "\n".join(self.warnings))
        if not self.errors and not self.warnings:
            logger.info("Startup validation passed")

    def raise_for_errors(self) -> None:
        if self.errors:
            raise StartupValidationError(self.format())


def validate_startup() -> StartupValidationReport:
    report = StartupValidationReport()

    _validate_runtime(report)
    _validate_settings(report)
    _validate_assets(report)
    _validate_ui(report)
    _validate_logging(report)

    return report


def run_startup_validation() -> StartupValidationReport:
    report = validate_startup()
    report.log()
    report.raise_for_errors()
    return report


def _validate_runtime(report: StartupValidationReport) -> None:
    for module_name in ("PySide6", "platformdirs"):
        if importlib.util.find_spec(module_name) is None:
            report.add_error(f"Required Python package is not available: {module_name}")

    _check_required_directory(report, PROJECT_ROOT, "project root")


def _validate_settings(report: StartupValidationReport) -> None:
    _check_required_file(report, DEFAULT_SETTINGS_FILE, "default settings file")

    default_settings = _read_json_file(report, DEFAULT_SETTINGS_FILE, "default settings")
    if isinstance(default_settings, dict):
        required_paths = [
            ("appearance", "theme"),
            ("appearance", "font_family"),
            ("appearance", "ui_scale"),
            ("window", "width"),
            ("window", "height"),
            ("general", "restore_last_window_size"),
        ]
        for path in required_paths:
            if _nested_get(default_settings, path) is None:
                report.add_error(f"Default settings missing key: {'.'.join(path)}")

    try:
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        probe_file = SETTINGS_FILE.parent / ".write_test"
        probe_file.write_text("ok", encoding="utf-8")
        probe_file.unlink(missing_ok=True)
    except OSError as exc:
        report.add_error(f"User settings directory is not writable: {exc}")


def _validate_assets(report: StartupValidationReport) -> None:
    _check_required_directory(report, ASSETS_ROOT, "assets directory")
    _check_required_directory(report, ICONS_ROOT, "icons directory")
    _check_required_directory(report, FONTS_ROOT, "fonts directory")

    _check_required_file(report, ICONS_ROOT / "app" / "logo.png", "application logo")
    _check_required_file(report, ICONS_ROOT / "app" / "logo_symbol.png", "application icon")

    if FONTS_ROOT.is_dir() and not any(FONTS_ROOT.rglob("*.ttf")):
        report.add_warning("No bundled TrueType fonts were found.")


def _validate_ui(report: StartupValidationReport) -> None:
    _check_required_file(report, MAIN_WINDOW_UI, "main window UI file")
    if not MAIN_WINDOW_UI.is_file():
        return

    required_names = {
        "btnHome",
        "btnPLC",
        "mainStack",
        "sidebarStack",
        "actionTerminal",
        "actionLicense",
        "actionSoftware",
        "actionPreferences",
    }

    try:
        root = ElementTree.parse(MAIN_WINDOW_UI).getroot()
    except ElementTree.ParseError as exc:
        report.add_error(f"Main window UI file is not valid XML: {exc}")
        return

    object_names = {
        element.attrib["name"]
        for element in root.iter()
        if "name" in element.attrib
    }
    missing = sorted(required_names - object_names)
    for object_name in missing:
        report.add_error(f"Main window UI missing required object: {object_name}")


def _validate_logging(report: StartupValidationReport) -> None:
    if MAX_LOG_BYTES <= 0:
        report.add_error("Log rotation max size must be greater than zero.")
    if BACKUP_LOG_COUNT < 1:
        report.add_error("Log rotation backup count must be at least one.")

    try:
        LOGS_ROOT.mkdir(parents=True, exist_ok=True)
        probe_file = LOGS_ROOT / ".write_test"
        probe_file.write_text("ok", encoding="utf-8")
        probe_file.unlink(missing_ok=True)
    except OSError as exc:
        report.add_error(f"Logs directory is not writable: {exc}")


def _check_required_file(report: StartupValidationReport, path: Path, description: str) -> None:
    try:
        require_file(path, description)
    except ResourceError as exc:
        report.add_error(str(exc))


def _check_required_directory(
    report: StartupValidationReport,
    path: Path,
    description: str,
) -> None:
    try:
        require_directory(path, description)
    except ResourceError as exc:
        report.add_error(str(exc))


def _read_json_file(report: StartupValidationReport, path: Path, description: str) -> dict | None:
    if not path.is_file():
        return None

    try:
        with path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
    except json.JSONDecodeError as exc:
        report.add_error(f"{description.capitalize()} is not valid JSON: {exc}")
        return None

    if not isinstance(loaded, dict):
        report.add_error(f"{description.capitalize()} root must be a JSON object.")
        return None

    return loaded


def _nested_get(data: dict, path: tuple[str, ...]):
    value = data
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value
