import logging
from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces.db_interface import IDBRepository
from src.user.model import User

logger = logging.getLogger(__name__)


class SQLAlchemyUserRepository(IDBRepository):
    """
    Repository for working with users via SQLAlchemy.

    Implements CRUD operations using async SQLAlchemy
    with error handling. Sessions are passed from outside.
    """

    async def create(
        self,
        session: AsyncSession,
        email: str,
        password: str,
        tracking_sites: list[str] | None = None,
    ) -> User:
        """
        Create a new user record in the database.

        Args:
            session: Async SQLAlchemy session.
            email: User email.
            password: User password hash.
            tracking_sites: List of tracked site URLs.

        Returns:
            Created User model.
        """
        async with self._handle_db_error(operation="Create", email=email):
            user_to_add = User(
                email=email,
                password=password,
                tracking_sites=str(tracking_sites) if tracking_sites else "[]",
            )
            session.add(user_to_add)
            await session.flush()
            return user_to_add

    async def get_by_id(self, session: AsyncSession, id: int) -> User | None:
        """
        Get a user by ID.

        Args:
            session: Async SQLAlchemy session.
            id: User ID.

        Returns:
            User model or None.
        """
        async with self._handle_db_error(operation="Get by id", id=id):
            stmt = select(User).where(User.id == id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_by_email(self, session: AsyncSession, email: str) -> User | None:
        """
        Get a user by email.

        Args:
            session: Async SQLAlchemy session.
            email: User email.

        Returns:
            User model or None.
        """
        async with self._handle_db_error(operation="Get by email", email=email):
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def update(self, session: AsyncSession, id: int, **kwargs) -> User | None:
        """
        Update user fields.

        Args:
            session: Async SQLAlchemy session.
            id: User ID.
            **kwargs: Fields to update.

        Returns:
            Updated User model or None.
        """
        async with self._handle_db_error(operation="Update", id=id, **kwargs):
            stmt = select(User).where(User.id == id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                session.add(user)
                await session.refresh(user, attribute_names=["updated_at"])
                return user
            return None

    async def delete(self, session: AsyncSession, id: int) -> bool:
        """
        Delete a user by ID.

        Args:
            session: Async SQLAlchemy session.
            id: User ID.

        Returns:
            True if deleted, False if not found.
        """
        async with self._handle_db_error(operation="Delete", id=id):
            stmt = select(User).where(User.id == id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                await session.delete(user)
                return True
            return False

    @asynccontextmanager
    async def _handle_db_error(self, operation: str, **context):
        """
        Context manager for handling database errors.

        Logs IntegrityError, SQLAlchemyError and general exceptions
        with additional operation context.

        Args:
            operation: Type of operation (Create, Get, Update, Delete).
            **context: Additional data for logging.
        """
        try:
            yield
        except IntegrityError as e:
            logger.exception(
                f"Integrity error during {operation}",
                extra={**context, "error": str(e)},
            )
            raise

        except SQLAlchemyError as e:
            logger.exception(
                f"Database error during {operation}",
                extra={**context, "error": str(e)},
            )
            raise

        except Exception as e:
            logger.exception(
                f"Unexpected error during {operation}",
                extra={**context, "error": str(e)},
            )
            raise
