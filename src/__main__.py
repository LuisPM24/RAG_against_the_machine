import sys
from indexing import Parser, Indexer
from retrieval import tfidfIndex


def main() -> None:
    """Run indexing and test TF-IDF retrieval."""
    try:
        # Get arguments
        parser = Parser.get_args()

        # Indexing
        indexer = Indexer(parser.max_chunk_size)
        docs = indexer.chunking()

        # Retriever
        if parser.indexing_method == "tfidf":
            retriever = tfidfIndex()
        else:
            return

        retriever.build(docs)

        # Test
        query = "This is a test"
        results = retriever.search(query, 5)

        print(f"\nQuery: {query}")

        for i, chunk in enumerate(results, start=1):
            print(f"\n{i}. {chunk.file_path}")
            print(f"Content: {chunk.content}")

    except Exception as e:
        print(f"Error - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
