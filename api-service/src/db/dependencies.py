"""
FastAPI dependencies for database session handling.
"""

from collections.abc import AsyncGenerator
from logging import getLogger

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.db.infrastructure.session import AsyncSessionMaker

logger = getLogger(__name__)


async def get_session_factory() -> AsyncGenerator[async_sessionmaker[AsyncSession]]:
    """
    Dependency for getting a database session maker.
    """
    try:
        yield AsyncSessionMaker
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise e
