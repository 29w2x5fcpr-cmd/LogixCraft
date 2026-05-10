import logging
from functools import partial

from PySide6.QtWidgets import QFrame, QPushButton, QStackedWidget, QStatusBar, QWidget

logger = logging.getLogger(__name__)


class NavigationController:
    def __init__(self, window, status_bar: QStatusBar | None = None) -> None:
        self.window = window
        self.status_bar = status_bar

        self.btn_home = self._require_child(QPushButton, "btnHome")
        self.btn_plc = self._require_child(QPushButton, "btnPLC")

        self.sidebar_stack = self._require_child(QStackedWidget, "sidebarStack")
        self.sidebar_container = self._require_child(QFrame, "sidebarContainer")
        self.main_stack = self._require_child(QStackedWidget, "mainStack")

        self.nav_config = {
            "home": {
                "button": self.btn_home,
                "sidebar_page": self._require_child(QWidget, "page_sidebar_home"),
                "main_page": self._require_child(QWidget, "page_main_home"),
                "active": True,
            },
            "plc": {
                "button": self.btn_plc,
                "sidebar_page": self._require_child(QWidget, "page_sidebar_plc"),
                "main_page": self._require_child(QWidget, "page_main_plc"),
                "active": True,
            },
        }

        self.connect_navigation()
        self.main_stack.currentChanged.connect(self.update_sidebar_visibility)
        self.update_sidebar_visibility()

    def _require_child(self, widget_type, object_name: str):
        child = self.window.findChild(widget_type, object_name)
        if child is None:
            raise RuntimeError(f"Missing navigation UI widget: {object_name}")
        return child

    def connect_navigation(self) -> None:
        for key, item in self.nav_config.items():
            button = item["button"]
            button.clicked.connect(partial(self.navigate, key))

    def reset_active_buttons(self) -> None:
        for item in self.nav_config.values():
            button = item["button"]
            button.setProperty("active", False)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

    def set_active_button(self, button: QPushButton) -> None:
        self.reset_active_buttons()

        button.setProperty("active", True)
        button.style().unpolish(button)
        button.style().polish(button)
        button.update()

    def navigate(self, key: str) -> None:
        item = self.nav_config[key]

        self.sidebar_stack.setCurrentWidget(item["sidebar_page"])
        self.main_stack.setCurrentWidget(item["main_page"])
        self.update_sidebar_visibility()

        if item.get("active", True):
            self.set_active_button(item["button"])
        else:
            self.reset_active_buttons()

        if self.status_bar is not None:
            self.status_bar.showMessage(f"Opened {key}", 3000)

        logger.info("Opened %s page", key)

    def update_sidebar_visibility(self, _index: int | None = None) -> None:
        home_page = self.nav_config["home"]["main_page"]
        self.sidebar_container.setVisible(self.main_stack.currentWidget() is not home_page)
