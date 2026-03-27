from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import TypeVar

T = TypeVar("T")


class IDBepository[T](ABC):
    """Interface for db repositories with base CRUD.

    Raises:
        NotImplementedError for any not implemented methods.
    """

    @abstractmethod
    async def create(self, *args, **kwargs) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, *args, **kwargs) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_url(self, *args, **kwargs) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_sites_stream(self, *args, **kwargs) -> AsyncGenerator:
        raise NotImplementedError
