from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
)

from logixcraft.core.config import APP_NAME, APP_VERSION, ASSETS_ROOT


class AboutDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("aboutDialog")
        self.setWindowTitle(f"About {APP_NAME}")
        self.resize(460, 430)
        self.setMinimumSize(420, 380)

        self._build_ui()

    def _build_ui(self) -> None:
        self.logo_label = QLabel()
        self.logo_label.setObjectName("aboutLogo")
        self.logo_label.setAlignment(Qt.AlignCenter)

        logo_path = ASSETS_ROOT / "icons" / "app" / "logo_symbol.png"
        pixmap = QPixmap(str(logo_path))
        if not pixmap.isNull():
            self.logo_label.setPixmap(
                pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

        self.title_label = QLabel(APP_NAME)
        self.title_label.setObjectName("aboutTitle")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.subtitle_label = QLabel(
            "Industrial automation engineering workspace for PLC systems, "
            "commissioning, diagnostics, documentation, and daily project work."
        )
        self.subtitle_label.setObjectName("aboutSubtitle")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setWordWrap(True)

        self.info_frame = QFrame()
        self.info_frame.setObjectName("aboutInfoFrame")

        info_layout = QGridLayout()
        info_layout.setContentsMargins(14, 12, 14, 12)
        info_layout.setHorizontalSpacing(16)
        info_layout.setVerticalSpacing(7)

        info_items = [
            ("Version", APP_VERSION),
            ("Author", "Jakub H. Rembisz"),
            ("License", "Proprietary"),
            ("Framework", "Python / PySide6"),
        ]

        for row, (label, value) in enumerate(info_items):
            key_label = QLabel(label)
            key_label.setObjectName("aboutInfoKey")
            value_label = QLabel(value)
            value_label.setObjectName("aboutInfoValue")
            value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            info_layout.addWidget(key_label, row, 0)
            info_layout.addWidget(value_label, row, 1)

        self.info_frame.setLayout(info_layout)

        self.button_box = QDialogButtonBox()
        self.close_button = self.button_box.addButton(QDialogButtonBox.Close)
        self.close_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 18, 20, 14)
        layout.setSpacing(9)
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.info_frame)
        layout.addStretch()
        layout.addWidget(self.button_box)
        self.setLayout(layout)
