from src.websocket.connection_manager import ConnectionManager

manager = ConnectionManager()


def get_manager() -> ConnectionManager:
    return manager
