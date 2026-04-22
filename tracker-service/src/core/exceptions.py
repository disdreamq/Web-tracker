class BaseAppException(Exception):
    """Base exception for application errors."""

    def __init__(self, message: str):
        """
        Initialize base exception.

        Args:
            message: Exception message.
        """
        self.message = message


class PageFetchError(BaseAppException):
    """Exception raised when page fetching fails."""

    def __init__(self, message: str, status_code: int):
        """
        Initialize page fetch error.

        Args:
            message: Error message.
            status_code: HTTP status code that caused the error.
        """
        super().__init__(message=message)
        self.status_code = status_code


class PageTimeoutError(BaseException):
    """Exception raised when page request times out."""

    pass


class PageConnectionError(BaseException):
    """Exception raised when page connection fails."""

    pass


class ValidationException(BaseException):
    """Exception raised for validation errors."""

    pass


class DataBaseException(BaseException):
    """Exception raised for database errors."""

    pass


class PageInvalidURLError(BaseException):
    """Exception raised for invalid URL errors."""

    pass


class UniqueURLError(BaseException):
    """Exception raised when unique constraint is violated."""

    pass


class NotFoundException(BaseException):
    """Exception raised when requested resource is not found."""

    pass


class BadDataException(BaseException):
    """Exception raised for invalid or bad data."""

    pass


class TemporaryFailException(BaseException):
    """Exception raised for temporary failures (retryable)."""

    pass


class UnexpectedException(BaseException):
    """Exception raised for unexpected errors."""

    pass
