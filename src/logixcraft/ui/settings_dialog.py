import logging

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
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
        self.setMinimumWidth(360)

        self.theme_label = QLabel("Theme")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.available_themes())

        current_theme = self.settings.get("appearance", "theme", default="dark")
        index = self.theme_combo.findText(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        self.button_save = QPushButton("Save")
        self.button_cancel = QPushButton("Cancel")
        self.button_reset_all = QPushButton("Reset All Settings")
        self.button_reset_window = QPushButton("Reset Window Size")

        self.button_save.clicked.connect(self.save_settings)
        self.button_cancel.clicked.connect(self.reject)
        self.button_reset_all.clicked.connect(self.reset_all_settings)
        self.button_reset_window.clicked.connect(self.reset_window_size)

        main_layout = QVBoxLayout()
        theme_row = QHBoxLayout()
        action_row = QHBoxLayout()
        bottom_row = QHBoxLayout()

        theme_row.addWidget(self.theme_label)
        theme_row.addWidget(self.theme_combo)

        action_row.addWidget(self.button_reset_window)
        action_row.addWidget(self.button_reset_all)

        bottom_row.addStretch()
        bottom_row.addWidget(self.button_cancel)
        bottom_row.addWidget(self.button_save)

        main_layout.addLayout(theme_row)
        main_layout.addSpacing(12)
        main_layout.addLayout(action_row)
        main_layout.addSpacing(18)
        main_layout.addLayout(bottom_row)

        self.setLayout(main_layout)

    def save_settings(self) -> None:
        selected_theme = self.theme_combo.currentText()
        self.settings.set("appearance", "theme", value=selected_theme)
        self.settings.save()
        logger.info("Settings saved from settings dialog")
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

        default_theme = self.settings.get("appearance", "theme", default="dark")
        index = self.theme_combo.findText(default_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        self.settings.save()
        logger.info("All settings reset to defaults")

    def reset_window_size(self) -> None:
        self.settings.save_window_size(
            DEFAULT_SETTINGS["window"]["width"],
            DEFAULT_SETTINGS["window"]["height"],
        )

        if self.parent() is not None:
            self.parent().resize(
                DEFAULT_SETTINGS["window"]["width"],
                DEFAULT_SETTINGS["window"]["height"],
            )

        logger.info("Window size reset to defaults")
