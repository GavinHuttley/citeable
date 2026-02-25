"""Auto key generation, unique key assignment, and .bib file writing."""

from __future__ import annotations

import string
from pathlib import Path
from typing import TYPE_CHECKING

from citeable._validate import extract_surname

if TYPE_CHECKING:
    from citeable._entries import CitationBase


def generate_key(author: list[str], year: int) -> str:
    """Generate a citation key from the first author surname and year.

    Algorithm:
    1. Extract surname from the first author (before comma, or last token).
    2. Strip non-ASCII and spaces; title-case.
    3. Return ``"{surname}.{year}"``.
    """
    surname = extract_surname(author[0])
    return f"{surname}.{year}"


def assign_unique_keys(citations: list[CitationBase]) -> list[CitationBase]:
    """Deduplicate *citations* by value and resolve key collisions in-place.

    Returns the deduplicated list (mutated in-place for surviving objects).
    """
    seen: dict[CitationBase, CitationBase] = {}
    unique: list[CitationBase] = []
    for c in citations:
        if c not in seen:
            seen[c] = c
            unique.append(c)

    key_groups: dict[str, list[CitationBase]] = {}
    for c in unique:
        key_groups.setdefault(c.key, []).append(c)

    for key, group in key_groups.items():
        if len(group) <= 1:
            continue
        if len(group) > 26:
            msg = f"More than 26 collisions for key {key!r}"
            raise ValueError(msg)
        for i, c in enumerate(group):
            c.key = f"{key}.{string.ascii_lowercase[i]}"

    return unique


def write_bibtex(citations: list[CitationBase], path: str | Path) -> None:
    """Deduplicate, assign unique keys, and write a ``.bib`` file."""
    unique = assign_unique_keys(citations)
    content = "\n\n".join(str(c) for c in unique)
    Path(path).write_text(content, encoding="utf-8")
