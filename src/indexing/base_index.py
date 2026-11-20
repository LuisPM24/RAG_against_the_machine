from abc import ABC, abstractmethod
from .chunkers import Chunk


class BaseIndex(ABC):
    """Common Interface for recovery index"""

    @abstractmethod
    def build(self, chunks: list[Chunk]) -> None:
        """Build indexes from chunks"""
        pass

    @abstractmethod
    def search(self, query: str, k: int) -> list[Chunk]:
        """Return top-k indexes"""
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """Save indexes on disc"""
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        """Recover an index previously saved"""
        pass
