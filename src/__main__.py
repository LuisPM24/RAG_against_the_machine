import sys
from indexing import Parser, Indexer
from retrieval import TFIDFIndex


def main() -> None:
    """Run indexing and test TF-IDF retrieval."""
    try:
        parser = Parser.get_args()

        indexer = Indexer(parser.max_chunk_size)
        documents = indexer.chunking()

        if not documents:
            return

        retriever = TFIDFIndex()
        retriever.build(documents)

        query = "How does vLLM manage GPU memory?"
        results = retriever.search(query, 5)

        print(f"\nQuery: {query}")

        for i, chunk in enumerate(results, start=1):
            print(f"\n{i}. {chunk.file_path}")
            print(
                f"Characters: "
                f"{chunk.first_character_index}-"
                f"{chunk.last_character_index}"
            )
            print(f"Content: {chunk.content}")

    except Exception as e:
        print(f"Error - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
