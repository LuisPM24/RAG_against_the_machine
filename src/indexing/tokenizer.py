import re


class Tokenizer:
    """Tokenize Python source code and text for lexical retrieval."""

    def _split_identifier(self, identifier: str) -> list[str]:
        """Split snake_case and camelCase identifiers into tokens."""
        parts: list[str] = identifier.split("_")
        tokens: list[str] = []

        for part in parts:
            words: list[str] = re.findall(
                r"[A-Z]+(?=[A-Z][a-z]|\d|$)|"
                r"[A-Z]?[a-z]+|[A-Z]+|\d+",
                part
            )
            tokens.extend(word.lower() for word in words)

        return tokens

    def tokenize(self, text: str) -> list[str]:
        """Extract normalized tokens and preserve full identifiers."""
        identifiers: list[str] = re.findall(r"[A-Za-z0-9_]+", text)
        tokens: list[str] = []

        for identifier in identifiers:
            normalized: str = identifier.lower()
            parts: list[str] = self._split_identifier(identifier)

            if len(parts) > 1:
                tokens.append(normalized)

            tokens.extend(parts)

        return tokens
