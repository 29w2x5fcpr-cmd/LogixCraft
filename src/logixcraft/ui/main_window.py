import logging

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QStatusBar,
)

from logixcraft.core.config import (
    APP_NAME,
    APP_VERSION,
    ASSETS_ROOT,
    MAIN_WINDOW_UI,
)
from logixcraft.core.controller import AppController
from logixcraft.core.resources import require_file
from logixcraft.ui.dialog_manager import DialogManager
from logixcraft.ui.menu_actions import MenuActionController
from logixcraft.ui.navigation import NavigationController
from logixcraft.ui.ui_loader import load_ui_file
from logixcraft.ui.window_state import WindowState

logger = logging.getLogger(__name__)


class MainWindow(QObject):
    def __init__(self, settings, font_manager) -> None:
        super().__init__()
        self.settings = settings
        self.font_manager = font_manager

        self.controller = AppController()
        self.window = load_ui_file(MAIN_WINDOW_UI)

        self.dialog_manager = DialogManager(parent=self.window)
        self.window_state = WindowState(window=self.window, settings=self.settings)
        self.window.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.window_state.restore_size()

        self.status_bar = self.window.findChild(QStatusBar, "statusbar")

        if self.status_bar is not None:
            self.status_bar.showMessage("Ready")

        self.homeImage = self.window.findChild(QLabel, "homeImage")
        self.homeTitle = self.window.findChild(QLabel, "homeTitle")

        self.btnHome = self.window.findChild(QPushButton, "btnHome")
        self.btnPLC = self.window.findChild(QPushButton, "btnPLC")
        self.navBarFrame = self.window.findChild(QFrame, "navBarFrame")

        if self.navBarFrame is not None:
            self.navBarFrame.setFrameShape(QFrame.NoFrame)
            self.navBarFrame.setFixedHeight(42)

        self.navigation = NavigationController(window=self.window, status_bar=self.status_bar)
        self.menu_actions = MenuActionController(
            window=self.window,
            settings=self.settings,
            font_manager=self.font_manager,
            dialog_manager=self.dialog_manager,
        )
        image_path = require_file(ASSETS_ROOT / "icons" / "app" / "logo.png", "home logo")

        pixmap = QPixmap(str(image_path))
        self.homeImage.setPixmap(
            pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.window.installEventFilter(self)
        self.navigation.navigate("home")
        logger.info("Main window initialized")

    def eventFilter(self, obj, event):
        if obj == self.window and event.type() == QEvent.Close:
            self.window_state.save_size()

        return super().eventFilter(obj, event)

    def show(self) -> None:
        self.window.show()
