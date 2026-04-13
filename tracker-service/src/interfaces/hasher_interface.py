from abc import ABC, abstractmethod


class IHasherRepository(ABC):
    """Interface for hasher"""

    @abstractmethod
    def calculate_hash(self, html_page: str) -> str:
        pass
