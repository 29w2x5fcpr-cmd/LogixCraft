from pathlib import Path

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QTextEdit, QVBoxLayout

from logixcraft.core.config import PROJECT_ROOT


class LicenseDialog(QDialog):
    def __init__(self, license_file: Path | None = None, parent=None) -> None:
        super().__init__(parent)
        self.license_file = license_file or PROJECT_ROOT / "LICENSE"

        self.setObjectName("licenseDialog")
        self.setWindowTitle("License")
        self.resize(700, 540)
        self.setMinimumSize(600, 420)

        self._build_ui()
        self._load_license()

    def _build_ui(self) -> None:
        self.title_label = QLabel("License")
        self.title_label.setObjectName("licenseTitle")

        self.subtitle_label = QLabel("LogixCraft Proprietary License")
        self.subtitle_label.setObjectName("licenseSubtitle")
        self.subtitle_label.setWordWrap(True)

        self.content = QTextEdit()
        self.content.setObjectName("licenseContent")
        self.content.setReadOnly(True)

        self.button_box = QDialogButtonBox()
        self.button_close = self.button_box.addButton(QDialogButtonBox.Close)

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.content, 1)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

        self.button_close.clicked.connect(self.accept)

    def _load_license(self) -> None:
        if not self.license_file.exists():
            self.content.setPlainText(f"License file not found: {self.license_file}")
            return

        self.content.setPlainText(self.license_file.read_text(encoding="utf-8"))
