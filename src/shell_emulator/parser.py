"""Разбор командной строки на токены."""


class ParseError(Exception):
    """Ошибка разбора строки."""


class Parser:
    """Разбивает строку на команду и аргументы с учётом кавычек."""

    def parse(self, line: str) -> list[str]:
        """Возвращает список слов."""
        tokens = []
        current = ""
        quote = None
        for char in line:
            if quote is None:
                if char in ('"', "'"):
                    quote = char
                elif char != " ":
                    current += char
                elif current != "":
                    tokens.append(current)
                    current = ""
            elif char == quote:
                quote = None
            else:
                current += char
        if quote is not None:
            raise ParseError("syntax error: unterminated quote")
        if current != "":
            tokens.append(current)
        return tokens
