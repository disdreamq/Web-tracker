from bs4 import BeautifulSoup

from src.core.exceptions import UnexpectedException
from src.interfaces.cleaner_interface import ICleanerRepository


class BaseCleaner(ICleanerRepository):
    """
    HTML cleaner using BeautifulSoup.

    Removes scripts, styles, and other irrelevant HTML tags,
    then returns plain text content.
    """

    def clear_html(self, html_page: str) -> str:
        """
        Clean HTML page from irrelevant content.

        Removes scripts, styles, meta tags, navigation, footers,
        and all HTML attributes, returning plain text.

        Args:
            html_page: Raw HTML content to clean.

        Returns:
            Cleaned text content without HTML tags.

        Raises:
            UnexpectedException: If an error occurs during cleaning.

        Example:
            >>> cleaner = BaseCleaner()
            >>> text = cleaner.clear_html("<html><body><p>Hello</p></body></html>")
            >>> print(text)
            "Hello"
        """
        try:
            soup = BeautifulSoup(html_page, "lxml")

            for tag in soup(
                [
                    "script",
                    "style",
                    "noscript",
                    "meta",
                    "link",
                    "head",
                    "nav",
                    "footer",
                    "header",
                    "form",
                    "button",
                    "input",
                    "aside",
                    "svg",
                    "iframe",
                    "object",
                    "embed",
                ]
            ):
                tag.decompose()

            for tag in soup.find_all(True):
                tag.attrs = {}

            return soup.get_text(strip=True)
        except Exception as e:
            raise UnexpectedException(f"Unexpected error: {e}") from e
