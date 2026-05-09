import logging
import traceback
from collections.abc import Callable

from logixcraft.core.error_handling import show_error_dialog

logger = logging.getLogger(__name__)


def run_safely[T](action_name: str, callback: Callable[[], T]) -> T | None:
    try:
        return callback()
    except Exception as exc:
        details = traceback.format_exc()
        logger.exception("Failed to run action '%s': %s", action_name, exc)
        show_error_dialog(
            title="Action Failed",
            message=f"LogixCraft could not complete: {action_name}.",
            details=details,
        )
        return None
