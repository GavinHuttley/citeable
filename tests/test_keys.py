"""Tests for key generation and assign_unique_keys."""

import pytest

from citeable import Article, Misc, Software, assign_unique_keys
from citeable._keys import generate_key

# ── generate_key ─────────────────────────────────────────────────────────


def test_generate_key_comma_format():
    assert generate_key(["Huttley, Gavin"], 2025) == "Huttley.2025"


def test_generate_key_space_format():
    assert generate_key(["Gavin Huttley"], 2025) == "Huttley.2025"


def test_generate_key_strips_non_ascii():
    assert generate_key(["Müller, Hans"], 2020) == "Mller.2020"


def test_generate_key_title_cases():
    assert generate_key(["van der berg, Jan"], 2020) == "Vanderberg.2020"


# ── assign_unique_keys ──────────────────────────────────────────────────


def test_assign_unique_keys_no_collision():
    a = Misc(author=["Smith, A"], title="Paper A", year=2024)
    b = Misc(author=["Jones, B"], title="Paper B", year=2024)
    result = assign_unique_keys([a, b])
    assert len(result) == 2
    assert a.key == "Smith.2024"
    assert b.key == "Jones.2024"


def test_assign_unique_keys_collision():
    a = Misc(author=["Smith, A"], title="Paper A", year=2024)
    b = Misc(author=["Smith, B"], title="Paper B", year=2024)
    result = assign_unique_keys([a, b])
    assert len(result) == 2
    assert a.key == "Smith.2024.a"
    assert b.key == "Smith.2024.b"


def test_assign_unique_keys_deduplication():
    a = Article(
        author=["Smith, A"],
        title="Paper",
        year=2024,
        journal="J",
        volume=1,
        pages="1",
        app="app1",
    )
    b = Article(
        author=["Smith, A"],
        title="Paper",
        year=2024,
        journal="J",
        volume=1,
        pages="1",
        app="app2",
    )
    result = assign_unique_keys([a, b])
    assert len(result) == 1
    assert result[0] is a


def test_assign_unique_keys_preserves_order():
    a = Misc(author=["Smith, A"], title="First", year=2024)
    b = Misc(author=["Smith, B"], title="Second", year=2024)
    c = Misc(author=["Smith, C"], title="Third", year=2024)
    result = assign_unique_keys([a, b, c])
    assert result == [a, b, c]
    assert a.key == "Smith.2024.a"
    assert b.key == "Smith.2024.b"
    assert c.key == "Smith.2024.c"


def test_assign_unique_keys_returns_list():
    a = Misc(author=["Smith, A"], title="Paper", year=2024)
    result = assign_unique_keys([a])
    assert isinstance(result, list)
    assert result == [a]


def test_assign_unique_keys_empty():
    result = assign_unique_keys([])
    assert result == []


def test_assign_unique_keys_too_many_collisions():
    citations = [
        Misc(author=["Smith, A"], title=f"Paper {i}", year=2024) for i in range(27)
    ]
    with pytest.raises(ValueError, match="More than 26 collisions"):
        assign_unique_keys(citations)


def test_assign_unique_keys_mixed_types_same_key():
    a = Misc(author=["Smith, A"], title="Misc Paper", year=2024)
    b = Software(author=["Smith, B"], title="Software", year=2024)
    result = assign_unique_keys([a, b])
    assert len(result) == 2
    assert a.key == "Smith.2024.a"
    assert b.key == "Smith.2024.b"
