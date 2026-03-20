import logging
from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces.abstract_db_repository import IDBepository
from src.site.model import Site

logger = logging.getLogger(__name__)


class SQLAlchemySiteRepository(IDBepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, url: str, hash: str) -> Site:
        async with self._handle_db_error(operation="Create", url=url, hash=hash):
            site_to_add = Site(url=url, hash=hash)
            self.session.add(site_to_add)
            await self.session.flush()
            return site_to_add

    async def get_by_id(self, id: int) -> Site | None:
        async with self._handle_db_error(operation="Get by id", id=id):
            stmt = select(Site).where(Site.id == id)
            result = await self.session.execute(stmt)
            site = result.scalar_one_or_none()
            return site

    async def get_by_url(self, url: str) -> Site | None:
        async with self._handle_db_error(operation="Get by url", url=url):
            stmt = select(Site).where(Site.url == url)
            result = await self.session.execute(stmt)
            site = result.scalar_one_or_none()
            return site

    async def update(self, url: str, hash_to_update: str) -> Site | None:
        async with self._handle_db_error(
            operation="Update", url=url, hash_to_update=hash_to_update
        ):
            site = await self.get_by_url(url)
            if site:
                site.hash = hash_to_update
                self.session.add(site)
                await self.session.flush()
                return site

    async def delete(self, url: str, hash_to_update: str) -> bool:
        async with self._handle_db_error(
            operation="Update", url=url, hash_to_update=hash_to_update
        ):
            site = await self.get_by_url(url)
            if site:
                await self.session.delete(site)
                return True
            return False

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
