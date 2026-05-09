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
    assert dialog.button_toggle_details.text() == "Hide Details"
    assert app is not None
