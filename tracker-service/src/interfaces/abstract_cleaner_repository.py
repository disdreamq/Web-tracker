from abc import ABC, abstractmethod


class ICleanerRepository(ABC):
    """Interface for HTML cleaner. Removes garbage HTML tags"""

    @abstractmethod
    async def clear(self, html_page: str) -> str:
        raise NotImplementedError

