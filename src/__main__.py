from classes import Parser, Indexer
import sys


def main() -> None:
    """Main function. Runs the application"""
    try:
        parser = Parser.get_args()

        indexer = Indexer(
            max_chunk_size=parser.max_chunk_size,
            indexing_method=parser.indexing_method
        )
        print(f"Max Chunk Size: {indexer.max_chunk_size}")
        print(f"Indexing method: {indexer.indexing_method}")
    except Exception as e:
        print(f"Error - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
