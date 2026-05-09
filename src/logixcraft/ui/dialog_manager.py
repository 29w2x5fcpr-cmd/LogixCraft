from collections.abc import Callable

from PySide6.QtWidgets import QDialog, QWidget


class DialogManager:
    def __init__(self, parent: QWidget) -> None:
        self.parent = parent
        self._dialogs: dict[str, QDialog] = {}

    def show_single(self, key: str, factory: Callable[..., QDialog]) -> None:
        dialog = self._dialogs.get(key)

        if dialog is None:
            dialog = factory(parent=self.parent)
            self._dialogs[key] = dialog
            dialog.finished.connect(
                lambda _result, dialog_key=key: self._dialogs.pop(dialog_key, None)
            )

        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
