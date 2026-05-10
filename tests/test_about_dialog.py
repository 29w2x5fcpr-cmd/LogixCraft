import sys

from PySide6.QtWidgets import QApplication, QLabel

from logixcraft.core.config import APP_NAME, APP_VERSION
from logixcraft.ui.about_dialog import AboutDialog


def test_about_dialog_shows_application_identity() -> None:
    app = QApplication.instance() or QApplication(sys.argv)

    dialog = AboutDialog()

    assert dialog.windowTitle() == f"About {APP_NAME}"
    assert dialog.title_label.text() == APP_NAME
    values = [label.text() for label in dialog.info_frame.findChildren(QLabel, "aboutInfoValue")]
    assert APP_VERSION in values
    assert app is not None
