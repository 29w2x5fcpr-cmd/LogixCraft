import sys
from pathlib import Path

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton


class MainWindow:
    def __init__(self) -> None:
        ui_path = Path(__file__).resolve().parents[2] / "ui" / "main_window.ui"

        loader = QUiLoader()
        ui_file = QFile(str(ui_path))

        if not ui_file.open(QIODevice.ReadOnly):
            raise RuntimeError(f"Could not open UI file: {ui_path}")

        self.window = loader.load(ui_file)
        ui_file.close()

        if self.window is None:
            raise RuntimeError(f"Could not load UI file: {ui_path}")

        self.label_status = self.window.findChild(QLabel, "label_status")
        self.button_test = self.window.findChild(QPushButton, "button_test")

        if self.label_status is None:
            raise RuntimeError("Could not find QLabel with objectName 'label_status'")

        if self.button_test is None:
            raise RuntimeError("Could not find QPushButton with objectName 'button_test'")

        self.button_test.clicked.connect(self.on_test_clicked)

    def on_test_clicked(self) -> None:
        self.label_status.setText("Button clicked")

    def show(self) -> None:
        self.window.show()


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()