"""
FastAPI dependencies for database session handling.
"""

from collections.abc import AsyncGenerator

from fastapi import HTTPException, status
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.infrastructure.session import AsyncSessionLocal


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting a database session.

    Creates and yields an async SQLAlchemy session, ensuring proper cleanup.
    """
    session: AsyncSession = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except OperationalError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error",
        ) from e
    finally:
        await session.close()
