from src.websocket.connection_manager import ConnectionManager

manager = ConnectionManager()


async def get_connection_manager() -> ConnectionManager:
    return manager
