from classes import Parser
import sys


def main() -> None:
    """Main function. Runs the application"""
    try:
        parser = Parser.get_args()
        print(f"Max Chunk Size: {parser.max_chunk_size}")
    except Exception as e:
        print(f"Error - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
