from abc import ABC, abstractmethod
from typing import Any


class IRabbitMQProducer(ABC):
    """Interface for RabbitMQ message producer."""

    @abstractmethod
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
            RabbitMQConnectionError: If connection to RabbitMQ failed.
            RabbitMQMessageError: If message publishing failed.
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Close the producer connection.

        Safely closes all connections and channels.
        """
        pass
