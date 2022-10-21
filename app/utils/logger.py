import logging
from logging.config import dictConfig

from app.config import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger('hataraki-backend')


def get_logger():
    """
    Get logger instance for dependency injection
    """
    return logger
