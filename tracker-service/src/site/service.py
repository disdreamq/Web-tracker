from logging import getLogger

import validators

from src.core.deco_for_SQLAlchemy_exc import handle_service_exceptions
from src.core.exceptions import UniqueURLError
from src.interfaces.abstract_db_repository import IDBepository
from src.site.schemas import SSiteCreate, SSiteDTO

logger = getLogger(__name__)


class SiteService:

    def __init__(self, repo: IDBepository):
        self.repo = repo

    @handle_service_exceptions
    async def create(self, site: SSiteCreate) -> SSiteDTO:
        if not validators.url(SSiteCreate.url):
            raise ValueError

        if self.repo.get_by_url(site.url):
            raise UniqueURLError(
                f"Cannot add site to database, site already exists: {site.url=}"
            )

        site_in_db = await self.repo.create(url=site.url, hash=site.hash)
        return SSiteDTO.model_validate(site_in_db)

    @handle_service_exceptions
    async def get_by_url(self, url: str) -> SSiteDTO | None:
        if site := await self.repo.get_by_url(url):
            return SSiteDTO.model_validate(site)
        return

    @handle_service_exceptions
    async def get_by_id(self, id: int) -> SSiteDTO | None:
        if site := await self.repo.get_by_id(id):
            return SSiteDTO.model_validate(site)
        return

    @handle_service_exceptions
    async def update(self, url, hash_to_update) -> SSiteDTO | None:
        if site := await self.repo.update(url, hash_to_update):
            return SSiteDTO.model_validate(site)
        return

    @handle_service_exceptions
    async def delete(self, url) -> bool:
        return await self.repo.delete(url)
