import re


class SectionExtractor:

    def extract(self, text: str, section_patterns: list[tuple[str, str]]) -> dict[str, str]:
        """
        Выделение текста для каждого раздела.

        Args:
            text: Исходный текст.
            section_patterns: Паттерны для заданных разделов.

        Returns:
            sections: Словарь с разделами и текстами каждого раздела.
        """
        current_name = 'preamble'
        lines = text.split('\n')
        sections: dict[str, str] = {}
        current_lines: list[str] = []

        for line in lines:
            matched = self._match_section_header(line, section_patterns)
            if matched:
                if current_lines:
                    sections[current_name] = '\n'.join(current_lines).strip()
                current_name = matched
                current_lines = []
            else:
                current_lines.append(line)

        if current_lines:
            sections[current_name] = '\n'.join(current_lines).strip()

        return sections

    def _match_section_header(self, text_line: str, section_patterns: list[tuple[str, str]]) -> str | None:
        """
        Возврат имени заданного раздела.

        Args:
            text_line: Исходный текст строки.
            section_patterns: Паттерны для заданных разделов.

        Returns:
            name: Имя раздела.
        """
        stripped = text_line.strip()
        if not stripped or len(stripped) > 60:
            return None

        normalized = self._normalize_line(stripped)

        for name, pattern in section_patterns:
            if re.search(pattern, normalized, re.IGNORECASE):
                return name
        return None

    @staticmethod
    def _normalize_line(text: str) -> str:
        """
        Убираем всё, кроме букв и пробелов между словами.

        Args:
            text: Исходная строка.

        Returns:
            text: Нормализованная строка.
        """
        text = re.sub(r"[\t\n\r]", ' ', text)  # пробельные символы -> пробел
        # text = re.sub(r"\xa0", ' ', text)  # пробельные символы (\xa0) -> пробел
        text = re.sub(r"\d", '', text)  # убираем цифры-разделители
        text = text.strip()
        return text
