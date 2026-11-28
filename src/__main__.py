import sys
import fire
from cli import CLI


def main() -> None:
    """Run the RAG command-line interface."""
    try:
        fire.Fire(CLI)
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
