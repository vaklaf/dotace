import logging

from pathlib import Path


from .log_parts import  log_header

# https://stackoverflow.com/questions/33468174/write-header-to-a-python-log-file-but-only-if-a-record-gets-written
# Create a class that extends the FileHandler class from logging.FileHandler
class FileHandlerWithHeader(logging.FileHandler):

    def __init__(self, filename: str, mode: str = 'a', encoding: str | None = 'utf-8', delay: bool = False, errors: str | None = None) -> None:

        # Determine if the file pre-exists
        self.file_pre_exists = Path(filename).is_file()

        # Call the parent __init__
        super().__init__(filename, mode, encoding, delay, errors)

        # Write the header if delay is False and a file stream was created.
        if not delay and self.stream is not None:
            self.stream.write(log_header())

    def emit(self, record):
        # Create the file stream if not already created.
        if self.stream is None:
            self.stream = self._open()

            # If the file pre_exists, it should already have a header.
            # Else write the header to the file so that it is the first line.
            if not self.file_pre_exists:
                self.stream.write(log_header())

        # Call the parent class emit function.
        logging.FileHandler.emit(self, record)