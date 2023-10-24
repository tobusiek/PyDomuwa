from logging import Logger

from colorlog import ColoredFormatter, StreamHandler, getLogger


def get_logger(logger_name: str) -> Logger:
    handler = StreamHandler()
    logger_fmt = "%(log_color)s%(asctime)s [%(name)s:%(levelname)s] %(funcName)s() %(message)s"
    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
    handler.setFormatter(ColoredFormatter(logger_fmt, log_colors=log_colors))
    logger = getLogger(logger_name)
    logger.addHandler(handler)
    return logger
