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
    QPushButton[navButton="true"] {{
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

    QPushButton[navButton="true"]:hover {{
        background-color: {color["nav_button_hover_bg"]};
    }}

    QPushButton[navButton="true"]:pressed {{
        background-color: {color["nav_button_pressed_bg"]};
    }}

    QPushButton[navButton="true"][active="true"] {{
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

    QFrame#navBarFrame[expanded="false"] {{
        background-color: {color["panel_bg_emphasis"]};
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

    QLabel#preferencesPageTitle {{
        color: {color["text_primary"]};
        font-size: 16px;
        font-weight: 700;
        background-color: transparent;
    }}

    QLabel#preferencesInfo {{
        color: {color["text_secondary"]};
        background-color: transparent;
    }}

    QLabel#preferencesMeta {{
        color: {color["text_secondary"]};
        background-color: {color["panel_bg"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
        padding: 8px 10px;
    }}

    QLabel#preferencesFontPreview {{
        color: {color["text_primary"]};
        background-color: {color["panel_bg"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
        padding: 12px;
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

    QDialog#aboutDialog {{
        background-color: {color["app_bg"]};
        color: {color["text_primary"]};
    }}

    QLabel#aboutLogo {{
        background-color: transparent;
    }}

    QLabel#aboutTitle {{
        color: {color["text_primary"]};
        font-size: 26px;
        font-weight: 700;
        background-color: transparent;
    }}

    QLabel#aboutSubtitle {{
        color: {color["text_secondary"]};
        background-color: transparent;
    }}

    QFrame#aboutInfoFrame {{
        background-color: {color["panel_bg"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
    }}

    QLabel#aboutInfoKey {{
        color: {color["text_secondary"]};
        font-weight: 600;
        background-color: transparent;
    }}

    QLabel#aboutInfoValue {{
        color: {color["text_primary"]};
        background-color: transparent;
    }}

    QDialog#helpViewerDialog {{
        background-color: {color["app_bg"]};
        color: {color["text_primary"]};
    }}

    QLabel#helpTitle {{
        color: {color["text_primary"]};
        font-size: {font["preferences_title_size"]};
        font-weight: 700;
        background-color: transparent;
    }}

    QLabel#helpSubtitle {{
        color: {color["text_secondary"]};
        background-color: transparent;
    }}

    QLineEdit#helpSearch {{
        background-color: {color["panel_bg"]};
        color: {color["text_secondary"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
        padding: 8px 10px;
    }}

    QFrame#helpContentFrame {{
        background-color: {color["panel_bg"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
    }}

    QListWidget#helpTopicList {{
        background-color: {color["content_bg"]};
        color: {color["text_primary"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
        padding: 6px;
    }}

    QListWidget#helpTopicList::item {{
        min-height: 28px;
        padding: 4px 8px;
        border-radius: {radius["button"]};
    }}

    QListWidget#helpTopicList::item:selected {{
        background-color: {color["button_active_bg"]};
        color: {color["text_primary"]};
    }}

    QTextEdit#helpContent {{
        background-color: {color["content_bg"]};
        color: {color["text_primary"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
        padding: 12px;
        selection-background-color: {color["button_active_bg"]};
    }}

    QDialog#errorDialog {{
        background-color: {color["app_bg"]};
        color: {color["text_primary"]};
    }}

    QFrame#errorHeader {{
        background-color: {color["panel_bg"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
    }}

    QLabel#errorIcon {{
        background-color: transparent;
        border: none;
    }}

    QLabel#errorTitle {{
        color: {color["text_primary"]};
        font-size: 15px;
        font-weight: 700;
        background-color: transparent;
    }}

    QLabel#errorMessage {{
        color: {color["text_secondary"]};
        background-color: transparent;
    }}

    QFrame#errorSummary {{
        background-color: {color["content_bg"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
    }}

    QLabel#errorSummaryKey {{
        color: {color["text_secondary"]};
        font-weight: 600;
        background-color: transparent;
    }}

    QLabel#errorSummaryValue {{
        color: {color["text_primary"]};
        background-color: transparent;
    }}

    QTextEdit#errorDetails {{
        background-color: {color["panel_bg_emphasis"]};
        color: {color["text_primary"]};
        border: 1px solid {color["border"]};
        border-radius: {radius["button"]};
        padding: 10px;
    }}

    QPushButton#errorDetailsButton {{
        background-color: transparent;
        color: {color["text_secondary"]};
        border: none;
        padding: 4px 6px;
    }}

    QPushButton#errorDetailsButton:hover {{
        color: {color["text_primary"]};
        background-color: {color["button_hover_bg"]};
        border-radius: {radius["button"]};
    }}
    """
