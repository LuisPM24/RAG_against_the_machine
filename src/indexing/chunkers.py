import ast
import re
from abc import ABC, abstractmethod
from pathlib import Path
from pydantic import BaseModel, Field


class Chunk(BaseModel):
    """Amount of ***python code*** or ***text*** that has been properly cut"""
    file_path: Path
    line_start: int = Field(default=1, ge=1)
    line_end: int = Field(default=1, ge=1)
    first_character_index: int = Field(default=0, ge=0)
    last_character_index: int = Field(default=0, ge=0)
    content: str = Field(default="")


class Chunker(ABC):
    def __init__(self, max_chunk_size: int = 2000) -> None:
        if not 1 <= max_chunk_size <= 2000:
            raise ValueError("max_chunk_size must be between 1 and 2000")
        self.max_chunk_size = max_chunk_size

    @abstractmethod
    def chunk_file(self, file: Path) -> list[Chunk]:
        pass


class PythonChunker(Chunker):
    """
    Implements the '*chunk_file*' method to split a Python file
    in multiple **'Chunks'** using the AST library
    """
    def __init__(self, max_chunk_size: int = 2000) -> None:
        super().__init__(max_chunk_size)

    def _node_start(self, node: ast.stmt) -> int:
        """Get a node's first line, including decorators."""
        start: int = node.lineno

        if isinstance(node,
                      (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.decorator_list:
                start = min(decorator.lineno
                            for decorator in node.decorator_list)
        return start - 1

    def _get_boundaries(self, tree: ast.Module, lines: list[str]) -> list[int]:
        """Find AST boundaries, including methods of large classes"""
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
        """Split a Python file using AST-based boundaries"""
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

        character_index: int = 0

        for chunk in chunks:
            chunk.first_character_index = character_index
            character_index += len(chunk.content)
            chunk.last_character_index = character_index

        return chunks


class TextChunker(Chunker):
    """Split Markdown and text files into structured chunks."""

    def _scan_fence(self, line: str, fence: str | None) -> str | None:
        """Track the opening and closing of Markdown code fences."""
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)

        if match is None:
            return fence

        marker = match.group(1)
        rest = match.group(2)

        if fence is None:
            return marker

        if (marker[0] == fence[0] and len(marker) >= len(fence)
           and not rest.strip()):
            return None

        return fence

    def _get_boundaries(self, lines: list[str]) -> list[int]:
        """Find Markdown headings outside fenced code blocks."""
        boundaries: set[int] = {0, len(lines)}
        fence: str | None = None

        for index, line in enumerate(lines):
            if fence is None:
                if re.match(r"^ {0,3}#{1,6}(?:\s|$)", line):
                    boundaries.add(index)

            fence = self._scan_fence(line, fence)

        return sorted(boundaries)

    def _paragraph_boundaries(self, lines: list[str], start: int,
                              end: int) -> list[int]:
        """Find paragraph boundaries within a text section."""
        boundaries: list[int] = [start]
        fence: str | None = None

        for index in range(start, end):
            line = lines[index]
            fence = self._scan_fence(line, fence)

            if fence is None and not line.strip():
                boundaries.append(index + 1)

        boundaries.append(end)

        return sorted(set(boundaries))

    def chunk_file(self, file: Path) -> list[Chunk]:
        """Split a Markdown or text file into size-limited chunks."""
        try:
            content: str = file.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return []

        lines: list[str] = content.splitlines(keepends=True)

        if not lines:
            return []

        boundaries: list[int] = self._get_boundaries(lines)
        chunks: list[Chunk] = []
        buffer: str = ""
        buffer_start: int = 1
        buffer_end: int = 1

        def flush() -> None:
            """Save the current buffer as a chunk."""
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
            """Append text while respecting the maximum chunk size."""
            nonlocal buffer, buffer_start, buffer_end

            if not text:
                return
            if buffer and (len(buffer) + len(text) > self.max_chunk_size):
                flush()
            if not buffer:
                buffer_start = start

            buffer += text
            buffer_end = end

        def add_lines(start: int, end: int) -> None:
            """Split oversized paragraphs into lines."""
            for index in range(start, end):
                line = lines[index]
                line_number = index + 1

                if len(line) <= self.max_chunk_size:
                    add_piece(line, line_number, line_number)
                else:
                    for pos in range(0, len(line), self.max_chunk_size):
                        piece = line[pos:pos + self.max_chunk_size]
                        add_piece(piece, line_number, line_number)

        def add_section(start: int, end: int) -> None:
            """Split a section by paragraphs if it is too large."""
            section = "".join(lines[start:end])

            if len(section) <= self.max_chunk_size:
                add_piece(section, start + 1, end)
                return

            paragraphs = self._paragraph_boundaries(lines, start, end)

            for index in range(len(paragraphs) - 1):
                paragraph_start = paragraphs[index]
                paragraph_end = paragraphs[index + 1]
                paragraph = "".join(lines[paragraph_start:paragraph_end])

                if len(paragraph) <= self.max_chunk_size:
                    add_piece(paragraph, paragraph_start + 1, paragraph_end)
                else:
                    add_lines(paragraph_start, paragraph_end)

        for index in range(len(boundaries) - 1):
            start = boundaries[index]
            end = boundaries[index + 1]
            add_section(start, end)

        flush()
        character_index: int = 0

        for chunk in chunks:
            chunk.first_character_index = character_index
            character_index += len(chunk.content)
            chunk.last_character_index = character_index

        return chunks
