
import ast
from abc import ABC, abstractmethod
from pathlib import Path
from pydantic import BaseModel, Field


class Chunk(BaseModel):
    """
    #### Chunk class
    \n
    Amount of ***python code*** or ***text*** that has been properly cut
    """
    file_path: Path
    line_start: int = Field(default=1, ge=1)
    line_end: int = Field(default=1, ge=1)
    content: str = Field(default="")

    def update_content(self, new_end: int, new_content: str) -> None:
        if new_end:
            self.line_end = new_end

        if new_content:
            self.content = new_content


class Chunker(ABC):
    def __init__(self, max_chunk_size: int = 2000) -> None:
        if max_chunk_size <= 0:
            raise ValueError("max_chunk_size must be positive")
        self.max_chunk_size = max_chunk_size

    @abstractmethod
    def chunk_file(self, file: Path) -> list[Chunk]:
        pass


class Python_chunker(Chunker):
    """
    #### Python_chunker class
    \n
    Implements the '*chunk_file*' method to split a Python file
    in multiple **'Chunks'** using the AST library
    """
    def __init__(self, max_chunk_size: int = 2000) -> None:
        super().__init__(max_chunk_size)

    def _node_start(self, node: ast.AST) -> int:
        """
        #### _node_start
        \n
        Get a node's first line, including decorators
        """
        if node is None:
            return 0

        start: int = node.lineno  # type: ignore

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            if node.decorator_list:
                start = min(
                    decorator.lineno
                    for decorator in node.decorator_list
                )
        return start - 1

    def _get_boundaries(self, tree: ast.Module, lines: list[str]) -> list[int]:
        """
        #### _get_boundaries
        \n
        Find AST boundaries, including methods of large classes
        """
        boundaries: set[int] = {0, len(lines)}

        for node in tree.body:
            if not hasattr(node, "lineno"):
                continue
            if node.end_lineno is None:
                continue

            start: int = self._node_start(node)
            end: int = node.end_lineno

            boundaries.add(start)
            boundaries.add(end)

            if isinstance(node, ast.ClassDef):
                text: str = "".join(lines[start:end])

                if len(text) > self.max_chunk_size:
                    for child in node.body:
                        if not hasattr(child, "lineno"):
                            continue
                        if child.end_lineno is None:
                            continue

                        boundaries.add(self._node_start(child))
                        boundaries.add(child.end_lineno)

        return sorted(boundaries)

    def chunk_file(self, file: Path) -> list[Chunk]:
        """
        #### chunk_file
        \n
        Split a Python file using AST-based boundaries
        """
        try:
            content: str = file.read_text(encoding="utf-8")
            tree: ast.Module = ast.parse(content)
        except (OSError, UnicodeError, SyntaxError, ValueError):
            return []

        lines: list[str] = content.splitlines(keepends=True)

        if not lines:
            return []

        buffer: str = ""
        buffer_start: int = 1
        buffer_end: int = 1
        boundaries: list[int] = self._get_boundaries(tree, lines)
        chunks: list[Chunk] = []

        def flush() -> None:
            nonlocal buffer

            if buffer:
                chunks.append(
                    Chunk(
                        file_path=file,
                        line_start=buffer_start,
                        line_end=buffer_end,
                        content=buffer
                    )
                )
                buffer = ""

        def add_piece(text: str, start: int, end: int) -> None:
            nonlocal buffer, buffer_start, buffer_end

            if not text:
                return

            if buffer and len(buffer) + len(text) > self.max_chunk_size:
                flush()

            if not buffer:
                buffer_start = start

            buffer += text
            buffer_end = end

        positions = boundaries

        for index in range(len(positions) - 1):
            start: int = positions[index]
            end: int = positions[index + 1]
            region: str = "".join(lines[start:end])

            if len(region) <= self.max_chunk_size:
                add_piece(region, start + 1, end)
                continue

            for line_index in range(start, end):
                line: str = lines[line_index]
                line_number: int = line_index + 1

                if len(line) <= self.max_chunk_size:
                    add_piece(line, line_number, line_number)
                else:
                    for pos in range(0, len(line), self.max_chunk_size):
                        piece = line[pos:pos + self.max_chunk_size]
                        add_piece(piece, line_number, line_number)

        flush()
        return chunks


class Text_chunker(Chunker):
    def __init__(self, max_chunk_size: int = 2000) -> None:
        super().__init__(max_chunk_size)

    def chunk_file(self, file: Path) -> list[Chunk]:
        return []
