'''
This module contains the LogLevel class which is an Enum class to represent the log levels.
'''
import logging
from enum import Enum

class LogLevel(Enum):
    '''
    Enum class to represent the log levels
    '''
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
