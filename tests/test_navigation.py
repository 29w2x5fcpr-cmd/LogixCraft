import sys

from PySide6.QtTest import QTest
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QWidget,
)

from logixcraft.ui.navigation import NavigationController


def build_navigation_window() -> QMainWindow:
    window = QMainWindow()

    nav_bar_frame = QFrame(window)
    nav_bar_frame.setObjectName("navBarFrame")
    nav_layout = QHBoxLayout()
    nav_layout.setContentsMargins(9, 1, 9, 1)
    nav_bar_frame.setLayout(nav_layout)

    btn_home = QPushButton(nav_bar_frame)
    btn_home.setObjectName("btnHome")
    nav_layout.addWidget(btn_home)
    btn_plc = QPushButton(nav_bar_frame)
    btn_plc.setObjectName("btnPLC")
    nav_layout.addWidget(btn_plc)
    btn_network = QPushButton(nav_bar_frame)
    btn_network.setObjectName("btnNetwork")
    nav_layout.addWidget(btn_network)
    btn_os = QPushButton(nav_bar_frame)
    btn_os.setObjectName("pushOS")
    nav_layout.addWidget(btn_os)

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


def test_navbar_buttons_share_nav_button_style_marker() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    window = build_navigation_window()

    navigation = NavigationController(window=window)

    assert navigation.btn_home.property("navButton") is None
    assert window.findChild(QPushButton, "btnPLC").property("navButton") is True
    assert window.findChild(QPushButton, "btnNetwork").property("navButton") is True
    assert window.findChild(QPushButton, "pushOS").property("navButton") is True
    assert app is not None


def test_home_button_icon_tracks_navbar_state() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    window = build_navigation_window()

    navigation = NavigationController(window=window)
    collapsed_icon_key = navigation.btn_home.icon().cacheKey()

    assert not navigation.btn_home.icon().isNull()

    navigation.btn_home.click()
    expanded_icon_key = navigation.btn_home.icon().cacheKey()

    assert expanded_icon_key != collapsed_icon_key

    navigation.btn_home.click()

    assert navigation.btn_home.icon().cacheKey() == collapsed_icon_key
    assert app is not None


def test_home_button_toggles_navbar_buttons() -> None:
    app = QApplication.instance() or QApplication(sys.argv)
    window = build_navigation_window()

    navigation = NavigationController(window=window)
    btn_network = window.findChild(QPushButton, "btnNetwork")
    btn_os = window.findChild(QPushButton, "pushOS")

    assert navigation.navbar_expanded is False
    assert navigation.btn_plc.isHidden()
    assert btn_network.isHidden()
    assert btn_os.isHidden()
    assert not navigation.btn_home.isHidden()

    navigation.btn_home.click()
    assert navigation.navbar_expanded is True
    assert not navigation.btn_plc.isHidden()
    assert not btn_network.isHidden()
    assert not btn_os.isHidden()
    assert navigation._navbar_animation is not None
    QTest.qWait(420)
    assert navigation.nav_bar_frame.width() >= navigation._expanded_navbar_width()

    navigation.btn_home.click()
    assert navigation.navbar_expanded is False
    assert not navigation.btn_plc.isHidden()
    QTest.qWait(420)
    assert navigation.btn_plc.isHidden()
    assert btn_network.isHidden()
    assert btn_os.isHidden()
    assert app is not None
