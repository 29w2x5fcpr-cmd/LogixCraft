import sys

from PySide6.QtWidgets import QApplication

from logixcraft.ui.terminal_dialog import TerminalDialog


def test_terminal_dialog_reads_log_file(tmp_path) -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    log_file = tmp_path / "logixcraft.log"
    log_file.write_text("test log line", encoding="utf-8")

    dialog = TerminalDialog(log_file=log_file)
    dialog.refresh_log()

    assert "test log line" in dialog.output.toPlainText()
    assert app is not None
