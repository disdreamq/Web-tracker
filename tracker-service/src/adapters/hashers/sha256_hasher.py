import hashlib

from src.interfaces.abstract_hasher_repository import IHasherRepository


class BaseHasher(IHasherRepository):
    async def calculate_hash(self, html_page: str) -> str:
        try:
            hash = hashlib.sha256(html_page.encode()).hexdigest()
            return hash
        except Exception:  # TODO доделать исключения
            raise
