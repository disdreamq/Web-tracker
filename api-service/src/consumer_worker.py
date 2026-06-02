from collections.abc import Awaitable, Callable
from logging import getLogger
from typing import Any

from src.core.config import get_settings
from src.interfaces.connection_manager_interface import IConnectionManager
from src.rabbitmq.rabbit_consumer import RabbitMQConsumer

logger = getLogger(__name__)


async def _create_handler(
    connection_manager: IConnectionManager,
) -> Callable[[dict[str, Any]], Awaitable[None]]:
    """Create a message handler for incoming notifications.

    Args:
        connection_manager: Connection manager instance for sending messages.

    Returns:
        Async handler function for RabbitMQ messages.
    """

    async def handler(message: dict[str, Any]) -> None:
        """Process incoming notification message.

        Args:
            message: Message with notification data.
        """
        if not message.get("url"):
            logger.warning("Received message without 'url' field: %s", message)
            return
        logger.info("Received request to start tracking: %s", message)
        try:
            await connection_manager.send_to_user(message)
            logger.info("Successfully started tracking: %s", message)
        except Exception as e:
            logger.error("Failed to start tracking %s: %s", message, e)

    return handler


async def subscribe_worker(
    connection_manager: IConnectionManager,
    consumer: RabbitMQConsumer,
    queue_name: str | None = None,
    exchange: str | None = None,
    routing_key: str | None = None,
) -> None:
    """Worker that listens for notification messages and forwards them to users.

    Subscribes to a RabbitMQ queue and starts processing incoming messages.
    This is a long-running process that should be started on application startup.

    Args:
        connection_manager: Connection manager instance for sending WebSocket messages.
        consumer: RabbitMQ consumer instance.
        queue_name: Queue name to subscribe to (from config if None).
        exchange: Exchange to bind to (from config if None).
        routing_key: Routing key for binding (from config if None).

    Example:
        >>> connection_manager = ConnectionManager()
        >>> consumer = RabbitMQConsumer()
        >>> await subscribe_worker(connection_manager, consumer)
        >>> await consumer.close()
    """

    settings = get_settings()

    # Use config values if not provided
    queue_name = queue_name or settings.rabbitmq_queue_new
    exchange = exchange or settings.rabbitmq_exchange_name
    routing_key = routing_key or settings.rabbitmq_routing_key_new

    handler = await _create_handler(connection_manager)

    await consumer.subscribe(
        queue_name=queue_name,
        handler=handler,
        exchange=exchange,
        routing_key=routing_key,
    )

    logger.info("Subscribe worker started, listening on %s/%s", exchange, routing_key)
