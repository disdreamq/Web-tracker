"""
RabbitMQ connection and channel configuration.

Provides:
- Async connection to RabbitMQ
- Channel factory for producer/consumer
"""

from aio_pika import connect_robust
from aio_pika.abc import AbstractChannel, AbstractRobustConnection

from src.core.config import get_settings
from src.core.exceptions import RabbitMQConnectionError

settings = get_settings()


async def get_rabbitmq_connection() -> AbstractRobustConnection:
    """
    Get or create RabbitMQ connection.

    Returns:
        Active aio_pika Connection instance.

    Raises:
        RabbitMQConnectionError: If connection to RabbitMQ failed.
    """
    try:
        connection = await connect_robust(
            settings.rabbitmq_url,
            client_properties={"connection_name": "tracker-service"},
        )
        return connection
    except Exception as e:
        raise RabbitMQConnectionError(f"Failed to connect to RabbitMQ: {e}") from e


async def get_channel() -> AbstractChannel:
    """
    Get a channel from the RabbitMQ connection.

    Returns:
        Active aio_pika Channel instance.

    Raises:
        RabbitMQConnectionError: If channel creation failed.
    """
    try:
        connection = await get_rabbitmq_connection()
        channel = await connection.channel()
        return channel
    except Exception as e:
        raise RabbitMQConnectionError(f"Failed to create channel: {e}") from e
