from logging import getLogger

import validators

from src.core.deco_for_SQLAlchemy_exc import handle_service_exceptions
from src.core.exceptions import UniqueURLError
from src.interfaces.abstract_db_repository import IDBepository
from src.site.DTO import SiteDTO

logger = getLogger(__name__)


class SiteService:

    def __init__(self, repo: IDBepository):
        self.repo = repo

    @handle_service_exceptions
    async def create(self, url: str, hash: str) -> SiteDTO:
        if not validators.url(url):
            raise ValueError

        if self.repo.get_by_url(url):
            raise UniqueURLError(
                f"Cannot add site to database, site already exists: {url=}"
            )

        site_in_db = await self.repo.create(url=url, hash=hash)
        return SiteDTO(
            id=site_in_db.id,
            url=site_in_db.url,
            hash=site_in_db.hash,
            created_at=site_in_db.created_at,
            updated_at=site_in_db.updated_at,
        )

    @handle_service_exceptions
    async def get_by_url(self, url: str) -> SiteDTO | None:
        if site := await self.repo.get_by_url(url):
            return SiteDTO(
                id=site.id,
                url=site.url,
                hash=site.hash,
                created_at=site.created_at,
                updated_at=site.updated_at,
            )
        return

    @handle_service_exceptions
    async def get_by_id(self, id: int) -> SiteDTO | None:
        if site := await self.repo.get_by_id(id):
            return SiteDTO(
                id=site.id,
                url=site.url,
                hash=site.hash,
                created_at=site.created_at,
                updated_at=site.updated_at,
            )
        return

    @handle_service_exceptions
    async def update(self, url, hash_to_update) -> SiteDTO | None:
        if site := await self.repo.update(url, hash_to_update):
            return SiteDTO(
                id=site.id,
                url=site.url,
                hash=site.hash,
                created_at=site.created_at,
                updated_at=site.updated_at,
            )
        return

    @handle_service_exceptions
    async def delete(self, url) -> bool:
        return await self.repo.delete(url)
