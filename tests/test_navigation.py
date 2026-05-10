import sys

from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QWidget,
)

from logixcraft.ui.navigation import NavigationController


def build_navigation_window() -> QMainWindow:
    window = QMainWindow()

    btn_home = QPushButton(window)
    btn_home.setObjectName("btnHome")
    btn_plc = QPushButton(window)
    btn_plc.setObjectName("btnPLC")

    sidebar_container = QFrame(window)
    sidebar_container.setObjectName("sidebarContainer")

    sidebar_stack = QStackedWidget(sidebar_container)
    sidebar_stack.setObjectName("sidebarStack")
    page_sidebar_home = QWidget()
    page_sidebar_home.setObjectName("page_sidebar_home")
    page_sidebar_plc = QWidget()
    page_sidebar_plc.setObjectName("page_sidebar_plc")
    sidebar_stack.addWidget(page_sidebar_home)
    sidebar_stack.addWidget(page_sidebar_plc)

    main_stack = QStackedWidget(window)
    main_stack.setObjectName("mainStack")
    page_main_home = QWidget()
    page_main_home.setObjectName("page_main_home")
    page_main_plc = QWidget()
    page_main_plc.setObjectName("page_main_plc")
    main_stack.addWidget(page_main_home)
    main_stack.addWidget(page_main_plc)

    status_bar = QStatusBar(window)
    status_bar.setObjectName("statusbar")
    window.setStatusBar(status_bar)

    return window


def test_sidebar_hides_on_home_and_shows_on_plc() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    window = build_navigation_window()

    navigation = NavigationController(window=window)

    navigation.navigate("home")
    assert navigation.sidebar_container.isHidden()

    navigation.navigate("plc")
    assert not navigation.sidebar_container.isHidden()
    assert app is not None
