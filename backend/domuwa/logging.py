import logging

import colorlog

# logging.getLogger("multipart.multipart").setLevel(logging.INFO)
logging.getLogger("asyncio").setLevel(logging.INFO)


def get_logger(logger_name: str) -> logging.Logger:
    logger_fmt = (
        "%(log_color)s%(asctime)s [%(name)s:%(levelname)s] %(funcName)s() %(message)s"
    )
    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(logger_fmt, log_colors=log_colors))
    logger = colorlog.getLogger(logger_name)
    logger.addHandler(handler)
    return logger
