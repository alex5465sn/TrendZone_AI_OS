import logging
import os
import sys


LOGGER_NAME = "TrendZone AI OS"

LOG_FOLDER = "logs"

LOG_FILE = os.path.join(
    LOG_FOLDER,
    "trendzone.log",
)


os.makedirs(
    LOG_FOLDER,
    exist_ok=True,
)


logger = logging.getLogger(LOGGER_NAME)

logger.setLevel(logging.DEBUG)


if not logger.handlers:

    formatter = logging.Formatter(

        "[%(asctime)s] %(levelname)s | %(message)s",

        datefmt="%Y-%m-%d %H:%M:%S",

    )

    # ==========================================
    # Console
    # ==========================================

    console = logging.StreamHandler(sys.stdout)

    console.setLevel(logging.INFO)

    console.setFormatter(formatter)

    logger.addHandler(console)

    # ==========================================
    # Arquivo
    # ==========================================

    file_handler = logging.FileHandler(

        LOG_FILE,

        encoding="utf-8",

    )

    file_handler.setLevel(logging.DEBUG)

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


class TZLogger:

    @staticmethod
    def debug(agent: str, message: str):

        logger.debug(f"[{agent}] {message}")

    @staticmethod
    def info(agent: str, message: str):

        logger.info(f"[{agent}] {message}")

    @staticmethod
    def success(agent: str, message: str):

        logger.info(f"✅ [{agent}] {message}")

    @staticmethod
    def warning(agent: str, message: str):

        logger.warning(f"⚠️ [{agent}] {message}")

    @staticmethod
    def error(agent: str, message: str):

        logger.error(f"❌ [{agent}] {message}")

    @staticmethod
    def critical(agent: str, message: str):

        logger.critical(f"🔥 [{agent}] {message}")