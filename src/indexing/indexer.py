import os
from pathlib import Path
from tqdm import tqdm
from .chunkers import Chunk, Python_chunker, Text_chunker


class Indexer():
    """
    Roams the 'data/raw/' folder in search of relevant files
    from the 'vLLM' repository.
    """
    def __init__(self, max_chunk_size: int = 2000) -> None:
        self.max_chunk_size: int = max_chunk_size
        self.chunks: dict[str, list[list[Chunk]]] = {}

    def _identify_files(self, route: Path = Path('data/raw/vllm-0.10.1')
                        ) -> dict[str, list[Path]]:
        """
        Gets all the python files (.py) and the text
        files (.txt/.md), and returns them as a dictionary
        *dict[str, list[str]]*.
        """
        content: list[str] = os.listdir(route)

        python_files: set[Path] = set()
        text_files: set[Path] = set()

        for file in content:
            file_path = Path(os.path.join(route, file))

            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as fd:
                        if fd.read():
                            if file.endswith('.py'):
                                python_files.add(Path(file_path))
                            elif file.endswith(('.md', '.txt')):
                                text_files.add(Path(file_path))
                except (OSError, UnicodeError):
                    continue
            elif os.path.isdir(file_path):
                route_files: dict[str, list[Path]] = (
                    self._identify_files(file_path)
                )
                python_files.update(route_files['python'])
                text_files.update(route_files['text'])

        return {'python': list(python_files), 'text': list(text_files)}

    def chunking(self) -> list[list[Chunk]]:
        """
        Applies a chunking strategy with a given
        self.max_chunk_size. Chunks are saved in the
        */data/chunks* folder
        """
        files: dict[str, list[Path]] = self._identify_files()
        python_chunker = Python_chunker(self.max_chunk_size)
        text_chunker = Text_chunker(self.max_chunk_size)
        python_chunks: list[list[Chunk]] = []
        text_chunks: list[list[Chunk]] = []

        if not files["python"] and files["text"]:
            print("No files were identified. Exiting the program")
            return []

        for lst in files:
            for file in tqdm(files[lst], desc=f"Chunking {lst}",
                             unit="file"):
                if file.suffix == ".py":
                    python_chunks.append(python_chunker.chunk_file(file))
                elif file.suffix == ".md" or file.suffix == ".txt":
                    text_chunks.append(text_chunker.chunk_file(file))
        return list(python_chunks) + list(text_chunks)
