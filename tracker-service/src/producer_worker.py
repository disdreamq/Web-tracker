import asyncio
from logging import getLogger

from src.db.infrastructure.session import AsyncSessionLocal
from src.rabbitmq.rabbitmq_publisher import RabbitMQProducer
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


def create_producer() -> RabbitMQProducer:
    """
    Factory function to create a RabbitMQ producer.

    Returns:
        A configured RabbitMQProducer instance.

    Example:
        >>> producer = create_producer()
        >>> await producer.publish("exchange", "key", {"data": "value"})
    """
    return RabbitMQProducer()


async def check_demon(
    tracker: Tracker,
    producer: RabbitMQProducer,
    check_interval: int = 5,
) -> None:
    """
    Demon that periodically checks all tracked sites for changes.

    Runs an infinite loop that checks all sites for content changes
    and sends notifications via RabbitMQ when changes are detected.

    Args:
        tracker: Tracker instance for checking sites.
        producer: RabbitMQ producer for sending notifications.
        check_interval: Interval between checks in seconds.

    Example:
        >>> tracker = await create_tracker()
        >>> producer = create_producer()
        >>> await check_demon(tracker, producer, check_interval=10)
    """
    try:
        while True:
            try:
                if updated_sites := await tracker.check_all_sites():
                    for url in updated_sites:
                        await producer.publish(
                            exchange="sites",
                            routing_key="updated",
                            message={"url": url, "status": "updated"},
                        )
                        logger.info(f"Sent update notification for: {url}")
            except Exception as e:
                logger.error(f"Error in check demon: {e}")
            await asyncio.sleep(check_interval)
    finally:
        await producer.close()


async def main() -> None:
    """
    Application entry point.

    Creates the Tracker and RabbitMQ producer, then starts
    the site monitoring demon.
    """
    tracker = await create_tracker()
    producer = create_producer()

    logger.info("Tracker initialized, starting monitoring demon")
    await check_demon(tracker, producer)
