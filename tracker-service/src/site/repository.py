import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces.abstract_db_repository import IDBRepository
from src.site.model import Site

logger = logging.getLogger(__name__)


class SQLAlchemySiteRepository(IDBRepository):
    def __init__(self, session: AsyncGenerator[AsyncSession]):
        self.session = session

    async def create(self, url: str, hash: str) -> Site:
        async with self._handle_db_error(
            operation="Create", url=url, hash=hash
        ), self.get_session() as session:
            site_to_add = Site(url=url, hash=hash)
            session.add(site_to_add)
            await session.flush()
            return site_to_add

    async def get_by_id(self, id: int) -> Site | None:
        async with self._handle_db_error(
            operation="Create", id=id
        ), self.get_session() as session:
            stmt = select(Site).where(Site.id == id)
            result = await session.execute(stmt)
            site = result.scalar_one_or_none()
            return site

    async def get_by_url(self, url: str) -> Site | None:
        async with self._handle_db_error(
            operation="Get by url", url=url
        ), self.get_session() as session:
            stmt = select(Site).where(Site.url == url)
            result = await session.execute(stmt)
            site = result.scalar_one_or_none()
            return site

    async def update(self, url: str, hash_to_update: str) -> Site | None:
        async with self._handle_db_error(
            operation="Update", url=url, hash_to_update=hash_to_update
        ), self.get_session() as session:
            site = await self.get_by_url(url)
            if site:
                site.hash = hash_to_update
                session.add(site)
                await session.flush()
                return site

    async def delete(self, url: str, hash_to_update: str) -> bool:
        async with self._handle_db_error(
            operation="Update", url=url, hash_to_update=hash_to_update
        ), self.get_session() as session:
            site = await self.get_by_url(url)
            if site:
                await session.delete(site)
                return True
            return False

    async def get_sites_stream(self, batch_size: int = 100) -> AsyncGenerator:
        async with self.get_session() as session:
            stmt = select(Site).order_by(Site.id)
            stream = await session.stream(
                stmt, execution_options={"yield_per": batch_size}
            )
            async for row in stream:
                yield row.Site

    @asynccontextmanager
    async def get_session(
        self,
    ):
        async for session in self.session:
            yield session

    @asynccontextmanager
    async def _handle_db_error(self, operation: str, **context):
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
