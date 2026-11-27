from pathlib import Path
from tqdm import tqdm
from .chunkers import Chunk, PythonChunker, TextChunker


class Indexer:
    """Identify and split supported files from a corpus."""

    def __init__(self, max_chunk_size: int = 2000,
                 corpus_path: Path = Path("data/raw")) -> None:
        """Initialize the corpus path and chunk size."""
        self.max_chunk_size: int = max_chunk_size
        self.corpus_path: Path = corpus_path

    def _identify_files(self, route: Path) -> dict[str, list[Path]]:
        """Identify supported files recursively."""
        files: dict[str, list[Path]] = {"python": [], "text": []}

        if not route.is_dir():
            raise FileNotFoundError(f"Invalid corpus path: {route}")

        for file in sorted(route.rglob("*")):
            if not file.is_file():
                continue

            if file.suffix == ".py":
                files["python"].append(file)
            elif file.suffix in (".md", ".txt"):
                files["text"].append(file)

        return files

    def chunking(self) -> list[list[Chunk]]:
        """Apply the appropriate chunking strategy to each file."""
        files = self._identify_files(self.corpus_path)

        python_chunker = PythonChunker(self.max_chunk_size)
        text_chunker = TextChunker(self.max_chunk_size)

        documents: list[list[Chunk]] = []

        if not files["python"] and not files["text"]:
            print("No supported files were identified")
            return documents

        for file in tqdm(
            files["python"],
            desc="Chunking Python files",
            unit="file"
        ):
            chunks = python_chunker.chunk_file(file)
            if chunks:
                documents.append(chunks)

        for file in tqdm(
            files["text"],
            desc="Chunking text files",
            unit="file"
        ):
            chunks = text_chunker.chunk_file(file)
            if chunks:
                documents.append(chunks)

        return documents
