from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStyle,
    QTextEdit,
    QVBoxLayout,
)


class ErrorDialog(QDialog):
    def __init__(self, title: str, message: str, details: str = "", parent=None) -> None:
        super().__init__(parent)
        self.details_text = details
        self.collapsed_size = (560, 260)
        self.expanded_size = (760, 520)

        self.setObjectName("errorDialog")
        self.setWindowTitle(title)
        self.resize(*self.collapsed_size)
        self.setMinimumSize(480, 220)

        self._build_ui(title, message)

    def _build_ui(self, title: str, message: str) -> None:
        self.header_frame = QFrame()
        self.header_frame.setObjectName("errorHeader")

        self.icon_label = QLabel()
        self.icon_label.setObjectName("errorIcon")
        self.icon_label.setFixedSize(36, 36)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self._set_error_icon()

        self.title_label = QLabel(title)
        self.title_label.setObjectName("errorTitle")
        self.title_label.setWordWrap(True)

        self.message_label = QLabel(message)
        self.message_label.setObjectName("errorMessage")
        self.message_label.setWordWrap(True)

        self.summary_frame = QFrame()
        self.summary_frame.setObjectName("errorSummary")
        summary_layout = QGridLayout()
        summary_layout.setContentsMargins(10, 8, 10, 8)
        summary_layout.setHorizontalSpacing(12)
        summary_layout.setVerticalSpacing(3)
        self.summary_frame.setLayout(summary_layout)

        error_summary, error_type, error_location = self._summarize_details()
        summary_items = [
            ("Summary", error_summary),
            ("Type", error_type),
            ("Location", error_location),
            ("Logged", "Yes"),
        ]

        for row, (label, value) in enumerate(summary_items):
            key_label = QLabel(label)
            key_label.setObjectName("errorSummaryKey")
            value_label = QLabel(value)
            value_label.setObjectName("errorSummaryValue")
            value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            summary_layout.addWidget(key_label, row, 0)
            summary_layout.addWidget(value_label, row, 1)

        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(2)
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.message_label)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setSpacing(10)
        header_layout.addWidget(self.icon_label, 0, Qt.AlignTop)
        header_layout.addLayout(title_layout, 1)
        self.header_frame.setLayout(header_layout)

        self.details_box = QTextEdit()
        self.details_box.setObjectName("errorDetails")
        self.details_box.setReadOnly(True)
        self.details_box.setPlainText(self.details_text)
        self.details_box.setVisible(False)

        self.button_toggle_details = QPushButton("Show technical details")
        self.button_toggle_details.setObjectName("errorDetailsButton")

        self.button_box = QDialogButtonBox()
        self.button_close = self.button_box.addButton("Close", QDialogButtonBox.AcceptRole)
        self.button_close.setDefault(True)
        self.button_box.addButton(self.button_toggle_details, QDialogButtonBox.ActionRole)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(self.header_frame)
        layout.addWidget(self.summary_frame)
        layout.addWidget(self.details_box, 1)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

        self.button_close.clicked.connect(self.accept)
        self.button_toggle_details.clicked.connect(self.toggle_details)

    def toggle_details(self) -> None:
        should_show = not self.details_box.isVisible()
        self.details_box.setVisible(should_show)
        self.button_toggle_details.setText(
            "Hide technical details" if should_show else "Show technical details"
        )

        if should_show:
            self.setMinimumSize(620, 420)
            self.resize(*self.expanded_size)
        else:
            self.setMinimumSize(480, 220)
            self.resize(*self.collapsed_size)

    def _set_error_icon(self) -> None:
        app = QApplication.instance()
        if app is None:
            return

        icon = app.style().standardIcon(QStyle.SP_MessageBoxWarning)
        self.icon_label.setPixmap(icon.pixmap(28, 28))

    def _summarize_details(self) -> tuple[str, str, str]:
        if not self.details_text:
            return (
                "The action failed, but no technical details were available.",
                "Application error",
                "Not available",
            )

        lines = [line.strip() for line in self.details_text.splitlines() if line.strip()]
        error_type = lines[-1] if lines else "Application error"
        file_lines = [line for line in lines if line.startswith('File "')]
        location = file_lines[-1] if file_lines else "See technical details"

        return self._build_error_summary(error_type, location), error_type, location

    def _build_error_summary(self, error_type: str, location: str) -> str:
        exception_name, _, exception_message = error_type.partition(":")
        exception_message = exception_message.strip()

        if exception_name == "FileNotFoundError":
            return "LogixCraft could not find a file it needs."
        if exception_name == "PermissionError":
            return "LogixCraft does not have permission to access a required file or folder."
        if exception_name == "JSONDecodeError":
            return "LogixCraft could not read a settings or data file because it is not valid JSON."
        if exception_name == "KeyError":
            return "LogixCraft expected a setting or data field that was missing."
        if exception_name == "ImportError" or exception_name == "ModuleNotFoundError":
            return "LogixCraft could not load a required Python module."
        if exception_name == "ResourceError":
            return "LogixCraft could not find or load a required application resource."

        if exception_message:
            return f"{exception_name} occurred: {exception_message}"

        if location != "See technical details":
            return f"{exception_name} occurred while running this part of the application."

        return "LogixCraft hit an unexpected application error."
