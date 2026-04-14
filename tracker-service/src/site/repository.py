import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.interfaces.db_interface import IDBRepository
from src.site.model import Site

logger = logging.getLogger(__name__)


class SQLAlchemySiteRepository(IDBRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    @asynccontextmanager
    async def _get_session(self):
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def create(self, url: str, hash: str) -> Site:
        async with self._handle_db_error(
            operation="Create", url=url, hash=hash
        ), self._get_session() as session:
            site_to_add = Site(url=url, hash=hash)
            session.add(site_to_add)
            await session.flush()
            return site_to_add

    async def get_by_id(self, id: int) -> Site | None:
        async with self._handle_db_error(
            operation="Get by id", id=id
        ), self._get_session() as session:
            stmt = select(Site).where(Site.id == id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_by_url(self, url: str) -> Site | None:
        async with self._handle_db_error(
            operation="Get by url", url=url
        ), self._get_session() as session:
            stmt = select(Site).where(Site.url == url)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def update(self, url: str, hash_to_update: str) -> Site | None:
        async with self._handle_db_error(
            operation="Update", url=url, hash_to_update=hash_to_update
        ), self._get_session() as session:
            stmt = select(Site).where(Site.url == url)
            result = await session.execute(stmt)
            site = result.scalar_one_or_none()
            if site:
                site.hash = hash_to_update
                session.add(site)
                await session.refresh(site, attribute_names=["updated_at"])
                return site
            return None

    async def delete(self, url: str) -> bool:
        async with self._get_session() as session:
            stmt = select(Site).where(Site.url == url)
            result = await session.execute(stmt)
            site = result.scalar_one_or_none()
            if site:
                await session.delete(site)
                return True
            return False

    async def get_sites_stream(
        self, batch_size: int = 100
    ) -> AsyncGenerator[Site, None]:
        async with self.session_factory() as session:
            stmt = select(Site).order_by(Site.id)
            stream = await session.stream(
                stmt, execution_options={"yield_per": batch_size}
            )
            async for row in stream:
                yield row.Site

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
