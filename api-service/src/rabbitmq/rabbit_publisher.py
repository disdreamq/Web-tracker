import json
import logging
from typing import Any

from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractChannel, AbstractExchange

from src.core.exceptions import RabbitMQMessageError
from src.interfaces.rabbit_producer_interface import IRabbitMQProducer
from src.rabbitmq.rabbit_connection import get_channel

logger = logging.getLogger(__name__)


class RabbitMQProducer(IRabbitMQProducer):
    """
    RabbitMQ message producer using aio-pika.

    Provides reliable message publishing with confirmation support.

    Attributes:
        _channel: Cached AMQP channel instance.
    """

    def __init__(self):
        """
        Initialize the RabbitMQ producer.

        Creates a connection and channel for publishing messages.
        """
        self._channel: AbstractChannel | None = None

    async def _get_channel(self) -> AbstractChannel:
        """
        Get or create AMQP channel.

        Returns:
            Active channel instance.
        """
        if self._channel is None:
            self._channel = await get_channel()
        return self._channel

    async def publish(
        self,
        exchange: str,
        routing_key: str,
        message: dict[str, Any],
    ) -> bool:
        """
        Publish a message to RabbitMQ exchange.

        Args:
            exchange: Target exchange name.
            routing_key: Routing key for message routing.
            message: Message payload as dictionary.

        Returns:
            True if message was published successfully.

        Raises:
            RabbitMQMessageError: If message publishing failed.

        Example:
            >>> producer = RabbitMQProducer()
            >>> await producer.publish(
            ...     exchange="sites",
            ...     routing_key="updated",
            ...     message={"url": "https://example.com", "hash": "abc123"}
            ... )
        """
        try:
            channel = await self._get_channel()
            exchange_obj: AbstractExchange = channel.default_exchange

            if exchange != "":
                exchange_obj = await channel.get_exchange(exchange)

            message_body = json.dumps(message).encode("utf-8")
            amqp_message = Message(
                body=message_body,
                delivery_mode=DeliveryMode.PERSISTENT,
                content_type="application/json",
            )

            await exchange_obj.publish(
                message=amqp_message,
                routing_key=routing_key,
                mandatory=True,
            )

            logger.info(f"Published message to {exchange}/{routing_key}: {message}")
            return True

        except Exception as e:
            logger.exception(f"Failed to publish message: {e}")
            raise RabbitMQMessageError(f"Message publishing failed: {e}") from e

    async def close(self) -> None:
        """
        Close the producer connection.

        Safely closes the channel and connection.
        """
        if self._channel is not None:
            await self._channel.close()
            logger.info("RabbitMQ producer closed")
            self._channel = None
