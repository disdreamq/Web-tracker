import logging

from httpx import AsyncClient, Response

from src.interfaces.abstract_http_client_repository import IHTTPClientRepository

logger = logging.getLogger(__name__)

class HTTPXClient(IHTTPClientRepository):
    async def get(self, url: str) -> Response:
        try:
            async with AsyncClient() as client:
                response = await client.get(url)
            if response.status_code != 200:
                raise #TODO добавить доменные исключения
            return response
        except Exception: #TODO доделать тут ошибки
            raise

