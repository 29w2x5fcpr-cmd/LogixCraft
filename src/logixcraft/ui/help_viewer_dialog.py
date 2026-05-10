from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QTextEdit,
    QVBoxLayout,
)


class HelpViewerDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("helpViewerDialog")
        self.setWindowTitle("Help Viewer")
        self.resize(760, 500)
        self.setMinimumSize(640, 420)

        self._build_ui()

    def _build_ui(self) -> None:
        self.title_label = QLabel("Help Viewer")
        self.title_label.setObjectName("helpTitle")

        self.subtitle_label = QLabel(
            "Documentation, workflows, and troubleshooting guidance will be available here."
        )
        self.subtitle_label.setObjectName("helpSubtitle")
        self.subtitle_label.setWordWrap(True)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("helpSearch")
        self.search_input.setPlaceholderText("Search help topics")
        self.search_input.setEnabled(False)

        self.topic_list = QListWidget()
        self.topic_list.setObjectName("helpTopicList")
        self.topic_list.addItems(
            [
                "Getting Started",
                "PLC Tools",
                "HMI and SCADA",
                "Industrial Networks",
                "Commissioning",
                "Diagnostics",
                "Reports and Documentation",
                "Troubleshooting",
            ]
        )
        self.topic_list.setCurrentRow(0)

        self.placeholder_text = QTextEdit()
        self.placeholder_text.setObjectName("helpContent")
        self.placeholder_text.setReadOnly(True)
        self.placeholder_text.setText(
            "Help content placeholder\n\n"
            "This viewer is ready for the LogixCraft documentation system. Planned content "
            "can include step-by-step workflows, tool references, troubleshooting notes, "
            "release notes, keyboard shortcuts, and project-specific guidance.\n\n"
            "The current build only provides the shell so the menu flow and window behavior "
            "can be reviewed before the documentation pages are added."
        )

        content_frame = QFrame()
        content_frame.setObjectName("helpContentFrame")

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(12)
        content_layout.addWidget(self.topic_list, 1)
        content_layout.addWidget(self.placeholder_text, 3)
        content_frame.setLayout(content_layout)

        self.button_box = QDialogButtonBox()
        self.close_button = self.button_box.addButton(QDialogButtonBox.Close)
        self.close_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 16, 18, 14)
        layout.setSpacing(9)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.search_input)
        layout.addWidget(content_frame, 1)
        layout.addWidget(self.button_box, alignment=Qt.AlignRight)
        self.setLayout(layout)
