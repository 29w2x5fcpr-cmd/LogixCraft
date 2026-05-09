def build_stylesheet(theme: dict) -> str:
    color = theme["color"]
    radius = theme["radius"]
    size = theme["size"]
    font = theme["font"]

    return f"""
    * {{
        font-size: {font["base_size"]};
    }}

    QMainWindow {{
        background-color: {color["app_bg"]};
        color: {color["text_primary"]};
    }}

    QWidget#centralwidget {{
        background-color: {color["app_bg"]};
        color: {color["text_primary"]};
    }}

    QFrame#headerContainer,
    QFrame#sidebarContainer {{
        background-color: {color["panel_bg"]};
        color: {color["text_primary"]};
    }}

    QWidget#contentContainer,
    QStackedWidget#mainStack {{
        background-color: {color["content_bg"]};
        color: {color["text_primary"]};
    }}

    QFrame#headerContainer {{
        border-bottom: 1px solid {color["border"]};
    }}

    QFrame#sidebarContainer {{
        border-right: 1px solid {color["border"]};
    }}

    QStackedWidget#sidebarStack,
    QWidget#page_sidebar_plc {{
        background-color: {color["panel_bg"]};
        border: none;
    }}

    QLabel#headerTitleLabel,
    QLabel#pageTitleLabel {{
        color: {color["text_primary"]};
        font-weight: 600;
        background-color: transparent;
    }}

    QPushButton {{
        background-color: {color["button_bg"]};
        border: 1px solid {color["border"]};
        padding: 8px 12px;
        border-radius: {radius["button"]};
    }}

    QPushButton:hover {{
        background-color: {color["button_hover_bg"]};
    }}

    QPushButton:pressed,
    QPushButton[active="true"] {{
        background-color: {color["button_active_bg"]};
    }}

    QLabel#homeImage {{
        background: transparent;
    }}  
    QPushButton#btnHome {{
    background-color: {color["home_button_bg"]};
    color: {color["home_button_text"]};
    border: none;

    min-width: {size["home_button"]};
    max-width: {size["home_button"]};
    min-height: {size["home_button"]};
    max-height: {size["home_button"]};

    border-radius: {radius["home_button"]};
    padding: 0px;
    }}   
    QPushButton#btnHome:hover {{
        background-color: {color["home_button_hover_bg"]};
    }} 
    QPushButton#btnHome:pressed {{
        background-color: {color["home_button_pressed_bg"]};
    }}
    QPushButton[active="true"] {{
        background-color: {color["button_active_bg"]};
        color: {color["text_primary"]};
        border: none;
    }}    
    QPushButton#btnPLC {{
        background-color: {color["nav_button_bg"]};
        color: {color["nav_button_text"]};
        border: none;
        font-size: {font["nav_button_size"]};
        font-weight: {font["nav_button_weight"]};

        min-height: {size["nav_button_height"]};
        max-height: {size["nav_button_height"]};

        padding: 0px {size["nav_button_horizontal_padding"]};
        border-radius: {radius["pill"]};
    }}

    QPushButton#btnPLC:hover {{
        background-color: {color["nav_button_hover_bg"]};
    }}

    QPushButton#btnPLC:pressed {{
        background-color: {color["nav_button_pressed_bg"]};
    }}

    QPushButton#btnPLC[active="true"] {{
        background-color: {color["nav_button_active_bg"]};
        color: {color["nav_button_active_text"]};
        border-radius: {radius["pill"]};
    }}
    QFrame#navBarFrame {{
        background-color: {color["panel_bg_emphasis"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["navbar"]};
        min-height: {size["navbar_height"]};
        max-height: {size["navbar_height"]};
    }}

    QDialog#preferencesDialog {{
        background-color: {color["app_bg"]};
        color: {color["text_primary"]};
    }}

    QLabel#settingsTitle {{
        color: {color["text_primary"]};
        font-size: {font["preferences_title_size"]};
        font-weight: 700;
        background-color: transparent;
    }}

    QLabel#settingsSubtitle {{
        color: {color["text_secondary"]};
        background-color: transparent;
    }}

    QFrame#preferencesSidebar {{
        background-color: {color["panel_bg"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
    }}

    QStackedWidget#preferencesPages,
    QWidget#preferencesPage {{
        background-color: {color["content_bg"]};
        color: {color["text_primary"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
    }}

    QPushButton#preferencesNavButton {{
        background-color: transparent;
        color: {color["text_primary"]};
        border: none;
        border-radius: {radius["button"]};
        padding: 9px 10px;
        text-align: left;
        min-height: 34px;
    }}

    QPushButton#preferencesNavButton:hover {{
        background-color: {color["button_hover_bg"]};
    }}

    QPushButton#preferencesNavButton:checked {{
        background-color: {color["button_active_bg"]};
        color: {color["text_primary"]};
    }}

    QDialog#terminalDialog {{
        background-color: {color["app_bg"]};
        color: {color["text_primary"]};
    }}

    QLabel#terminalTitle {{
        color: {color["text_primary"]};
        font-size: {font["preferences_title_size"]};
        font-weight: 700;
        background-color: transparent;
    }}

    QLabel#terminalSubtitle {{
        color: {color["text_secondary"]};
        background-color: transparent;
    }}

    QTextEdit#terminalOutput {{
        background-color: {color["panel_bg_emphasis"]};
        color: {color["text_primary"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
        padding: 10px;
    }}

    QDialog#licenseDialog {{
        background-color: {color["app_bg"]};
        color: {color["text_primary"]};
    }}

    QLabel#licenseTitle {{
        color: {color["text_primary"]};
        font-size: {font["preferences_title_size"]};
        font-weight: 700;
        background-color: transparent;
    }}

    QLabel#licenseSubtitle {{
        color: {color["text_secondary"]};
        background-color: transparent;
        font-size: {font["base_size"]};
    }}

    QTextEdit#licenseContent {{
        background-color: {color["panel_bg"]};
        color: {color["text_primary"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
        padding: 16px;
        selection-background-color: {color["button_active_bg"]};
    }}

    QDialog#softwareDialog {{
        background-color: {color["app_bg"]};
        color: {color["text_primary"]};
    }}

    QLabel#softwareLogo {{
        background-color: transparent;
    }}

    QLabel#softwareTitle {{
        color: {color["text_primary"]};
        font-size: 28px;
        font-weight: 700;
        background-color: transparent;
    }}

    QLabel#softwareSubtitle {{
        color: {color["text_secondary"]};
        background-color: transparent;
    }}

    QFrame#softwareInfoFrame {{
        background-color: {color["panel_bg"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
    }}

    QLabel#softwareInfoKey {{
        color: {color["text_secondary"]};
        font-weight: 600;
        background-color: transparent;
    }}

    QLabel#softwareInfoValue {{
        color: {color["text_primary"]};
        background-color: transparent;
    }}

    QDialog#errorDialog {{
        background-color: {color["app_bg"]};
        color: {color["text_primary"]};
    }}

    QLabel#errorTitle {{
        color: {color["text_primary"]};
        font-size: {font["preferences_title_size"]};
        font-weight: 700;
        background-color: transparent;
    }}

    QLabel#errorMessage {{
        color: {color["text_secondary"]};
        background-color: transparent;
    }}

    QTextEdit#errorDetails {{
        background-color: {color["panel_bg_emphasis"]};
        color: {color["text_primary"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
        padding: 10px;
    }}
    """
