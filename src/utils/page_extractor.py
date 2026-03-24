import fitz
from src.entities.models import PageText

class PageExtractor:

    def extract(self, file_path: str) -> list[PageText]:
        """
        Выделение текста для каждой страницы.

        Args:
            file_path: Путь к файлу.

        Returns:
            pages_data: Список страниц с текстом.
        """
        pages_data = []
        try:
            with fitz.open(file_path) as doc:
                for idx, page in enumerate(doc):
                    page_text = page.get_text()
                    page_text = self.replace_bug_symbols(page_text)
                    pages_data.append(
                        PageText(
                            page_num=idx + 1,
                            raw_text=page_text,
                            char_count=len(page_text)
                        )
                    )
        except Exception as e:
            raise RuntimeError(f'Здесь поправить еррор {e}')
        return pages_data

    @staticmethod
    def replace_bug_symbols(text: str) -> str:
        """
        Замена лигатур из-за неправильного определения текста.

        Args:
            text: Исходный текст.

        Returns:
            text: Исправленный текст
        """
        replacements = {
            '\xa0': ' ',
            # 'Ɵ': 'ti',
            # 'ﬁ': 'fi',
            # 'ﬂ': 'fl',
            # 'ﬀ': 'ff'
        }

        for wrong, correct in replacements.items():
            text = text.replace(wrong, correct)
        return text

if __name__ == '__main__':
    pe = PageExtractor()
    pe.extract()