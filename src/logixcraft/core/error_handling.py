import logging
import sys
import traceback
from types import TracebackType

from PySide6.QtCore import QtMsgType, qInstallMessageHandler
from PySide6.QtWidgets import QApplication

logger = logging.getLogger(__name__)


def format_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_traceback: TracebackType | None,
) -> str:
    return "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))


def show_error_dialog(title: str, message: str, details: str) -> None:
    app = QApplication.instance()
    if app is None:
        return

    from logixcraft.ui.error_dialog import ErrorDialog

    dialog = ErrorDialog(title=title, message=message, details=details)
    dialog.exec()


def handle_uncaught_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_traceback: TracebackType | None,
) -> None:
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    details = format_exception(exc_type, exc_value, exc_traceback)
    logger.critical("Uncaught exception:\n%s", details)
    show_error_dialog(
        title="Unexpected Error",
        message="LogixCraft encountered an unexpected error. The details were written to the log.",
        details=details,
    )


def install_exception_hook() -> None:
    sys.excepthook = handle_uncaught_exception


def qt_message_handler(mode, context, message: str) -> None:
    log_message = f"{message} ({context.file}:{context.line}, {context.function})"

    if mode == QtMsgType.QtDebugMsg:
        logger.debug("Qt: %s", log_message)
    elif mode == QtMsgType.QtInfoMsg:
        logger.info("Qt: %s", log_message)
    elif mode == QtMsgType.QtWarningMsg:
        logger.warning("Qt: %s", log_message)
    elif mode == QtMsgType.QtCriticalMsg:
        logger.error("Qt: %s", log_message)
    elif mode == QtMsgType.QtFatalMsg:
        logger.critical("Qt: %s", log_message)
    else:
        logger.info("Qt: %s", log_message)


def install_qt_message_handler() -> None:
    qInstallMessageHandler(qt_message_handler)
