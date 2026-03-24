import re
import unicodedata


class TextCleaner:
    """
    Класс очистки исходного текста.
    """

    def clean(self, text: str) -> str:
        """
        Очистка текста по заданным правилам для выявления названий секций.
        Args:
            text: Исходный (сырой) текст.

        Returns:
            text: Очищенный текст.
        """
        text = self._normalize_unicode_chars(text)
        text = self._clean_linebreaks(text)
        text = self._clean_numbers(text)
        text = self._clean_extra_space(text)
        text = self._clean_multiple_spaces(text)
        return text

    @staticmethod
    def _normalize_unicode_chars(text: str) -> str:
        """
        Исправление артефактов кодировки шрифтов pdf: типографских лигатур и кривого маппинга символов.
        """
        replacements = {
            # '\ufb00': 'ff',
            # '\ufb01': 'fi',
            # '\ufb02': 'fl',
            # '\ufb03': 'ffi',
            # '\ufb04': 'ffl',
            # '\ufb05': 'st',
            # '\ufb06': 'st',
            '\u019f': 'ti',  # Ɵ -> ti
            '\xa0': ' ',
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text

    @staticmethod
    def _clean_linebreaks(text: str) -> str:
        """
        Удаление переносов строки.

        Args:
            text: Исходный текст.

        Returns:
            res_text: Очищенный текст.
        """
        return re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)

    @staticmethod
    def _clean_numbers(text: str) -> str:
        """
        Удаление строк, состоящих только из цифр.

        Args:
            text: Исходный текст.

        Returns:
            text: Очищенный текст.
        """
        return re.sub(r'\n\d+\n', '\n', text)

    @staticmethod
    def _clean_extra_space(text: str) -> str:
        """
        Удаление множественных пробелов и табуляций на один пробел.

        Args:
            text: Исходный текст.

        Returns:
            Очищенный текст.
        """
        return re.sub(r'[ \t]+', ' ', text)

    @staticmethod
    def _clean_multiple_spaces(text: str) -> str:
        """
        Удаление множественных пустых строк (2+ пустые строки в одну).

        Args:
            text: Исходный текст.

        Returns:
            Очищенный текст.
        """
        return re.sub(r'\n{3,}', '\n\n', text)
