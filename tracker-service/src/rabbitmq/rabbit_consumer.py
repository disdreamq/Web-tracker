import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aio_pika.abc import AbstractChannel, AbstractIncomingMessage

from src.core.exceptions import RabbitMQMessageError
from src.interfaces.rabbit_consumer_interface import IRabbitMQConsumer
from src.rabbitmq.rabbit_connection import get_channel

logger = logging.getLogger(__name__)

Handler = Callable[[dict[str, Any]], Awaitable[None]]


class RabbitMQConsumer(IRabbitMQConsumer):
    """
    Simple RabbitMQ consumer using aio-pika.

    Subscribes to queues and processes messages with user-defined handlers.

    Example:
        >>> async def handler(message: dict):
        ...     print(f"Received: {message['url']}")
        >>>
        >>> consumer = RabbitMQConsumer()
        >>> await consumer.subscribe("updates", handler, exchange="sites", routing_key="updated")
        >>> await consumer.close()
    """

    def __init__(self):
        """Initialize the consumer with empty channel reference."""
        self._channel: AbstractChannel | None = None
        self._handlers: dict[str, Handler] = {}

    async def subscribe(
        self,
        queue_name: str,
        handler: Handler,
        exchange: str | None = None,
        routing_key: str | None = None,
    ) -> None:
        """
        Subscribe to a queue with a message handler.

        Args:
            queue_name: Queue name to consume from.
            handler: Async function to process messages.
            exchange: Optional exchange to bind to.
            routing_key: Optional routing key for binding.

        Raises:
            RabbitMQMessageError: If subscription fails.
        """
        try:
            if self._channel is None:
                self._channel = await get_channel()

            # Declare queue
            queue = await self._channel.declare_queue(queue_name, durable=True)

            # Bind to exchange if provided
            if exchange:
                exchange_obj = await self._channel.get_exchange(exchange)
                await queue.bind(exchange_obj, routing_key or "")

            # Store handler for this queue
            self._handlers[queue_name] = handler

            # Start consuming
            await queue.consume(self._make_callback(handler, queue_name))

            logger.info(f"Subscribed to queue: {queue_name}")

        except Exception as e:
            logger.exception(f"Failed to subscribe to queue: {e}")
            raise RabbitMQMessageError(f"Subscription failed: {e}") from e

    def _make_callback(self, handler: Handler, queue_name: str) -> Callable:
        """
        Create a callback wrapper for message processing.

        Args:
            handler: User-defined message handler.
            queue_name: Queue name for logging.

        Returns:
            Callback function for aio_pika.
        """

        async def callback(message: AbstractIncomingMessage) -> None:
            async with message.process():
                try:
                    body = json.loads(message.body.decode("utf-8"))
                    logger.debug(f"[{queue_name}] Received: {body}")
                    await handler(body)
                except json.JSONDecodeError as e:
                    logger.error(f"[{queue_name}] Invalid JSON: {e}")
                except Exception as e:
                    logger.error(f"[{queue_name}] Handler error: {e}")
                    raise

        return callback

    async def close(self) -> None:
        """Close the channel and all subscriptions."""
        if self._channel is not None:
            await self._channel.close()
            logger.info("RabbitMQ consumer closed")
            self._channel = None
            self._handlers.clear()

