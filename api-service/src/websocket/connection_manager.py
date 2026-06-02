from fastapi import WebSocket

from src.interfaces.connection_manager_interface import IConnectionManager


class ConnectionManager(IConnectionManager):
    """Manages active WebSocket connections for users.

    Stores connections grouped by user_id and provides methods to connect,
    disconnect, and send messages to users.
    """

    def __init__(self):
        self.active_connections: dict[int, set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """Accept and register a new WebSocket connection.

        Args:
            websocket: WebSocket connection instance.
            user_id: User identifier associated with the connection.
        """
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)

    async def disconnect(self, websocket: WebSocket, user_id: int):
        """Remove a WebSocket connection from active connections.

        Args:
            websocket: WebSocket connection instance to remove.
            user_id: User identifier associated with the connection.

        Note:
            If this was the last connection for the user, the user entry
            will be removed from active connections.
        """
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_to_user(self, user_id: int, message: dict):
        """Send a JSON message to all active connections of a user.

        Args:
            user_id: User identifier to send the message to.
            message: Dictionary payload to send as JSON.

        Note:
            If the user has no active connections, the message is silently ignored.
        """
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)
