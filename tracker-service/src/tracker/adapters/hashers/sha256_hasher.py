import hashlib

from src.core.exceptions import UnexpectedException
from src.interfaces.hasher_interface import IHasherRepository


class BaseHasher(IHasherRepository):
    """
    Hash calculator using SHA-256 algorithm.

    Computes cryptographic hash of content for change detection.
    """

    def calculate_hash(self, html_page: str) -> str:
        """
        Calculate SHA-256 hash of content.

        Args:
            html_page: Content to hash.

        Returns:
            Hexadecimal representation of the hash.

        Raises:
            UnexpectedException: If an error occurs during hashing.

        Example:
            >>> hasher = BaseHasher()
            >>> hash = hasher.calculate_hash("content")
            >>> print(hash)
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        """
        try:
            hash = hashlib.sha256(html_page.encode()).hexdigest()
            return hash
        except Exception as e:
            raise UnexpectedException(f"Unexpected error: {e}") from e
