from collections.abc import AsyncGenerator
from logging import getLogger

from src.core.deco_for_SQLAlchemy_exc import handle_service_exceptions
from src.core.exceptions import UniqueURLError
from src.interfaces.db_interface import IDBRepository
from src.interfaces.site_service_interface import ISiteService
from src.site.schemas import SSiteCreate, SSiteDTO

logger = getLogger(__name__)


class SiteService(ISiteService):

    def __init__(self, repo: IDBRepository):
        self.repo = repo

    @handle_service_exceptions
    async def create(self, site_to_create: SSiteCreate) -> SSiteDTO:

        if await self.repo.get_by_url(str(site_to_create.url)):
            logger.exception(
                f"Unique url exception during create site, url already exists: url= {site_to_create.url}"
            )
            raise UniqueURLError(
                f"Cannot add site to database, site already exists: {site_to_create.url=}"
            )

        site_in_db = await self.repo.create(
            url=str(site_to_create.url), hash=str(site_to_create.hash)
        )
        logger.info(
            f"Added site to database: url = {site_to_create.url}, hash = {site_to_create.hash}"
        )
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
            logger.info(
                f"Updated site to database: url = {site.url}, hash = {site.hash}"
            )
            return SSiteDTO.model_validate(site)
        return

    async def get_sites_stream(self) -> AsyncGenerator:
        stream = self.repo.get_sites_stream()
        async for site in stream:  # type: ignore #
            url = site.url
            hash = site.hash
            yield (url, hash)

    @handle_service_exceptions
    async def delete(self, url) -> bool:
        logger.info(f"Deleted site from database: {url=}")
        return await self.repo.delete(url)
