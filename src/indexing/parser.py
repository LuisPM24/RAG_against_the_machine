import argparse
from typing import Literal
from pydantic import BaseModel, Field, ValidationError


class Parser(BaseModel):
    """Validate command-line arguments."""

    max_chunk_size: int = Field(default=2000, gt=0, le=2000)
    indexing_method: Literal["tfidf"] = "tfidf"

    @classmethod
    def get_args(cls) -> "Parser":
        """Parse and validate command-line arguments."""
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--max_chunk_size",
            type=int,
            default=2000,
            metavar="[1-2000]",
            help="Maximum chunk size in characters"
        )

        parser.add_argument(
            "--indexing",
            dest="indexing_method",
            type=str,
            default="tfidf",
            choices=["tfidf"]
        )

        args = parser.parse_args()

        try:
            return cls(**vars(args))
        except ValidationError:
            parser.error("max_chunk_size must be between 1 and 2000")
