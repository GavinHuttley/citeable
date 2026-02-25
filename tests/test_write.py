"""Tests for write_bibtex."""

from pathlib import Path

import pytest

from citeable import Article, Misc, write_bibtex


def test_write_bibtex_creates_file(tmp_path):
    a = Misc(author=["Smith, A"], title="Paper A", year=2024)
    b = Misc(author=["Jones, B"], title="Paper B", year=2024)
    path = tmp_path / "refs.bib"
    write_bibtex([a, b], path)
    content = path.read_text(encoding="utf-8")
    assert "@misc{Smith.2024," in content
    assert "@misc{Jones.2024," in content
    assert "\n\n" in content


def test_write_bibtex_deduplicates(tmp_path):
    a = Article(
        author=["Smith, A"],
        title="Paper",
        year=2024,
        journal="J",
        volume=1,
        pages="1",
    )
    b = Article(
        author=["Smith, A"],
        title="Paper",
        year=2024,
        journal="J",
        volume=1,
        pages="1",
    )
    path = tmp_path / "refs.bib"
    write_bibtex([a, b], path)
    content = path.read_text(encoding="utf-8")
    assert content.count("@article{") == 1


def test_write_bibtex_resolves_collisions(tmp_path):
    a = Misc(author=["Smith, A"], title="Paper A", year=2024)
    b = Misc(author=["Smith, B"], title="Paper B", year=2024)
    path = tmp_path / "refs.bib"
    write_bibtex([a, b], path)
    content = path.read_text(encoding="utf-8")
    assert "Smith.2024.a" in content
    assert "Smith.2024.b" in content


def test_write_bibtex_empty_list(tmp_path):
    path = tmp_path / "refs.bib"
    write_bibtex([], path)
    content = path.read_text(encoding="utf-8")
    assert content == ""


def test_write_bibtex_str_path(tmp_path):
    a = Misc(author=["Smith, A"], title="Paper", year=2024)
    path = str(tmp_path / "refs.bib")
    write_bibtex([a], path)
    assert Path(path).exists()


def test_write_bibtex_missing_parent():
    with pytest.raises(FileNotFoundError):
        write_bibtex(
            [Misc(author=["Smith, A"], title="Paper", year=2024)],
            "/nonexistent/dir/refs.bib",
        )


def test_write_bibtex_utf8(tmp_path):
    a = Misc(
        author=["Müller, Hans"],
        title="Über etwas",
        year=2020,
    )
    path = tmp_path / "refs.bib"
    write_bibtex([a], path)
    content = path.read_text(encoding="utf-8")
    assert "Müller" in content
    assert "Über" in content
