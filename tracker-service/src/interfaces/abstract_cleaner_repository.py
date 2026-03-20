from abc import ABC, abstractmethod


class ICleanerRepository(ABC):
    """Interface for HTML cleaner. Removes garbage HTML tags"""

    @abstractmethod
    async def clear_html(self, html_page: str) -> str:
        raise NotImplementedError

