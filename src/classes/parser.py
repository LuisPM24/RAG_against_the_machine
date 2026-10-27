import argparse
from typing import Literal
from pydantic import BaseModel, Field, ValidationError


class Parser(BaseModel):
    """
    Parser class:
    \n
    Takes the parameters "--max_chunk_size" and "--indexing"
    from the execution command and checks whether the values
    provided are valid.
    """
    max_chunk_size: int = Field(default=2000, gt=0, le=2000)
    indexing_method: Literal["bm25", "tfidf"] = "bm25"

    @classmethod
    def get_args(cls) -> "Parser":
        """
        Gets all arguments from the executed command, then initialize
        the class arguments with those values.
        """
        new_args = argparse.ArgumentParser()

        new_args.add_argument(
            "--max_chunk_size",
            dest="max_chunk_size",
            type=int,
            default=2000,
            metavar="[1-2000]",
            help="Maximum chunk size in characters (default: 2000)"
        )

        new_args.add_argument(
            "--indexing",
            dest="indexing_method",
            type=str,
            default="bm25",
            choices=["bm25", "tfidf"]
        )

        args = new_args.parse_args()

        try:
            return cls(**vars(args))
        except ValidationError:
            new_args.error("max_chunk_size must be between 1 and 2000")
