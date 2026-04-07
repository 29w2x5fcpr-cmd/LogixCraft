def build_stylesheet(theme: dict) -> str:
    return f"""
    QWidget {{
        background-color: {theme["bg_app"]};
        color: {theme["text_primary"]};
    }}

    QFrame#headerContainer,
    QFrame#sidebarContainer {{
        background-color: {theme["bg_panel"]};
    }}

    QWidget#contentContainer {{
        background-color: {theme["bg_content"]};
    }}

    QFrame#headerContainer {{
        border-bottom: 1px solid {theme["border"]};
    }}

    QFrame#sidebarContainer {{
        border-right: 1px solid {theme["border"]};
    }}

    QLabel#headerTitleLabel,
    QLabel#pageTitleLabel {{
        color: {theme["text_primary"]};
        font-weight: 600;
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
    """
