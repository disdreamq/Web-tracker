class BaseAppException(Exception):
    """Base exception for application errors."""

    def __init__(self, message: str):
        """
        Initialize base exception.

        Args:
            message: Exception message.
        """
        self.message = message


class DataBaseException(BaseAppException):
    """Exception raised for database errors."""

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


class RabbitMQConnectionError(BaseAppException):
    """Exception raised when RabbitMQ connection fails."""

    pass


class RabbitMQMessageError(BaseAppException):
    """Exception raised when RabbitMQ message processing fails."""

    pass


class UnexpectedException(BaseAppException):
    """Exception raised for unexpected errors."""

    pass
