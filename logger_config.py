import os

from aiologger import Logger
from aiologger.levels import LogLevel
from aiologger.handlers.files import AsyncTimedRotatingFileHandler
from aiologger.formatters.base import Formatter


def setup_logger(name, level=LogLevel.INFO):
    log_path = os.path.join('logs', 'logs.log')
    formatter = Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = Logger.with_default_handlers(
        name=name,
        level=level
    )
    handler = AsyncTimedRotatingFileHandler(
        filename=log_path,
        when='W6',
        backup_count=5,
        encoding='utf-8'
    )
    handler.formatter = formatter
    logger.add_handler(handler)
    return logger
