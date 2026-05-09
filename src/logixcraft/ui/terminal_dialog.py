import logging
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QTextEdit, QVBoxLayout

from logixcraft.core.config import LOGS_ROOT

logger = logging.getLogger(__name__)


class TerminalDialog(QDialog):
    def __init__(self, log_file: Path | None = None, parent=None) -> None:
        super().__init__(parent)
        self.log_file = log_file or LOGS_ROOT / "logixcraft.log"
        self._last_content = ""

        self.setObjectName("terminalDialog")
        self.setWindowTitle("Terminal")
        self.resize(920, 560)
        self.setMinimumSize(720, 420)

        self._build_ui()

        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(750)
        self.refresh_timer.timeout.connect(self.refresh_log)
        self.refresh_timer.start()

        self.refresh_log()
        logger.info("Terminal dialog opened")

    def _build_ui(self) -> None:
        self.title_label = QLabel("Terminal")
        self.title_label.setObjectName("terminalTitle")

        self.subtitle_label = QLabel(str(self.log_file))
        self.subtitle_label.setObjectName("terminalSubtitle")
        self.subtitle_label.setWordWrap(True)

        self.output = QTextEdit()
        self.output.setObjectName("terminalOutput")
        self.output.setReadOnly(True)
        self.output.setLineWrapMode(QTextEdit.NoWrap)
        self.output.setFont(QFont("Consolas", 10))

        self.button_box = QDialogButtonBox()
        self.button_refresh = self.button_box.addButton("Refresh", QDialogButtonBox.ActionRole)
        self.button_close = self.button_box.addButton(QDialogButtonBox.Close)

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.output, 1)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

        self.button_refresh.clicked.connect(self.refresh_log)
        self.button_close.clicked.connect(self.accept)

    def refresh_log(self) -> None:
        if not self.log_file.exists():
            content = f"Waiting for log file: {self.log_file}"
        else:
            content = self.log_file.read_text(encoding="utf-8", errors="replace")

        if content == self._last_content:
            return

        self._last_content = content
        self.output.setPlainText(content)
        self.output.moveCursor(QTextCursor.End)

    def showEvent(self, event) -> None:
        self.refresh_log()
        super().showEvent(event)
