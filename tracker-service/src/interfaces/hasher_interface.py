from abc import ABC, abstractmethod


class IHasherRepository(ABC):
    """Interface for hash calculator."""

    @abstractmethod
    def calculate_hash(self, content: str) -> str:
        """
        Calculate hash of content.

        Args:
            content: Content to hash.

        Returns:
            Computed hash.
        """
        pass
