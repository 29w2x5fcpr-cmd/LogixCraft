from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class ErrorDialog(QDialog):
    def __init__(self, title: str, message: str, details: str = "", parent=None) -> None:
        super().__init__(parent)
        self.details_text = details

        self.setObjectName("errorDialog")
        self.setWindowTitle(title)
        self.resize(680, 420)
        self.setMinimumSize(520, 280)

        self._build_ui(title, message)

    def _build_ui(self, title: str, message: str) -> None:
        self.title_label = QLabel(title)
        self.title_label.setObjectName("errorTitle")
        self.title_label.setWordWrap(True)

        self.message_label = QLabel(message)
        self.message_label.setObjectName("errorMessage")
        self.message_label.setWordWrap(True)

        self.details_box = QTextEdit()
        self.details_box.setObjectName("errorDetails")
        self.details_box.setReadOnly(True)
        self.details_box.setPlainText(self.details_text)
        self.details_box.setVisible(False)

        self.button_toggle_details = QPushButton("Show Details")
        self.button_toggle_details.setObjectName("errorDetailsButton")

        self.button_box = QDialogButtonBox()
        self.button_close = self.button_box.addButton(QDialogButtonBox.Close)
        self.button_box.addButton(self.button_toggle_details, QDialogButtonBox.ActionRole)

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)
        layout.addWidget(self.details_box, 1)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

        self.button_close.clicked.connect(self.accept)
        self.button_toggle_details.clicked.connect(self.toggle_details)

    def toggle_details(self) -> None:
        should_show = not self.details_box.isVisible()
        self.details_box.setVisible(should_show)
        self.button_toggle_details.setText("Hide Details" if should_show else "Show Details")
