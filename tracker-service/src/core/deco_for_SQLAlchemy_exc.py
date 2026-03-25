import logging

from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError

from src.core.exceptions import (
    DataBaseException,
    ValidationException,
)

logger = logging.getLogger(__name__)


def handle_service_exceptions(func):
    """Deco for db service with exceptions handling."""

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

    return wrapper
