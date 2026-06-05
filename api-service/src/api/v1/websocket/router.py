"""WebSocket endpoints for real-time notifications."""

from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from src.core.security.dependencies import require_auth
from src.user.schemas import SUserDTO
from src.websocket.connection_manager import ConnectionManager
from src.websocket.dependencies import get_connection_manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user: Annotated[SUserDTO, Depends(require_auth)],
    connection_manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
):
    """Handle WebSocket connection for authenticated user.

    Establishes a persistent WebSocket connection for receiving real-time
    update notifications. The user is authenticated via JWT token and
    identified by their user ID from the token payload.

    Args:
        websocket: WebSocket connection instance.
        user: Authenticated user data from JWT token.
        connection_manager: Connection manager for tracking active connections.

    Raises:
        WebSocketDisconnect: When client disconnects from the WebSocket.
    """
    user_id = user.id

    await connection_manager.connect(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket, user_id)
