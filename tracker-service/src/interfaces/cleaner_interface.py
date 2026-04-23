from abc import ABC, abstractmethod


class ICleanerRepository(ABC):
    """Interface for HTML cleaner. Removes garbage HTML tags."""

    @abstractmethod
    def clear_html(self, html_page: str) -> str:
        """
        Clean HTML page from irrelevant content.

        Args:
            html_page: Raw HTML content.

        Returns:
            Cleaned text content.
        """
        pass
