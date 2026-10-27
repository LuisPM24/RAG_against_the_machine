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

    def identify_files(self) -> None:
        pass
