import logging

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from logixcraft.core.config import SETTINGS_FILE
from logixcraft.core.fonts import DEFAULT_FONT_FAMILY
from logixcraft.core.settings.defaults import DEFAULT_SETTINGS

logger = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    def __init__(self, settings, theme_manager, font_manager, parent=None) -> None:
        super().__init__(parent)
        self.settings = settings
        self.theme_manager = theme_manager
        self.font_manager = font_manager

        self.setObjectName("preferencesDialog")
        self.setWindowTitle("Preferences")
        self.resize(720, 480)
        self.setMinimumSize(660, 430)

        self._build_ui()
        self._load_current_values()

    def _build_ui(self) -> None:
        self.title_label = QLabel("Preferences")
        self.title_label.setObjectName("settingsTitle")

        self.subtitle_label = QLabel("Manage appearance and application defaults.")
        self.subtitle_label.setObjectName("settingsSubtitle")
        self.subtitle_label.setWordWrap(True)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("preferencesSidebar")
        self.sidebar.setMinimumWidth(170)
        self.sidebar.setMaximumWidth(190)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(6)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        self.button_appearance = self._create_nav_button("Appearance", 0)
        self.button_window = self._create_nav_button("Window", 1)
        self.button_advanced = self._create_nav_button("Advanced", 2)

        sidebar_layout.addWidget(self.button_appearance)
        sidebar_layout.addWidget(self.button_window)
        sidebar_layout.addWidget(self.button_advanced)
        sidebar_layout.addStretch()
        self.sidebar.setLayout(sidebar_layout)

        self.pages = QStackedWidget()
        self.pages.setObjectName("preferencesPages")

        self.page_appearance = QWidget()
        self.page_appearance.setObjectName("preferencesPage")
        appearance_page_layout = QVBoxLayout()
        appearance_page_layout.setContentsMargins(18, 18, 18, 18)
        appearance_page_layout.setSpacing(12)
        appearance_page_layout.addWidget(self._create_page_title("Appearance"))
        appearance_page_layout.addWidget(
            self._create_page_note("Choose the active theme and application font.")
        )

        appearance_layout = QFormLayout()
        appearance_layout.setContentsMargins(0, 0, 0, 0)
        appearance_layout.setHorizontalSpacing(16)
        appearance_layout.setVerticalSpacing(14)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.available_themes())
        appearance_layout.addRow("Theme:", self.theme_combo)

        self.font_combo = QComboBox()
        self.font_combo.addItems(self.font_manager.available_families())
        appearance_layout.addRow("Font:", self.font_combo)
        appearance_page_layout.addLayout(appearance_layout)

        self.font_preview = QLabel("LogixCraft engineering workspace")
        self.font_preview.setObjectName("preferencesFontPreview")
        appearance_page_layout.addWidget(self.font_preview)
        appearance_page_layout.addStretch()
        self.page_appearance.setLayout(appearance_page_layout)

        self.page_window = QWidget()
        self.page_window.setObjectName("preferencesPage")
        window_layout = QVBoxLayout()
        window_layout.setContentsMargins(18, 18, 18, 18)
        window_layout.setSpacing(12)
        window_layout.addWidget(self._create_page_title("Window"))

        self.window_info = QLabel("Restore the default application window size.")
        self.window_info.setObjectName("preferencesInfo")
        self.window_info.setWordWrap(True)
        self.current_window_size = QLabel()
        self.current_window_size.setObjectName("preferencesMeta")
        self.button_reset_window = QPushButton("Reset Window Size")

        window_layout.addWidget(self.window_info)
        window_layout.addWidget(self.current_window_size)
        window_layout.addWidget(self.button_reset_window)
        window_layout.addStretch()
        self.page_window.setLayout(window_layout)

        self.page_advanced = QWidget()
        self.page_advanced.setObjectName("preferencesPage")
        advanced_layout = QVBoxLayout()
        advanced_layout.setContentsMargins(18, 18, 18, 18)
        advanced_layout.setSpacing(12)
        advanced_layout.addWidget(self._create_page_title("Advanced"))

        self.advanced_info = QLabel("Reset all saved settings back to factory defaults.")
        self.advanced_info.setObjectName("preferencesInfo")
        self.advanced_info.setWordWrap(True)
        self.settings_file_label = QLabel(f"Settings file: {SETTINGS_FILE}")
        self.settings_file_label.setObjectName("preferencesMeta")
        self.settings_file_label.setWordWrap(True)
        self.button_reset_all = QPushButton("Reset All Settings")
        self.button_reset_all.setObjectName("dangerButton")

        advanced_layout.addWidget(self.advanced_info)
        advanced_layout.addWidget(self.settings_file_label)
        advanced_layout.addWidget(self.button_reset_all)
        advanced_layout.addStretch()
        self.page_advanced.setLayout(advanced_layout)

        self.pages.addWidget(self.page_appearance)
        self.pages.addWidget(self.page_window)
        self.pages.addWidget(self.page_advanced)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(14)
        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.pages, 1)

        self.button_box = QDialogButtonBox()
        self.button_cancel = self.button_box.addButton(QDialogButtonBox.Cancel)
        self.button_apply = self.button_box.addButton("Apply", QDialogButtonBox.ApplyRole)
        self.button_save = self.button_box.addButton(QDialogButtonBox.Save)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(18)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)
        main_layout.addLayout(content_layout, 1)
        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)

        self.button_appearance.setChecked(True)
        self.button_cancel.clicked.connect(self.reject)
        self.button_apply.clicked.connect(self.apply_settings)
        self.button_save.clicked.connect(self.save_and_close)
        self.button_reset_all.clicked.connect(self.reset_all_settings)
        self.button_reset_window.clicked.connect(self.reset_window_size)
        self.font_combo.currentTextChanged.connect(self._update_font_preview)

    def _create_page_title(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("preferencesPageTitle")
        return label

    def _create_page_note(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("preferencesInfo")
        label.setWordWrap(True)
        return label

    def _create_nav_button(self, text: str, page_index: int) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("preferencesNavButton")
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button.clicked.connect(lambda: self.pages.setCurrentIndex(page_index))
        self.nav_group.addButton(button)
        return button

    def _load_current_values(self) -> None:
        current_theme = self.settings.get("appearance", "theme", default="dark")
        index = self.theme_combo.findText(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        current_font = self.font_manager.resolve_family(
            self.settings.get("appearance", "font_family", default=DEFAULT_FONT_FAMILY)
        )
        index = self.font_combo.findText(current_font)
        if index >= 0:
            self.font_combo.setCurrentIndex(index)
        self._update_font_preview(current_font)

        self._refresh_window_size_label()

    def apply_settings(self) -> None:
        selected_theme = self.theme_combo.currentText()
        selected_font = self.font_combo.currentText()
        self.settings.set("appearance", "theme", value=selected_theme)
        self.settings.set("appearance", "font_family", value=selected_font)
        self.settings.save()

        app = QApplication.instance()
        if app is not None:
            self.font_manager.apply_font(app, selected_font)
            self.theme_manager.apply_theme(app, selected_theme)

        logger.info("Settings applied from settings dialog")

    def save_and_close(self) -> None:
        self.apply_settings()
        self.accept()

    def reset_all_settings(self) -> None:
        result = QMessageBox.question(
            self,
            "Reset All Settings",
            "Reset all settings to default values?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if result != QMessageBox.Yes:
            return

        self.settings.reset_to_defaults()
        self.settings.save()

        default_theme = self.settings.get("appearance", "theme", default="dark")
        index = self.theme_combo.findText(default_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        default_font = self.font_manager.resolve_family(
            self.settings.get("appearance", "font_family", default=DEFAULT_FONT_FAMILY)
        )
        index = self.font_combo.findText(default_font)
        if index >= 0:
            self.font_combo.setCurrentIndex(index)

        app = QApplication.instance()
        if app is not None:
            self.font_manager.apply_font(app, default_font)
            self.theme_manager.apply_theme(app, default_theme)

        if self.parent() is not None:
            self.parent().resize(
                DEFAULT_SETTINGS["window"]["width"],
                DEFAULT_SETTINGS["window"]["height"],
            )

        logger.info("All settings reset to defaults")
        self._refresh_window_size_label()

    def reset_window_size(self) -> None:
        width = DEFAULT_SETTINGS["window"]["width"]
        height = DEFAULT_SETTINGS["window"]["height"]

        self.settings.save_window_size(width, height)

        if self.parent() is not None:
            self.parent().resize(width, height)

        logger.info("Window size reset to defaults")
        self._refresh_window_size_label()

    def _refresh_window_size_label(self) -> None:
        width = self.settings.get("window", "width", default=DEFAULT_SETTINGS["window"]["width"])
        height = self.settings.get("window", "height", default=DEFAULT_SETTINGS["window"]["height"])
        self.current_window_size.setText(f"Current saved size: {width} x {height}")

    def _update_font_preview(self, family: str) -> None:
        self.font_preview.setFont(QFont(family, 11))
