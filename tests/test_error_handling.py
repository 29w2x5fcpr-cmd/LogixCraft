import sys

from PySide6.QtWidgets import QApplication

from logixcraft.core.error_handling import format_exception
from logixcraft.ui.error_dialog import ErrorDialog


def test_format_exception_includes_exception_message() -> None:
    try:
        raise RuntimeError("example failure")
    except RuntimeError:
        exc_type, exc_value, exc_traceback = sys.exc_info()

    details = format_exception(exc_type, exc_value, exc_traceback)

    assert "RuntimeError" in details
    assert "example failure" in details


def test_error_dialog_toggles_details() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    dialog = ErrorDialog("Unexpected Error", "Something failed.", "Traceback details")

    assert dialog.details_box.isHidden()
    dialog.toggle_details()
    assert not dialog.details_box.isHidden()
    assert dialog.button_toggle_details.text() == "Hide technical details"
    assert dialog.width() >= dialog.expanded_size[0]
    assert dialog.height() >= dialog.expanded_size[1]
    assert dialog.button_close.isDefault()
    assert app is not None


def test_error_dialog_summarizes_traceback_details() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    details = 'Traceback\n  File "example.py", line 10, in run\nValueError: bad value'

    dialog = ErrorDialog("Unexpected Error", "Something failed.", details)
    summary, error_type, location = dialog._summarize_details()

    assert summary == "ValueError occurred: bad value"
    assert error_type == "ValueError: bad value"
    assert location == 'File "example.py", line 10, in run'
    assert app is not None


def test_error_dialog_summarizes_common_file_error() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    details = "Traceback\nFileNotFoundError: missing asset"

    dialog = ErrorDialog("Unexpected Error", "Something failed.", details)
    summary, _error_type, _location = dialog._summarize_details()

    assert summary == "LogixCraft could not find a file it needs."
    assert app is not None
