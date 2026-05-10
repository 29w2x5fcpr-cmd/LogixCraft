import sys

from PySide6.QtWidgets import QApplication

from logixcraft.ui.splash_screen import SplashScreen


def test_splash_screen_builds_pixmap_and_accepts_status() -> None:
    app = QApplication.instance() or QApplication(sys.argv)

    splash = SplashScreen()
    splash.show_status("Testing startup...")

    assert not splash.pixmap().isNull()
    assert app is not None
