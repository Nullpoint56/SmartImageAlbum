import logging
import os

from app.config.app import get_app_config


async def setup_logging():
    config = get_app_config()
    log_path = os.path.abspath(config.logger.file_location)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config.logger.level.upper(), logging.DEBUG),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )