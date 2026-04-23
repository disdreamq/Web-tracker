from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import TypeVar

T = TypeVar("T")


class IDBRepository[T](ABC):
    """Interface for database repositories with base CRUD operations."""

    @abstractmethod
    async def create(self, *args, **kwargs) -> T:
        """
        Create a record in database.

        Args:
            *args: Positional arguments for creation.
            **kwargs: Keyword arguments for creation.

        Returns:
            Created model instance.
        """
        pass

    @abstractmethod
    async def get_by_id(self, *args, **kwargs) -> T | None:
        """
        Get record by ID.

        Args:
            *args: Positional arguments for lookup.
            **kwargs: Keyword arguments for lookup.

        Returns:
            Model instance or None if not found.
        """
        pass

    @abstractmethod
    async def get_by_url(self, *args, **kwargs) -> T | None:
        """
        Get record by URL.

        Args:
            *args: Positional arguments for lookup.
            **kwargs: Keyword arguments for lookup.

        Returns:
            Model instance or None if not found.
        """
        pass

    @abstractmethod
    async def update(self, *args, **kwargs) -> T | None:
        """
        Update record.

        Args:
            *args: Positional arguments for update.
            **kwargs: Keyword arguments for update.

        Returns:
            Updated model instance or None if not found.
        """
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs) -> bool:
        """
        Delete record.

        Args:
            *args: Positional arguments for deletion.
            **kwargs: Keyword arguments for deletion.

        Returns:
            True if deleted, False otherwise.
        """
        pass

    @abstractmethod
    async def get_sites_stream(self, *args, **kwargs) -> AsyncGenerator:
        """
        Return stream of records.

        Args:
            *args: Positional arguments for streaming.
            **kwargs: Keyword arguments for streaming.

        Yields:
            Model instances.
        """
        pass
