from collections.abc import Awaitable, Callable
from logging import getLogger
from typing import Any

from src.rabbitmq.rabbitmq_consumer import RabbitMQConsumer
from src.tracker.tracker import Tracker

logger = getLogger(__name__)


async def create_site_handler(
    tracker: Tracker,
) -> Callable[[dict[str, Any]], Awaitable[None]]:
    """
    Create a message handler for new site subscriptions.

    Args:
        tracker: Tracker instance for starting site tracking.

    Returns:
        Async handler function for RabbitMQ messages.
    """

    async def handler(message: dict[str, Any]) -> None:
        """
        Process incoming site subscription request.

        Args:
            message: Message with 'url' field.
        """
        url = message.get("url")
        if not url:
            logger.warning("Received message without 'url' field: %s", message)
            return

        logger.info("Received request to start tracking: %s", url)
        try:
            await tracker.start_track(url)
            logger.info("Successfully started tracking: %s", url)
        except Exception as e:
            logger.error("Failed to start tracking %s: %s", url, e)

    return handler


async def subscribe_worker(
    tracker: Tracker,
    consumer: RabbitMQConsumer,
    queue_name: str = "new_sites",
    exchange: str = "sites",
    routing_key: str = "new",
) -> None:
    """
    Worker that listens for new site subscription requests.

    Subscribes to a queue and starts tracking new sites
    when messages arrive. This is a long-running process.

    Args:
        tracker: Tracker instance for site management.
        consumer: RabbitMQ consumer instance.
        queue_name: Queue name to subscribe to.
        exchange: Exchange to bind to.
        routing_key: Routing key for binding.

    Example:
        >>> tracker = await create_tracker()
        >>> consumer = RabbitMQConsumer()
        >>> await subscribe_worker(tracker, consumer)
        >>> await consumer.close()
    """
    handler = await create_site_handler(tracker)

    await consumer.subscribe(
        queue_name=queue_name,
        handler=handler,
        exchange=exchange,
        routing_key=routing_key,
    )

    logger.info(f"Subscribe worker started, listening on {exchange}/{routing_key}")
    return
