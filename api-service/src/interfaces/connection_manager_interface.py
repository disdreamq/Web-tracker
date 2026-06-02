from abc import ABC, abstractmethod

from fastapi import WebSocket


class IConnectionManager(ABC):
    """Connection manager interface for WebSocket management.

    Defines the contract for managing WebSocket connections and sending messages
    to connected users. Implemented by ConnectionManager.
    """

    @abstractmethod
    async def connect(self, websocket: WebSocket, user_id: int):
        """Accept and register a new WebSocket connection.

        Args:
            websocket: WebSocket connection instance.
            user_id: User identifier associated with the connection.
        """
        pass

    @abstractmethod
    async def disconnect(self, websocket: WebSocket, user_id: int):
        """Remove a WebSocket connection from active connections.

        Args:
            websocket: WebSocket connection instance to remove.
            user_id: User identifier associated with the connection.

        Note:
            If this was the last connection for the user, the user entry
            will be removed from active connections.
        """
        pass

    @abstractmethod
    async def send_to_user(self, user_id: int, message: dict):
        """Send a JSON message to all active connections of a user.

        Args:
            user_id: User identifier to send the message to.
            message: Dictionary payload to send as JSON.

        Note:
            If the user has no active connections, the message is silently ignored.
        """
        pass
