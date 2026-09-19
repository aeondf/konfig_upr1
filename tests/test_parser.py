"""Тесты парсера."""

import pytest

from shell_emulator.parser import ParseError, Parser


def test_simple_words() -> None:
    """Слова разделяются пробелами."""
    assert Parser().parse("ls -la") == ["ls", "-la"]


def test_extra_spaces() -> None:
    """Лишние пробелы не дают пустых слов."""
    assert Parser().parse("   ls    -la   ") == ["ls", "-la"]


def test_double_quotes() -> None:
    """Двойные кавычки объединяют слова с пробелом."""
    assert Parser().parse('cd "My Documents"') == ["cd", "My Documents"]


def test_single_quotes() -> None:
    """Одинарные кавычки работают так же."""
    assert Parser().parse("cd 'my dir' file") == ["cd", "my dir", "file"]


def test_quote_inside_other_quote() -> None:
    """Кавычка другого типа внутри кавычек — обычный символ."""
    assert Parser().parse('echo "it\'s ok"') == ["echo", "it's ok"]


def test_quotes_glue_to_word() -> None:
    """Кавычки внутри слова не разрывают его."""
    assert Parser().parse('a"b c"d') == ["ab cd"]


def test_empty_line() -> None:
    """Пустая строка — пустой список."""
    assert Parser().parse("") == []
    assert Parser().parse("   ") == []


def test_unterminated_quote() -> None:
    """Незакрытая кавычка — ошибка."""
    with pytest.raises(ParseError):
        Parser().parse('ls "oops')
