from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")

class IHTTPClientRepository[T](ABC):
    """Interface for HTTP client"""
    @abstractmethod
    def get(self, url: str) -> T:
        raise NotImplementedError

