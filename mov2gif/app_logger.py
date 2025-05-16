import logging
from logging.handlers import TimedRotatingFileHandler
import os

APP_ROOT = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(APP_ROOT, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_PATH = os.path.join(LOG_DIR, "app.log")


class AppLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AppLogger, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.logger = logging.getLogger("AppLogger")
            self.logger.setLevel(logging.DEBUG)

            # StreamHandler
            sh = logging.StreamHandler()
            sh_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            sh.setFormatter(sh_formatter)
            self.logger.addHandler(sh)

            trfh = TimedRotatingFileHandler(
                LOG_PATH, when="midnight", interval=1, backupCount=7
            )
            trfh_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            trfh.setFormatter(trfh_formatter)
            self.logger.addHandler(trfh)

            self._initialized = True

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def critical(self, message: str):
        self.logger.critical(message)


# 動作確認用
if __name__ == "__main__":
    AppLogger().debug("This is a debug message")
    AppLogger().info("This is an info message")
    AppLogger().warning("This is a warning message")
    AppLogger().error("This is an error message")
    AppLogger().critical("This is a critical message")
