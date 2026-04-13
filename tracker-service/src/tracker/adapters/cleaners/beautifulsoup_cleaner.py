from bs4 import BeautifulSoup

from src.core.exceptions import UnexpectedException
from src.interfaces.cleaner_interface import ICleanerRepository


class BaseCleaner(ICleanerRepository):
    def clear_html(self, html_page: str) -> str:
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
