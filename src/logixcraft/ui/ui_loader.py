from pathlib import Path

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader

from logixcraft.core.resources import require_file


def load_ui_file(path: Path):
    require_file(path, "Qt UI file")

    loader = QUiLoader()
    ui_file = QFile(str(path))

    if not ui_file.open(QIODevice.ReadOnly):
        raise RuntimeError(f"Could not open UI file: {path}")

    try:
        widget = loader.load(ui_file)
    finally:
        ui_file.close()

    if widget is None:
        raise RuntimeError(f"Could not load UI file: {path}")

    return widget
