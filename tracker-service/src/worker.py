import asyncio
from logging import getLogger

from src.db.infrastructure.session import AsyncSessionLocal
from src.site.repository import SQLAlchemySiteRepository
from src.site.service import SiteService
from src.tracker.adapters.cleaners.beautifulsoup_cleaner import BaseCleaner
from src.tracker.adapters.hashers.sha256_hasher import BaseHasher
from src.tracker.adapters.http_clients.httpx_client import BaseClient
from src.tracker.tracker import Tracker

logger = getLogger(__name__)


async def create_tracker() -> Tracker:
    """
    Factory function to create a configured Tracker instance.

    Initializes all dependencies (repository, service, adapters)
    and returns a ready-to-use Tracker.

    Returns:
        A Tracker instance with all injected dependencies.

    Example:
        >>> tracker = await create_tracker()
        >>> await tracker.start_track("https://example.com")
    """
    repo = SQLAlchemySiteRepository(AsyncSessionLocal)
    return Tracker(
        site_service=SiteService(repo=repo),
        cleaner=BaseCleaner(),
        hasher=BaseHasher(),
        client=BaseClient(),
    )


async def check_demon(tracker: Tracker, check_interval: int = 5) -> None:
    """
    Demon that periodically checks all tracked sites for changes.

    Runs an infinite loop that checks all sites for content changes
    and initiates notification sending when changes are detected.

    Args:
        tracker: Tracker instance for checking sites.
        check_interval: Interval between checks in seconds.

    Example:
        >>> tracker = await create_tracker()
        >>> await check_demon(tracker, check_interval=10)
    """
    while True:
        if updated_sites := await tracker.check_all_sites():
            # отправляем в очередь сообщение о том, какие сайты обновились
            ...
        await asyncio.sleep(check_interval)


async def main() -> None:
    """
    Application entry point.

    Creates the Tracker and starts the site monitoring demon.
    """
    tracker = await create_tracker()
    logger.info("Tracker initialized, starting monitoring demon")
    await check_demon(tracker)
