import sys

from PySide6.QtWidgets import QApplication, QDialog, QWidget

from logixcraft.ui.dialog_manager import DialogManager


def test_dialog_manager_reuses_open_dialog() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    parent = QWidget()
    manager = DialogManager(parent=parent)

    manager.show_single("test", QDialog)
    first_dialog = manager._dialogs["test"]

    manager.show_single("test", QDialog)

    assert manager._dialogs["test"] is first_dialog
    assert app is not None
