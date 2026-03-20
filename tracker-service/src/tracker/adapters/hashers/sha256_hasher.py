import hashlib

from src.core.exceptions import UnexpectedException
from src.interfaces.abstract_hasher_repository import IHasherRepository


class BaseHasher(IHasherRepository):
    async def calculate_hash(self, html_page: str) -> str:
        try:
            hash = hashlib.sha256(html_page.encode()).hexdigest()
            return hash
        except Exception as e:
            raise UnexpectedException(f"Unexpected error: {e}") from e
