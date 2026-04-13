from logging import getLogger

from pydantic import HttpUrl

from src.core.exceptions import (
    BadDataException,
    PageFetchError,
    TemporaryFailException,
    UnexpectedException,
)
from src.interfaces.cleaner_interface import ICleanerRepository
from src.interfaces.hasher_interface import IHasherRepository
from src.interfaces.http_client_interface import IHTTPClientRepository
from src.interfaces.site_service_interface import ISiteService
from src.interfaces.tracker_interface import ITracker
from src.site.schemas import SSiteCreate

logger = getLogger(__name__)


class Tracker(ITracker):
    def __init__(
        self,
        site_service: ISiteService,
        cleaner: ICleanerRepository,
        hasher: IHasherRepository,
        client: IHTTPClientRepository,
    ):
        self.site_service = site_service
        self.cleaner = cleaner
        self.hasher = hasher
        self.client = client

    async def get_hash(self, url: str) -> str:
        try:
            response = await self.client.get(url)
        except PageFetchError as e:
            if str(e.status_code).startswith("4"):
                logger.exception(
                    f"Bad data exception during getting page for hash: {e}"
                )
                raise BadDataException(
                    f"Cannot get acces to the page, response.status_code = {e.status_code}"
                ) from None
            if str(e.status_code).startswith("5"):
                logger.exception(
                    f"Temporary exception during getting page for hash: {e}"
                )
                raise TemporaryFailException(
                    f"Can not get page, response.status_code = {e.status_code}"
                ) from None
        except Exception as e:
            logger.exception(f"Unexpected exception during getting page for hash: {e}")
            raise UnexpectedException(
                "Unexpected exception duiring getting page for hash."
            ) from e

        html_page = response.text
        clear_content = self.cleaner.clear_html(html_page)
        hash = self.hasher.calculate_hash(clear_content)

        return hash

    async def start_track(self, url: str) -> None:
        hash = await self.get_hash(url)
        site_to_create = SSiteCreate(url=HttpUrl(url), hash=hash)
        logger.info(f"Started tracking site {url=}")
        await self.site_service.create(site_to_create)

    async def stop_track(self, url: str) -> None:
        logger.info(f"Stopped tracking site {url}")
        await self.site_service.delete(url=url)

    async def check_all_sites(self) -> list[str] | None:
        stream = self.site_service.get_sites_stream()
        if not stream:
            return
        updated_sites = []
        async for url, hash in stream:  # type: ignore
            new_hash = await self.get_hash(url)
            if new_hash != hash:
                await self.site_service.update(url, new_hash)
                updated_sites.append(url)

        return updated_sites
