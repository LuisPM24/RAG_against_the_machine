import os


class Indexer():
    """
    Indexer class:
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

    def identify_files(self, route: str = 'data/raw/vllm-0.10.1'
                       ) -> dict[str, list[str]]:
        """
        Indexer.identify_files()
        \n
        Gets all the python files (.py) and the text
        files (.txt/.md), and returns them as a dictionary
         (dict[str, list[str]])
        """
        content: list[str] = os.listdir(route)

        python_files: set[str] = set()
        text_files: set[str] = set()

        for file in content:
            file_path = os.path.join(route, file)

            if os.path.isfile(file_path):
                if file.endswith('.py'):
                    python_files.add(file_path)
                elif file.endswith(('.md', '.txt')):
                    text_files.add(file_path)
            elif os.path.isdir(file_path):
                route_files: dict[str, list[str]] = (
                    self.identify_files(file_path)
                )
                python_files.update(route_files['python'])
                text_files.update(route_files['text'])
        return {'python': list(python_files), 'text': list(text_files)}
