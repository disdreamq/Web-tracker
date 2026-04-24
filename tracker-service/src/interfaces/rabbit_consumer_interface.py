from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any


class IRabbitMQConsumer(ABC):
    """Interface for RabbitMQ message consumer."""

    @abstractmethod
    async def subscribe(
        self,
        queue_name: str,
        handler: Callable[[dict[str, Any]], Awaitable[None]],
        exchange: str | None = None,
        routing_key: str | None = None,
    ) -> None:
        """
        Subscribe to a RabbitMQ queue.

        Args:
            queue_name: Name of the queue to subscribe to.
            handler: Async callback function to process messages.
            exchange: Optional exchange to bind queue to.
            routing_key: Optional routing key for binding.

        Raises:
            RabbitMQConnectionError: If connection to RabbitMQ failed.
            RabbitMQMessageError: If subscription failed.
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Close the consumer connection.

        Cancels all subscriptions and closes connections.
        """
        pass
