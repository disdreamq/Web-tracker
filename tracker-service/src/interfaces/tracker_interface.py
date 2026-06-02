from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any


class ITracker(ABC):
    """Interface for website tracker."""

    @abstractmethod
    async def get_hash(self, url: str) -> str:
        """
        Compute hash of page content by URL.

        Args:
            url: URL of the page.

        Returns:
            Computed hash.
        """
        pass

    @abstractmethod
    async def start_track(
        self, url: str
    ) -> Callable[[dict[str, Any]], Awaitable[None]]:
        """
        Start tracking a website.

        Args:
            url: URL of the site to track.
        """
        pass

    @abstractmethod
    async def stop_track(self, url: str) -> None:
        """
        Stop tracking a website.

        Args:
            url: URL of the site to stop tracking.
        """
        pass

    @abstractmethod
    async def check_all_sites(self) -> list[str] | None:
        """
        Check all tracked sites for changes.

        Returns:
            List of URLs with changes or None.
        """
        pass
