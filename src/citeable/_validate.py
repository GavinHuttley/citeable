"""Shared validation logic for citeable entry types."""

from __future__ import annotations

import re


def require_field(
    value: object,
    field_name: str,
    entry_type: str,
) -> None:
    """Raise ``ValueError`` if *value* is ``None``."""
    if value is None:
        msg = f"{entry_type} requires {field_name!r}; received None"
        raise ValueError(msg)


def require_non_empty_authors(authors: list[str], entry_type: str) -> None:
    """Raise ``ValueError`` if *authors* is empty."""
    if not authors:
        msg = f"{entry_type} requires at least one author"
        raise ValueError(msg)


def extract_surname(name: str) -> str:
    """Extract surname from an author name string.

    Handles both ``"Last, First"`` and ``"First Last"`` formats.
    Returns the surname stripped of non-ASCII characters and title-cased.
    """
    if "," in name:
        surname = name.split(",", maxsplit=1)[0].strip()
    else:
        surname = name.rsplit(maxsplit=1)[-1].strip()
    surname = re.sub(r"[^A-Za-z]", "", surname)
    return surname.title()
