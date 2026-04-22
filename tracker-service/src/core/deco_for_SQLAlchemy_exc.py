import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.core.exceptions import (
    DataBaseException,
    UnexpectedException,
    ValidationException,
)

logger = logging.getLogger(__name__)


def handle_service_exceptions(func):
    """
    Decorator for service methods with database exception handling.

    Catches SQLAlchemy exceptions and converts them to application-specific
    exceptions with proper logging.

    Args:
        func: Async service method to wrap.

    Returns:
        Wrapped async function with exception handling.

    Raises:
        ValidationException: On integrity constraint violations.
        DataBaseException: On general database errors.
        UnexpectedException: On any other unexpected errors.

    Example:
        >>> class MyService:
        ...     @handle_service_exceptions
        ...     async def create(self, data):
        ...         await repo.create(data)
    """

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except IntegrityError as e:
            logger.exception(f"Business logic violation: {e}")
            raise ValidationException("Data constraint violation") from e

        except SQLAlchemyError as e:
            logger.exception(f"Database error in service: {e}")
            raise DataBaseException("Data base exception") from e

        except Exception as e:
            logger.exception(f"Unexpected exception: {e}")
            raise UnexpectedException("Unexpected error occurred") from e

    return wrapper
