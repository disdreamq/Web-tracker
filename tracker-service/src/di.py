"""
Dependency Injection module.

Factory functions for creating application components with proper dependency injection.
"""

from src.core.config import get_settings
from src.db.infrastructure.session import AsyncSessionLocal
from src.rabbitmq.rabbitmq_publisher import RabbitMQProducer
from src.site.repository import SQLAlchemySiteRepository
from src.site.service import SiteService
from src.tracker.adapters.cleaners.beautifulsoup_cleaner import BaseCleaner
from src.tracker.adapters.hashers.sha256_hasher import BaseHasher
from src.tracker.adapters.http_clients.httpx_client import BaseClient
from src.tracker.tracker import Tracker


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


def get_rabbitmq_config():
    """
    Get RabbitMQ configuration from settings.

    Returns:
        Dictionary with RabbitMQ configuration.
    """
    settings = get_settings()
    return {
        "exchange": settings.rabbitmq_exchange_name,
        "queue_new": settings.rabbitmq_queue_new,
        "queue_updated": settings.rabbitmq_queue_updated,
        "routing_key_new": settings.rabbitmq_routing_key_new,
        "routing_key_updated": settings.rabbitmq_routing_key_updated,
    }
