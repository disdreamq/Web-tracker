from logging import getLogger

from src.core.config import get_settings
from src.rabbitmq.rabbit_publisher import RabbitMQProducer

logger = getLogger(__name__)


async def publish_message(url: str, producer: RabbitMQProducer) -> None:
    """Publish an update notification message to RabbitMQ.

    Sends a message with the updated URL to the configured exchange and routing key.

    Args:
        url: The URL that was updated.
        producer: RabbitMQ producer instance for publishing messages.

    Raises:
        Exception: If publishing to RabbitMQ fails (logged but not re-raised).
    """
    settings = get_settings()
    try:
        await producer.publish(
            exchange=settings.rabbitmq_exchange_name,
            routing_key=settings.rabbitmq_routing_key_updated,
            message={"url": url},
        )
        logger.info("Sent update notification for: %s", url)
    except Exception as e:
        logger.error("Failed to publish notification for %s: %s", url, e)
