import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILE_NAME = "logixcraft.log"
MAX_LOG_BYTES = 1_000_000
BACKUP_LOG_COUNT = 5


def setup_logging(
    log_dir: Path,
    max_bytes: int = MAX_LOG_BYTES,
    backup_count: int = BACKUP_LOG_COUNT,
) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / LOG_FILE_NAME

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    stream_handler = logging.StreamHandler()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            file_handler,
            stream_handler,
        ],
        force=True,
    )
