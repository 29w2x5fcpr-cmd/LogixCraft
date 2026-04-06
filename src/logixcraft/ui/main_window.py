import logging

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QLabel, QPushButton

from logixcraft.core.config import APP_NAME, APP_VERSION, MAIN_WINDOW_UI

from logixcraft.core.controller import AppController

logger = logging.getLogger(__name__)


class MainWindow:
    def __init__(self) -> None:
        loader = QUiLoader()
        ui_file = QFile(str(MAIN_WINDOW_UI))
        self.controller = AppController()
        if not ui_file.open(QIODevice.ReadOnly):
            raise RuntimeError(f"Could not open UI file: {MAIN_WINDOW_UI}")

        self.window = loader.load(ui_file)
        ui_file.close()

        if self.window is None:
            raise RuntimeError(f"Could not load UI file: {MAIN_WINDOW_UI}")

        self.window.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")

        self.label_status = self.window.findChild(QLabel, "label_status")
        self.button_test = self.window.findChild(QPushButton, "button_test")

        if self.label_status is None:
            raise RuntimeError("Could not find QLabel with objectName 'label_status'")

        if self.button_test is None:
            raise RuntimeError("Could not find QPushButton with objectName 'button_test'")

        self.button_test.clicked.connect(self.on_test_clicked)

        logger.info("Main window initialized")

    def on_test_clicked(self) -> None:
        result = self.controller.handle_test_button()
        self.label_status.setText(result)

    def show(self) -> None:
        logger.info("Showing main window")
        self.window.show()
