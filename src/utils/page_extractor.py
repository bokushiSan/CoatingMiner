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
                    pages_data.append(
                        PageText(
                            page_num=idx + 1,
                            raw_text=page_text
                        )
                    )
        except Exception as e:
            raise RuntimeError(f'Здесь поправить еррор {e}')
        return pages_data
