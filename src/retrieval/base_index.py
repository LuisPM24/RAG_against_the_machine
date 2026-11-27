import math
from abc import ABC, abstractmethod
from collections import Counter
from indexing import Chunk
from .tokenizer import Tokenizer


class BaseIndex(ABC):
    """Define the common interface for retrieval indexes."""

    @abstractmethod
    def build(self, chunks: list[list[Chunk]]) -> None:
        """Build the index from chunks."""
        pass

    @abstractmethod
    def search(self, query: str, k: int) -> list[Chunk]:
        """Return the top-k most relevant chunks."""
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """Save the index to disk."""
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        """Load a previously saved index."""
        pass


class TFIDFIndex(BaseIndex):
    """Implement lexical retrieval using TF-IDF."""

    def __init__(self) -> None:
        """Initialize the TF-IDF index."""
        self.tokenizer: Tokenizer = Tokenizer()
        self.docs: list[list[Chunk]] = []
        self.vectors: list[list[dict[str, float]]] = []
        self.idf: dict[str, float] = {}

    def build(self, chunks: list[list[Chunk]]) -> None:
        """Build the TF-IDF index from documents."""
        self.docs = [doc for doc in chunks if doc]
        self.vectors = []
        self.idf = {}

        if not self.docs:
            return

        doc_freqs: Counter[str] = Counter()
        term_freqs: list[list[Counter[str]]] = []

        for doc in self.docs:
            doc_terms: set[str] = set()
            doc_frequencies: list[Counter[str]] = []

            for chk in doc:
                tokens: list[str] = self.tokenizer.tokenize(chk.content)
                frequencies: Counter[str] = Counter(tokens)

                doc_frequencies.append(frequencies)
                doc_terms.update(frequencies.keys())

            term_freqs.append(doc_frequencies)
            doc_freqs.update(doc_terms)

        total_docs: int = len(self.docs)

        for term, df in doc_freqs.items():
            self.idf[term] = (
                math.log((total_docs + 1) / (df + 1)) + 1
            )

        for doc_frequencies in term_freqs:
            doc_vectors: list[dict[str, float]] = []

            for frequencies in doc_frequencies:
                vector: dict[str, float] = {}

                for term, tf in frequencies.items():
                    vector[term] = tf * self.idf[term]

                norm: float = math.sqrt(
                    sum(weight ** 2 for weight in vector.values())
                )

                if norm > 0:
                    for term in vector:
                        vector[term] /= norm

                doc_vectors.append(vector)

            self.vectors.append(doc_vectors)

    def search(self, query: str, k: int) -> list[Chunk]:
        """Return the k most relevant chunks for a query."""
        if not query.strip() or k <= 0 or not self.docs:
            return []

        words: list[str] = self.tokenizer.tokenize(query)
        frequencies: Counter[str] = Counter(words)
        query_vector: dict[str, float] = {}

        for term, tf in frequencies.items():
            if term in self.idf:
                query_vector[term] = tf * self.idf[term]

        norm: float = math.sqrt(
            sum(weight ** 2 for weight in query_vector.values())
        )

        if norm == 0:
            return []

        for term in query_vector:
            query_vector[term] /= norm

        results: list[tuple[float, Chunk]] = []

        for doc, doc_vectors in zip(self.docs, self.vectors):
            for chk, vector in zip(doc, doc_vectors):
                score: float = sum(
                    weight * vector.get(term, 0.0)
                    for term, weight in query_vector.items()
                )

                if score > 0:
                    results.append((score, chk))

        results.sort(key=lambda result: result[0], reverse=True)

        return [chk for _, chk in results[:k]]

    def save(self, path: str) -> None:
        """Save the index to disk."""
        pass

    def load(self, path: str) -> None:
        """Load a previously saved index."""
        pass
