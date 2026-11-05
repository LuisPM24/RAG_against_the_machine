import os
from pathlib import Path


class Indexer():
    """
    #### Indexer class:
    \n
    Roams the 'data/raw/' folder in search of relevant files
    from the 'vLLM' repository.
    """
    def __init__(self, max_chunk_size: int = 2000,
                 indexing_method: str = "bm25") -> None:
        self.max_chunk_size: int = max_chunk_size
        self.indexing_method = indexing_method
        self.python_indexation: str = ""
        self.text_indexation: str = ""

    def _identify_files(self, route: Path = Path('data/raw/vllm-0.10.1')
                        ) -> dict[str, list[Path]]:
        """
        #### _identify_files():
        \n
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

    def chunking(self) -> None:
        """
        #### chunking()
        \n
        Applies a chunking strategy with a given
        self.max_chunk_size. Chunks are saved in the
        */data/chunks* folder
        """
        files: dict[str, list[Path]] = self._identify_files()

        if not files["python"] and files["text"]:
            print("No files were identified. Exiting the program")

        for lst in files:
            folder: Path = Path(os.path.join('data/chunks', lst))

            for file in files[lst]:
                folder.mkdir(exist_ok=True, parents=True)

        return
