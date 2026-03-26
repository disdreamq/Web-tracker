from abc import ABC, abstractmethod

from src.site.schemas import SSiteCreate, SSiteDTO


class ISiteService(ABC):
    @abstractmethod
    async def create(self, site: SSiteCreate) -> SSiteDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_url(self, url: str) -> SSiteDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> SSiteDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, url: str, hash_to_update: str) -> SSiteDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, url: str) -> bool:
        raise NotImplementedError
