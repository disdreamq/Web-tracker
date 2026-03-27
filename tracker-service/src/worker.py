import asyncio
from logging import getLogger

from src.db.infrastructure.session import get_session
from src.site.repository import SQLAlchemySiteRepository
from src.site.service import SiteService
from src.tracker.adapters.cleaners.beautifulsoup_cleaner import BaseCleaner
from src.tracker.adapters.hashers.sha256_hasher import BaseHasher
from src.tracker.adapters.http_clients.httpx_client import BaseClient
from src.tracker.tracker import Tracker

logger = getLogger(__name__)
tracker = None


async def prepare():
    try:
        global tracker
        repo = SQLAlchemySiteRepository(get_session())
        service = SiteService(repo=repo)
        tracker = Tracker(
            site_service=service,
            cleaner=BaseCleaner(),
            hasher=BaseHasher(),
            client=BaseClient(),
        )
        logger.info("Created tracker")

    except Exception as e:
        logger.exception(f"Cannot start application during to exception: {e}")


async def cheking_demon():
    while True:
        if not tracker:
            logger.exception("Tracker not initialized")
            raise
        if updated_sites := await tracker.check_all_sites():
            ...  # отправка уведомлений в бота о том, что обновились сайты
        await asyncio.sleep(3600)


async def main():
    await prepare()
    await cheking_demon()
