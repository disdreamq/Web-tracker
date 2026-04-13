import hashlib

from src.core.exceptions import UnexpectedException
from src.interfaces.hasher_interface import IHasherRepository


class BaseHasher(IHasherRepository):
    def calculate_hash(self, html_page: str) -> str:
        try:
            hash = hashlib.sha256(html_page.encode()).hexdigest()
            return hash
        except Exception as e:
            raise UnexpectedException(f"Unexpected error: {e}") from e
