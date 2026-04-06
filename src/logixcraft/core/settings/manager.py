import json
import logging
from copy import deepcopy
from pathlib import Path
from typing import Any

from logixcraft.core.config import SETTINGS_FILE
from logixcraft.core.settings.defaults import DEFAULT_SETTINGS

logger = logging.getLogger(__name__)


class SettingsManager:
    def __init__(self, settings_file: Path | None = None) -> None:
        self.settings_file = settings_file or SETTINGS_FILE
        self._settings = deepcopy(DEFAULT_SETTINGS)

    def load(self) -> None:
        if not self.settings_file.exists():
            logger.info("Settings file not found. Using defaults.")
            self.save()
            return

        try:
            with self.settings_file.open("r", encoding="utf-8") as f:
                loaded = json.load(f)

            if not isinstance(loaded, dict):
                raise ValueError("Settings file root must be a dictionary.")

            self._deep_update(self._settings, loaded)
            logger.info("Settings loaded from %s", self.settings_file)

        except Exception as exc:
            logger.exception("Failed to load settings. Using defaults. Error: %s", exc)
            self._settings = deepcopy(DEFAULT_SETTINGS)
            self.save()

    def save(self) -> None:
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)

        with self.settings_file.open("w", encoding="utf-8") as f:
            json.dump(self._settings, f, indent=4)

        logger.info("Settings saved to %s", self.settings_file)

    def get(self, *keys: str, default: Any = None) -> Any:
        value: Any = self._settings
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return default
            value = value[key]
        return value

    def set(self, *keys: str, value: Any) -> None:
        if not keys:
            raise ValueError("At least one key must be provided.")

        target = self._settings
        for key in keys[:-1]:
            if key not in target or not isinstance(target[key], dict):
                target[key] = {}
            target = target[key]

        target[keys[-1]] = value

    @property
    def data(self) -> dict:
        return self._settings

    @staticmethod
    def _deep_update(base: dict, incoming: dict) -> None:
        for key, value in incoming.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                SettingsManager._deep_update(base[key], value)
            else:
                base[key] = value
