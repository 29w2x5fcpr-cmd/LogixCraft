import logging
from functools import partial

from PySide6.QtCore import QEasingCurve, QParallelAnimationGroup, QPropertyAnimation, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QWidget,
)

from logixcraft.core.config import NAV_BUTTONS
from logixcraft.core.resources import require_file

logger = logging.getLogger(__name__)

NAVBAR_ANIMATION_MS = 360
NAVBAR_TOGGLE_ICON_SIZE = QSize(25, 25)


class NavigationController:
    def __init__(self, window, status_bar: QStatusBar | None = None) -> None:
        self.window = window
        self.status_bar = status_bar

        self.btn_home = self._require_child(QPushButton, "btnHome")
        self.btn_plc = self._require_child(QPushButton, "btnPLC")

        self.sidebar_stack = self._require_child(QStackedWidget, "sidebarStack")
        self.sidebar_container = self._require_child(QFrame, "sidebarContainer")
        self.main_stack = self._require_child(QStackedWidget, "mainStack")
        self.nav_bar_frame = self._require_child(QFrame, "navBarFrame")
        self.nav_buttons: list[QPushButton] = []
        self.navbar_expanded = False
        self._navbar_animation: QParallelAnimationGroup | None = None
        self.icon_expand = QIcon(
            str(require_file(NAV_BUTTONS / "arrow-autofit-right.svg", "navbar expand icon"))
        )
        self.icon_collapse = QIcon(
            str(require_file(NAV_BUTTONS / "arrow-autofit-left.svg", "navbar collapse icon"))
        )

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

        self.configure_navbar_buttons()
        self.connect_navigation()
        self.main_stack.currentChanged.connect(self.update_sidebar_visibility)
        self.set_navbar_expanded(False, animated=False)
        self.update_sidebar_visibility()

    def _require_child(self, widget_type, object_name: str):
        child = self.window.findChild(widget_type, object_name)
        if child is None:
            raise RuntimeError(f"Missing navigation UI widget: {object_name}")
        return child

    def connect_navigation(self) -> None:
        for key, item in self.nav_config.items():
            button = item["button"]
            if button is self.btn_home:
                button.clicked.connect(self.toggle_home_navigation)
                continue

            button.clicked.connect(partial(self.navigate, key))

    def configure_navbar_buttons(self) -> None:
        for button in self.nav_bar_frame.findChildren(QPushButton):
            if button.objectName() == "btnHome":
                continue

            button.setProperty("navButton", True)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()
            button.setMinimumWidth(button.sizeHint().width())
            self._ensure_opacity_effect(button).setOpacity(0.0)
            self.nav_buttons.append(button)

    def toggle_home_navigation(self) -> None:
        self.navigate("home")
        self.set_navbar_expanded(not self.navbar_expanded, animated=True)

    def set_navbar_expanded(self, expanded: bool, animated: bool = True) -> None:
        self.navbar_expanded = expanded
        self.nav_bar_frame.setProperty("expanded", expanded)
        self._update_home_toggle_icon()

        collapsed_width = self._collapsed_navbar_width()
        expanded_width = self._expanded_navbar_width()

        if self._navbar_animation is not None:
            self._navbar_animation.stop()
            self._navbar_animation = None

        if not animated:
            for button in self.nav_buttons:
                button.setVisible(expanded)
                self._ensure_opacity_effect(button).setOpacity(1.0 if expanded else 0.0)

            self.nav_bar_frame.setFixedWidth(expanded_width if expanded else collapsed_width)
            self._refresh_navbar_style()
            return

        for button in self.nav_buttons:
            button.setVisible(True)

        group = QParallelAnimationGroup(self.nav_bar_frame)
        self._add_width_animation(
            group=group,
            start_width=self.nav_bar_frame.width() or collapsed_width,
            end_width=expanded_width if expanded else collapsed_width,
        )

        for button in self.nav_buttons:
            self._add_opacity_animation(
                group=group,
                button=button,
                start_opacity=0.0 if expanded else 1.0,
                end_opacity=1.0 if expanded else 0.0,
            )

        if not expanded:
            group.finished.connect(self._hide_collapsed_nav_buttons)

        group.finished.connect(lambda: setattr(self, "_navbar_animation", None))
        self._navbar_animation = group
        group.start()

        self._refresh_navbar_style()

    def _refresh_navbar_style(self) -> None:
        self.nav_bar_frame.style().unpolish(self.nav_bar_frame)
        self.nav_bar_frame.style().polish(self.nav_bar_frame)
        self.nav_bar_frame.update()

    def _update_home_toggle_icon(self) -> None:
        self.btn_home.setText("")
        self.btn_home.setIcon(self.icon_collapse if self.navbar_expanded else self.icon_expand)
        self.btn_home.setIconSize(NAVBAR_TOGGLE_ICON_SIZE)

    def _collapsed_navbar_width(self) -> int:
        layout = self.nav_bar_frame.layout()
        margins = layout.contentsMargins() if layout is not None else None
        horizontal_margins = margins.left() + margins.right() if margins is not None else 18
        return self.btn_home.sizeHint().width() + horizontal_margins + 2

    def _expanded_navbar_width(self) -> int:
        layout = self.nav_bar_frame.layout()
        if layout is None:
            spacing = 6
            horizontal_margins = 18
            layout_hint = 0
        else:
            margins = layout.contentsMargins()
            horizontal_margins = margins.left() + margins.right()
            horizontal_spacing = getattr(layout, "horizontalSpacing", None)
            spacing = horizontal_spacing() if horizontal_spacing is not None else layout.spacing()
            if spacing < 0:
                spacing = layout.spacing()
            if spacing < 0:
                spacing = 6
            layout_hint = layout.sizeHint().width()

        buttons = [self.btn_home, *self.nav_buttons]
        button_widths = sum(
            max(button.minimumWidth(), button.sizeHint().width()) for button in buttons
        )
        spacing_width = spacing * max(len(buttons) - 1, 0)
        required_width = button_widths + spacing_width + horizontal_margins + 24

        return max(layout_hint, required_width, self._collapsed_navbar_width())

    def _add_width_animation(
        self,
        group: QParallelAnimationGroup,
        start_width: int,
        end_width: int,
    ) -> None:
        min_animation = QPropertyAnimation(self.nav_bar_frame, b"minimumWidth", group)
        min_animation.setDuration(NAVBAR_ANIMATION_MS)
        min_animation.setStartValue(start_width)
        min_animation.setEndValue(end_width)
        min_animation.setEasingCurve(QEasingCurve.InOutCubic)
        group.addAnimation(min_animation)

        max_animation = QPropertyAnimation(self.nav_bar_frame, b"maximumWidth", group)
        max_animation.setDuration(NAVBAR_ANIMATION_MS)
        max_animation.setStartValue(start_width)
        max_animation.setEndValue(end_width)
        max_animation.setEasingCurve(QEasingCurve.InOutCubic)
        group.addAnimation(max_animation)

    def _add_opacity_animation(
        self,
        group: QParallelAnimationGroup,
        button: QPushButton,
        start_opacity: float,
        end_opacity: float,
    ) -> None:
        effect = self._ensure_opacity_effect(button)
        effect.setOpacity(start_opacity)

        animation = QPropertyAnimation(effect, b"opacity", group)
        animation.setDuration(NAVBAR_ANIMATION_MS)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        group.addAnimation(animation)

    @staticmethod
    def _ensure_opacity_effect(button: QPushButton) -> QGraphicsOpacityEffect:
        effect = button.graphicsEffect()
        if isinstance(effect, QGraphicsOpacityEffect):
            return effect

        effect = QGraphicsOpacityEffect(button)
        button.setGraphicsEffect(effect)
        return effect

    def _hide_collapsed_nav_buttons(self) -> None:
        for button in self.nav_buttons:
            button.setVisible(False)

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
