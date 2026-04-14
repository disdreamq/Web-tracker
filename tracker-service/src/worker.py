import asyncio
from logging import getLogger

from src.db.infrastructure.session import AsyncSessionLocal
from src.interfaces.tracker_interface import ITracker
from src.site.repository import SQLAlchemySiteRepository
from src.site.service import SiteService
from src.tracker.adapters.cleaners.beautifulsoup_cleaner import BaseCleaner
from src.tracker.adapters.hashers.sha256_hasher import BaseHasher
from src.tracker.adapters.http_clients.httpx_client import BaseClient
from src.tracker.tracker import Tracker

logger = getLogger(__name__)
_tracker = None


async def prepare(current_tracker: ITracker):
    try:
        global _tracker
        _tracker = current_tracker
        logger.info("Created tracker")

    except Exception as e:
        logger.exception(f"Cannot start application during to exception: {e}")


async def cheking_demon():
    while True:
        if not _tracker:
            logger.exception("Tracker not initialized")
            raise
        if updated_sites := await _tracker.check_all_sites():
            ...  # отправляем в очередь сообщение о том, какие сайты обновились
        await asyncio.sleep(5)


async def main():
    repo = SQLAlchemySiteRepository(AsyncSessionLocal)
    await prepare(
        Tracker(
            site_service=SiteService(repo=repo),
            cleaner=BaseCleaner(),
            hasher=BaseHasher(),
            client=BaseClient(),
        )
    )
    await cheking_demon()
