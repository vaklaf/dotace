class FileDownloadError(Exception):
    """Base class for processing exceptions during downloading."""
    pass

class FileExistsAlready(FileDownloadError):
    """Exception raised when target file already exists."""
    pass

class DownloadingFailure(FileDownloadError):
    """Exception raised when downloading failures."""
    pass

class FolderCannotBeCreated(FileDownloadError):
    """Exception when creation of target folder is not possible."""
    pass