from logging import getLogger

from pydantic import HttpUrl
from tenacity import RetryError

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
    """
    Main class for tracking website content changes.

    Implements the Tracker pattern for monitoring website content:
    - Loading pages via HTTP client
    - Cleaning HTML from scripts, styles and other irrelevant content
    - Computing hash to detect changes
    - Synchronization with the database

    Attributes:
        site_service: Service for site CRUD operations.
        cleaner: Adapter for cleaning HTML content.
        hasher: Adapter for computing content hashes.
        client: HTTP client for fetching pages.

    Example:
        >>> tracker = Tracker(site_service, cleaner, hasher, client)
        >>> await tracker.start_track("https://example.com")
        >>> updated = await tracker.check_all_sites()
    """

    def __init__(
        self,
        site_service: ISiteService,
        cleaner: ICleanerRepository,
        hasher: IHasherRepository,
        client: IHTTPClientRepository,
    ) -> None:
        """
        Initialize Tracker with injected dependencies.

        Args:
            site_service: Service for site database operations.
            cleaner: Adapter for cleaning HTML pages.
            hasher: Adapter for computing content hashes.
            client: HTTP client for fetching web pages.
        """
        self.site_service = site_service
        self.cleaner = cleaner
        self.hasher = hasher
        self.client = client

    async def get_hash(self, url: str) -> str:
        """
        Compute the hash of a web page content.

        Fetches the page, cleans HTML from scripts, styles and other
        irrelevant elements, then computes the hash of the cleaned content.

        Args:
            url: URL of the page to compute hash for.

        Returns:
            Computed hash of the page content.

        Raises:
            BadDataException: If page is unavailable (4xx status).
            TemporaryFailException: If temporary server error (5xx status).
            UnexpectedException: If an unexpected error occurs.

        Example:
            >>> hash = await tracker.get_hash("https://example.com")
            >>> print(hash)
            "a1b2c3d4..."
        """
        try:
            response = await self.client.get(url)
            html_page = response.text
            clear_content = self.cleaner.clear_html(html_page)
            hash = self.hasher.calculate_hash(clear_content)

            return hash
        except PageFetchError as e:
            if str(e.status_code).startswith("4"):
                logger.exception(
                    "Bad data exception during getting page for hash: %s", e
                )
                raise BadDataException(
                    f"Cannot get acces to the page, response.status_code = {e.status_code}"  # noqa: E501
                ) from None
            elif str(e.status_code).startswith("5"):
                logger.exception(
                    "Temporary exception during getting page for hash: %s", e
                )
                raise TemporaryFailException(
                    f"Can not get page, response.status_code = {e.status_code}"
                ) from None
            else:
                logger.exception("Page fetch error during getting page for hash: %s", e)
                raise UnexpectedException(
                    f"Unexpected status code {e.status_code} when fetching page"
                ) from e
        except RetryError as e:
            logger.info("Retry error during getting page for hash: %s", e)
            raise TemporaryFailException(
                f"Failed to fetch page after retries: {url}"
            ) from e
        except Exception as e:
            logger.exception(f"Unexpected exception during getting page for hash: {e}")
            raise UnexpectedException(
                "Unexpected exception duiring getting page for hash."
            ) from e

    async def start_track(self, url: str) -> None:
        """
        Start tracking a new website.

        Computes the initial hash of the page and saves the site to the database.

        Args:
            url: URL of the site to track.

        Raises:
            UniqueURLError: If the site is already being tracked.

        Example:
            >>> await tracker.start_track("https://example.com")
        """
        hash = await self.get_hash(url)
        site_to_create = SSiteCreate(url=HttpUrl(url), hash=hash)
        logger.info(f"Started tracking site {url=}")
        await self.site_service.create(site_to_create)

    async def stop_track(self, url: str) -> None:
        """
        Stop tracking a website.

        Removes the site from the database.

        Args:
            url: URL of the site to stop tracking.

        Example:
            >>> await tracker.stop_track("https://example.com")
        """
        logger.info(f"Stopped tracking site {url}")
        await self.site_service.delete(url=url)

    async def check_all_sites(self) -> list[str] | None:
        """
        Check all tracked sites for content changes.

        Compares the current hash of each page with the one stored in the database.
        Updates the hash in the database when changes are detected.

        Returns:
            List of URLs with changes, or None if no sites are tracked.

        Example:
            >>> updated = await tracker.check_all_sites()
            >>> if updated:
            ...     send_notification(updated)
        """
        stream = self.site_service.get_sites_stream()
        if not stream:
            return
        updated_sites = []
        async for url, hash in stream:  # type: ignore
            try:
                new_hash = await self.get_hash(url)
                if new_hash != hash:
                    await self.site_service.update(url, new_hash)
                    updated_sites.append(url)
            except RetryError as e:
                logger.info(f"Failed to get site content, site url = {url}: {e}")
            except Exception as e:
                logger.error(f"Failed to update site {url}: {e}")

        return updated_sites
