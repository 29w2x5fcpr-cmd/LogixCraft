import logging

logger = logging.getLogger(__name__)


class AppController:
    def __init__(self) -> None:
        logger.info("Controller initialized")

    def handle_test_button(self) -> str:
        logger.info("Handling test button logic")
        return "Button clicked (from controller)"
