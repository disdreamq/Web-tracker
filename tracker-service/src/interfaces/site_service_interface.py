from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from src.site.schemas import SSiteCreate, SSiteDTO


class ISiteService(ABC):
    @abstractmethod
    async def create(self, site: SSiteCreate) -> SSiteDTO:
        pass

    @abstractmethod
    async def get_by_url(self, url: str) -> SSiteDTO | None:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> SSiteDTO | None:
        pass

    @abstractmethod
    async def update(self, url: str, hash_to_update: str) -> SSiteDTO | None:
        pass

    @abstractmethod
    async def delete(self, url: str) -> bool:
        pass

    @abstractmethod
    async def get_sites_stream(self) -> AsyncGenerator:
        pass
