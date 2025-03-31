'''This module is responsible for the logging configuration and the log function'''
import logging.handlers
import os
import logging

from  pathlib import Path


from .loglevel import LogLevel
from .custom_formatters import OnScreenLoggerFormater
from .custom_message import CustomMessage


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def setup_logger(path:str, timestamp:str):
    '''Setup the logging configuration'''

    log_dir = Path().cwd() / path
    os.makedirs(log_dir, exist_ok=True)

    app_log_path = log_dir / f'app_{timestamp}.log'
    error_log_path = log_dir / f'error_{timestamp}.log'

    basicFileHandler:logging.Handler = logging.FileHandler(app_log_path)
    basicFileHandler.setLevel(logging.DEBUG)
    errorFileHadler:logging.Handler = logging.FileHandler(error_log_path)
    errorFileHadler.setLevel(logging.ERROR)
    consoleHandler:logging.Handler = logging.StreamHandler()
    consoleHandler.setFormatter(OnScreenLoggerFormater())
    consoleHandler.setLevel(logging.DEBUG)

    try:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                basicFileHandler,
                errorFileHadler,
                consoleHandler
            ],
            
        )
        
    except OSError as e:
        print(f"Chyba při nastavení logování: {e}")
        return None

# create a dictionary with the strategies to log by level
logger_strategies = {
     LogLevel.DEBUG: logger.debug,
     LogLevel.INFO: logger.info,
     LogLevel.WARNING: logger.warning,
     LogLevel.ERROR: logger.error,
     LogLevel.CRITICAL: logger.critical
}

def log(level:LogLevel, message:CustomMessage):
    '''Log a message with the level passed as parameter'''
    logger_strategies[level](message)
