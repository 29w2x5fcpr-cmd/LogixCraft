import platform
import sys

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

from logixcraft.core.config import APP_VERSION, ASSETS_ROOT


class SoftwareDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("softwareDialog")
        self.setWindowTitle("Software")
        self.resize(640, 560)
        self.setMinimumSize(580, 500)

        self._build_ui()

    def _build_ui(self) -> None:
        self.logo_label = QLabel()
        self.logo_label.setObjectName("softwareLogo")
        self.logo_label.setAlignment(Qt.AlignCenter)

        logo_path = ASSETS_ROOT / "icons" / "app" / "logo.png"
        pixmap = QPixmap(str(logo_path))
        if not pixmap.isNull():
            self.logo_label.setPixmap(
                pixmap.scaled(260, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

        self.subtitle_label = QLabel(
            "Professional desktop engineering toolkit for PLC systems, HMI/SCADA "
            "platforms, industrial networks, commissioning, diagnostics, documentation, "
            "and daily automation engineering workflows."
        )
        self.subtitle_label.setObjectName("softwareSubtitle")
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setAlignment(Qt.AlignCenter)

        self.info_frame = QFrame()
        self.info_frame.setObjectName("softwareInfoFrame")

        info_layout = QGridLayout()
        info_layout.setContentsMargins(14, 14, 14, 14)
        info_layout.setHorizontalSpacing(18)
        info_layout.setVerticalSpacing(7)

        info_items = [
            ("Version", APP_VERSION),
            ("Author", "Jakub H. Rembisz"),
            ("License", "Proprietary"),
            ("Framework", "Python / PySide6"),
            ("Platform", "Windows-focused, offline-first desktop application"),
            ("Scope", "PLC, SCADA, networking, engineering maths, documentation, and reporting"),
            ("Python", sys.version.split()[0]),
            ("Operating System", f"{platform.system()} {platform.release()}"),
        ]

        for row, (label, value) in enumerate(info_items):
            key_label = QLabel(label)
            key_label.setObjectName("softwareInfoKey")
            value_label = QLabel(value)
            value_label.setObjectName("softwareInfoValue")
            value_label.setWordWrap(True)
            value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            info_layout.addWidget(key_label, row, 0)
            info_layout.addWidget(value_label, row, 1)

        self.info_frame.setLayout(info_layout)

        self.button_box = QDialogButtonBox()
        self.button_close = self.button_box.addButton(QDialogButtonBox.Close)

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 16, 18, 14)
        layout.setSpacing(9)
        layout.addWidget(self.logo_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.info_frame)
        layout.addStretch()
        layout.addWidget(self.button_box)
        self.setLayout(layout)

        self.button_close.clicked.connect(self.accept)
