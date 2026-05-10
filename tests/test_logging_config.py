import logging

from logixcraft.core.logging_config import LOG_FILE_NAME, setup_logging


def test_setup_logging_rotates_log_file(tmp_path) -> None:
    setup_logging(tmp_path, max_bytes=120, backup_count=2)
    logger = logging.getLogger("logixcraft.tests.rotation")

    for index in range(20):
        logger.info("rotation test line %s with enough content to rotate", index)

    for handler in logging.getLogger().handlers:
        handler.flush()

    assert (tmp_path / LOG_FILE_NAME).exists()
    assert list(tmp_path.glob(f"{LOG_FILE_NAME}.*"))
