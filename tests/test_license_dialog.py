import sys

from PySide6.QtWidgets import QApplication

from logixcraft.ui.license_dialog import LicenseDialog


def test_license_dialog_reads_license_file(tmp_path) -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    license_file = tmp_path / "LICENSE"
    license_file.write_text("Example license text", encoding="utf-8")

    dialog = LicenseDialog(license_file=license_file)

    assert "Example license text" in dialog.content.toPlainText()
    assert app is not None
