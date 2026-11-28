
from pathlib import Path
from time import perf_counter
from uuid import uuid4
from indexing import Indexer
from retrieval import TFIDFIndex
from data_models import (MinimalSource,
                         MinimalSearchResults,
                         StudentSearchResults)


class CLI:
    """Provide the command-line interface for the RAG system."""

    def index(self, max_chunk_size: int = 2000,
              corpus_path: str = "data/raw",
              index_path: str = "data/processed/tfidf_index.json"
              ) -> None:
        """Build and persist the TF-IDF index."""
        start: float = perf_counter()

        indexer = Indexer(
            max_chunk_size=max_chunk_size,
            corpus_path=Path(corpus_path)
        )

        documents = indexer.chunking()

        if not documents:
            raise ValueError("No valid documents were found")

        retriever = TFIDFIndex()
        retriever.build(documents)
        retriever.save(index_path)

        print("Indexing completed successfully")
        print(f"Index saved to: {index_path}")
        print(f"Documents: {len(documents)}")
        print(f"Chunks: {sum(len(doc) for doc in documents)}")
        print(f"Total time: {perf_counter() - start:.3f} s")

    def search(self, query: str, k: int = 5,
               index_path: str = "data/processed/tfidf_index.json",
               output_path: str = "data/output/search_results/query.json"
               ) -> None:
        """Retrieve the top-k most relevant sources."""
        if k < 0:
            raise ValueError("k cannot be negative")

        retriever = TFIDFIndex()
        retriever.load(index_path)

        chunks = retriever.search(query, k)

        sources: list[MinimalSource] = []

        for chunk in chunks:
            sources.append(
                MinimalSource(
                    file_path=chunk.file_path.as_posix(),
                    first_character_index=chunk.first_character_index,
                    last_character_index=chunk.last_character_index
                )
            )

        result = MinimalSearchResults(
            question_id=str(uuid4()),
            question=query,
            retrieved_sources=sources
        )

        output = StudentSearchResults(search_results=[result], k=k)

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            file.write(output.model_dump_json(indent=4))

        print(output.model_dump_json(indent=4))
        print(f"\nResults saved to: {path}")
