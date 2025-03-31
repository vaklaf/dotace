
'''This module contains the CLogger class which is used to log data to a file.'''
import logging

from pathlib import Path
from logging import Logger

#from .custom_handlers import FileHandlerWithHeader
#from .custom_formatters import OnScreenLoggerFormater

class CLogger:
    '''Class for logging data to a file'''

    log_root: str | None = None
    
    def __init__(self,logath:str,output_suffix:str,on_screen:bool = True):
        self._log_file_suffix = output_suffix
        self._on_screen = on_screen
        self.logging_strategies = {
            logging.DEBUG: self._write_debug,
            logging.INFO: self._write_info,
            logging.WARNING: self._write_warning,
            logging.ERROR: self._write_error,
            logging.CRITICAL: self._write_crtical
        }
        self._init_logger()
           
    def _write_debug(self, logger: Logger, message: str):
        logger.debug(message)

    def _write_info(self, logger: Logger, message: str):
        logger.info(message)

    def _write_warning(self, logger: Logger, message: str):
        logger.warning(message)

    def _write_error(self, logger: Logger, message: str):
        logger.error(message)

    def _write_crtical(self, logger: Logger, message: str):
        logger.critical(message)

    def write(self, message: str, level: int = logging.INFO) -> None:
        """This method wrpas all standard logging methods to wirte
        log messages. According the argument level, default value is
        logging.INFO, chooses an apropriate method from the logging_strategies
        dictionary.

        Args:
            message (Message): An instance of the Message class to log.
            level (int, optional): The logging level. Defaults to logging.INFO.
        """
        self.logging_strategies[level](
            self._logger, f'{message}')

    def _init_logger(self):
        self._logger = logging.getLogger(self._name)
        self._logger.propagate = True
        self._logger.setLevel(logging.DEBUG)

        if not self._logger.hasHandlers():
            # File Handler
            file_handler = FileHandlerWithHeader(
                self._logfile
            )
            file_handler.setLevel(logging.DEBUG)

            # Setting File Formatter
            fformatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(fformatter)
            self._logger.addHandler(file_handler)

            if self._on_screen is True:
                # Standard StreamHandler
                sth = logging.StreamHandler()
                sth.setLevel(logging.INFO)
                # Setting Stream Formatter
                sth.setFormatter(OnScreenLoggerFormater())
                self._logger.addHandler(sth)
