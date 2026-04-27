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


class PageTimeoutError(BaseAppException):
    """Exception raised when page request times out."""

    pass


class PageConnectionError(BaseAppException):
    """Exception raised when page connection fails."""

    pass


class ValidationException(BaseAppException):
    """Exception raised for validation errors."""

    pass


class DataBaseException(BaseAppException):
    """Exception raised for database errors."""

    pass


class PageInvalidURLError(BaseAppException):
    """Exception raised for invalid URL errors."""

    pass


class UniqueURLError(BaseAppException):
    """Exception raised when unique constraint is violated."""

    pass


class NotFoundException(BaseAppException):
    """Exception raised when requested resource is not found."""

    pass


class BadDataException(BaseAppException):
    """Exception raised for invalid or bad data."""

    pass


class TemporaryFailException(BaseAppException):
    """Exception raised for temporary failures (retryable)."""

    pass


class UnexpectedException(BaseAppException):
    """Exception raised for unexpected errors."""

    pass


class RabbitMQConnectionError(BaseAppException):
    """Exception raised when RabbitMQ connection fails."""

    pass


class RabbitMQMessageError(BaseAppException):
    """Exception raised when RabbitMQ message processing fails."""

    pass
