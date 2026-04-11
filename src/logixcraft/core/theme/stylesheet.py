def build_stylesheet(theme: dict) -> str:
    return f"""
    QMainWindow {{
        background-color: {theme["bg_app"]};
        color: {theme["text_primary"]};
    }}

    QWidget#centralWidget {{
        background-color: {theme["bg_app"]};
        color: {theme["text_primary"]};
    }}

    QFrame#headerContainer,
    QFrame#sidebarContainer {{
        background-color: {theme["bg_panel"]};
        color: {theme["text_primary"]};
    }}

    QWidget#contentContainer,
    QStackedWidget#mainStack {{
        background-color: {theme["bg_content"]};
        color: {theme["text_primary"]};
    }}

    QFrame#headerContainer {{
        border-bottom: 1px solid {theme["border"]};
    }}

    QFrame#sidebarContainer {{
        border-right: 1px solid {theme["border"]};
    }}

    QStackedWidget#sidebarStack,
    QWidget#page_sidebar_plc {{
        background-color: {theme["bg_panel"]};
        border: none;
    }}

    QLabel#headerTitleLabel,
    QLabel#pageTitleLabel {{
        color: {theme["text_primary"]};
        font-weight: 600;
        background-color: transparent;
    }}

    QPushButton {{
        background-color: {theme["bg_button"]};
        border: 1px solid {theme["border"]};
        padding: 8px 12px;
        border-radius: 8px;
    }}

    QPushButton:hover {{
        background-color: {theme["bg_button_hover"]};
    }}

    QPushButton:pressed,
    QPushButton[active="true"] {{
        background-color: {theme["bg_button_active"]};
    }}

    QLabel#homeImage {{
        background: transparent;
    }}  
    QPushButton#btnHome {{
    background-color: white;
    color: black;
    border-radius: 16px;
    padding: 8px 14px;
    }}   
    QPushButton#BtnHome:hover {{
        background-color: #e6e6e6;
    }}  
    """
