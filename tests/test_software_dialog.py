import sys

from PySide6.QtWidgets import QApplication

from logixcraft.core.config import APP_VERSION
from logixcraft.ui.software_dialog import SoftwareDialog


def test_software_dialog_displays_core_information() -> None:
    app = QApplication.instance() or QApplication(sys.argv)

    dialog = SoftwareDialog()
    info_values = [label.text() for label in dialog.findChildren(type(dialog.subtitle_label))]

    assert "industrial networks" in dialog.subtitle_label.text()
    assert "HMI/SCADA" in dialog.subtitle_label.text()
    assert APP_VERSION in info_values
    assert app is not None
