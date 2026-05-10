from pathlib import Path

import pytest

from logixcraft.core.resources import ResourceError, require_file
from logixcraft.core.safe_call import run_safely
from logixcraft.core.startup_checks import run_startup_checks
from logixcraft.core.startup_validation import StartupValidationReport, validate_startup
from logixcraft.ui.ui_loader import load_ui_file


def test_require_file_returns_existing_file(tmp_path) -> None:
    file_path = tmp_path / "example.txt"
    file_path.write_text("ok", encoding="utf-8")

    assert require_file(file_path, "example") == file_path


def test_require_file_raises_for_missing_file(tmp_path) -> None:
    with pytest.raises(ResourceError):
        require_file(tmp_path / "missing.txt", "missing file")


def test_safe_call_returns_none_on_failure() -> None:
    def fail() -> None:
        raise RuntimeError("expected failure")

    assert run_safely("Failing action", fail) is None


def test_startup_checks_pass_for_current_project() -> None:
    run_startup_checks()


def test_startup_validation_report_passes_for_current_project() -> None:
    report = validate_startup()

    assert report.passed
    assert not report.errors


def test_startup_validation_report_formats_errors_and_warnings() -> None:
    report = StartupValidationReport(errors=["fatal"], warnings=["degraded"])

    formatted = report.format()

    assert "Errors:" in formatted
    assert "fatal" in formatted
    assert "Warnings:" in formatted
    assert "degraded" in formatted


def test_load_ui_file_rejects_missing_file(tmp_path) -> None:
    with pytest.raises(ResourceError):
        load_ui_file(Path(tmp_path / "missing.ui"))
