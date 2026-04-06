import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LogixCraft")

        label = QLabel("LogixCraft is running 🚀")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(800, 500)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()