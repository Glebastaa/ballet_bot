import os
import logging

from logging.handlers import RotatingFileHandler


def setup_logger(name, log_file, level=logging.INFO):
    # Path for logs.
    logs_dir = os.path.join('logs', *os.path.split(log_file)[:-1])
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join('logs', log_file)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
    )
    handler = RotatingFileHandler(log_path, maxBytes=10000000, backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
