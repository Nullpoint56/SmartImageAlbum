import logging
import os

from config.logger import LoggerSettings


async def setup_logging(logging_config: LoggerSettings):
    log_path = os.path.abspath(logging_config.file_location)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, logging_config.level.upper(), logging.DEBUG),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )