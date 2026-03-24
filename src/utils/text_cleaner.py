import re


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
        text = self._clean_linebreaks(text)
        text = self._clean_numbers(text)
        text = self._clean_extra_space(text)
        text = self._clean_multiple_spaces(text)
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

if __name__ == '__main__':
    tc = TextCleaner()
    print(tc.clean('2. Materials and \n\n\n\n\n\n\n\n\nmethods'))