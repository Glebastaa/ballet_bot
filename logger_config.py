import os
import logging
import atexit

from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
from multiprocessing import Queue


def setup_logger(name, level=logging.INFO):
    log_path = os.path.join('logs', 'logs.log')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(
        name=name
    )
    handler = RotatingFileHandler(
        log_path,
        maxBytes=10000000,
        backupCount=5,
        encoding='utf-8'
    )
    handler.setFormatter(formatter)

    que = Queue()
    logger.addHandler(QueueHandler(que))
    logger.setLevel(level)

    listener = QueueListener(que, handler)
    listener.start()

    # for correct stop listener.
    atexit.register(listener.stop)

    return logger
