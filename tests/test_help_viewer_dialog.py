import sys

from PySide6.QtWidgets import QApplication

from logixcraft.ui.help_viewer_dialog import HelpViewerDialog


def test_help_viewer_dialog_is_placeholder_shell() -> None:
    app = QApplication.instance() or QApplication(sys.argv)

    dialog = HelpViewerDialog()

    assert dialog.windowTitle() == "Help Viewer"
    assert dialog.search_input.isEnabled() is False
    assert dialog.topic_list.count() >= 6
    assert "Help content placeholder" in dialog.placeholder_text.toPlainText()
    assert app is not None
