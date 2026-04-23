from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from src.site.schemas import SSiteCreate, SSiteDTO


class ISiteService(ABC):
    """Interface for site service."""

    @abstractmethod
    async def create(self, site: SSiteCreate) -> SSiteDTO:
        """
        Create a new site.

        Args:
            site: Site data to create.

        Returns:
            Created site DTO.
        """
        pass

    @abstractmethod
    async def get_by_url(self, url: str) -> SSiteDTO | None:
        """
        Get site by URL.

        Args:
            url: Site URL.

        Returns:
            Site DTO or None.
        """
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> SSiteDTO | None:
        """
        Get site by ID.

        Args:
            id: Site ID.

        Returns:
            Site DTO or None.
        """
        pass

    @abstractmethod
    async def update(self, url: str, hash_to_update: str) -> SSiteDTO | None:
        """
        Update site hash.

        Args:
            url: Site URL.
            hash_to_update: New hash value.

        Returns:
            Updated site DTO or None.
        """
        pass

    @abstractmethod
    async def delete(self, url: str) -> bool:
        """
        Delete a site.

        Args:
            url: Site URL.

        Returns:
            True if deleted, False otherwise.
        """
        pass

    @abstractmethod
    async def get_sites_stream(self) -> AsyncGenerator:
        """
        Return stream of all sites.

        Yields:
            Tuples of (url, hash).
        """
        pass
