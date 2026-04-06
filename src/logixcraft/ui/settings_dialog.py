import logging

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from logixcraft.core.settings.defaults import DEFAULT_SETTINGS

logger = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    def __init__(self, settings, theme_manager, parent=None) -> None:
        super().__init__(parent)
        self.settings = settings
        self.theme_manager = theme_manager

        self.setWindowTitle("Settings")
        self.resize(680, 520)
        self.setMinimumSize(620, 480)

        self._build_ui()
        self._load_current_values()

    def _build_ui(self) -> None:
        self.title_label = QLabel("LogixCraft Settings")
        self.title_label.setObjectName("settingsTitle")

        self.subtitle_label = QLabel("Manage appearance and application defaults.")
        self.subtitle_label.setObjectName("settingsSubtitle")
        self.subtitle_label.setWordWrap(True)

        self.group_appearance = QGroupBox("Appearance")
        self.group_appearance.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        appearance_layout = QFormLayout()
        appearance_layout.setContentsMargins(16, 20, 16, 16)
        appearance_layout.setHorizontalSpacing(16)
        appearance_layout.setVerticalSpacing(14)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.available_themes())
        appearance_layout.addRow("Theme:", self.theme_combo)

        self.group_appearance.setLayout(appearance_layout)

        self.group_window = QGroupBox("Window")
        self.group_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        window_layout = QVBoxLayout()
        window_layout.setContentsMargins(16, 20, 16, 16)
        window_layout.setSpacing(12)

        self.window_info = QLabel("Restore the default application window size.")
        self.window_info.setWordWrap(True)
        self.button_reset_window = QPushButton("Reset Window Size")

        window_layout.addWidget(self.window_info)
        window_layout.addWidget(self.button_reset_window)

        self.group_window.setLayout(window_layout)

        self.group_advanced = QGroupBox("Advanced")
        self.group_advanced.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        advanced_layout = QVBoxLayout()
        advanced_layout.setContentsMargins(16, 20, 16, 16)
        advanced_layout.setSpacing(12)

        self.advanced_info = QLabel("Reset all saved settings back to factory defaults.")
        self.advanced_info.setWordWrap(True)
        self.button_reset_all = QPushButton("Reset All Settings")
        self.button_reset_all.setObjectName("dangerButton")

        advanced_layout.addWidget(self.advanced_info)
        advanced_layout.addWidget(self.button_reset_all)

        self.group_advanced.setLayout(advanced_layout)

        self.button_box = QDialogButtonBox()
        self.button_cancel = self.button_box.addButton(QDialogButtonBox.Cancel)
        self.button_apply = self.button_box.addButton("Apply", QDialogButtonBox.ApplyRole)
        self.button_save = self.button_box.addButton(QDialogButtonBox.Save)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(18)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)
        main_layout.addWidget(self.group_appearance)
        main_layout.addWidget(self.group_window)
        main_layout.addWidget(self.group_advanced)
        main_layout.addStretch()
        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)

        self.button_cancel.clicked.connect(self.reject)
        self.button_apply.clicked.connect(self.apply_settings)
        self.button_save.clicked.connect(self.save_and_close)
        self.button_reset_all.clicked.connect(self.reset_all_settings)
        self.button_reset_window.clicked.connect(self.reset_window_size)

    def _load_current_values(self) -> None:
        current_theme = self.settings.get("appearance", "theme", default="dark")
        index = self.theme_combo.findText(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

    def apply_settings(self) -> None:
        selected_theme = self.theme_combo.currentText()
        self.settings.set("appearance", "theme", value=selected_theme)
        self.settings.save()

        app = QApplication.instance()
        if app is not None:
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

        app = QApplication.instance()
        if app is not None:
            self.theme_manager.apply_theme(app, default_theme)

        if self.parent() is not None:
            self.parent().resize(
                DEFAULT_SETTINGS["window"]["width"],
                DEFAULT_SETTINGS["window"]["height"],
            )

        logger.info("All settings reset to defaults")

    def reset_window_size(self) -> None:
        width = DEFAULT_SETTINGS["window"]["width"]
        height = DEFAULT_SETTINGS["window"]["height"]

        self.settings.save_window_size(width, height)

        if self.parent() is not None:
            self.parent().resize(width, height)

        logger.info("Window size reset to defaults")
