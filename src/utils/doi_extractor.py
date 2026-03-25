import re
import logging
from src.entities.models import PageText

logger = logging.getLogger(__name__)


class DOIExtractor:
    """
    Извлекает DOI из текста первых страниц PDF. Проверяет только первые N страниц.
    """

    DOI_PATTERN = re.compile(
        r'\b(?:doi[:\s]*)?(10\.\d{4,9}/[^\s,\"\'<>]+)',
        re.IGNORECASE
    )

    def __init__(self, max_pages: int = 3):
        self.max_pages = max_pages

    def extract(self, pages: list[PageText]) -> str | None:
        """


        Args:
            pages: список PageText от PageExtractor.

        Returns:
            Первый найденный DOI или None.
        """
        for page in pages[:self.max_pages]:
            match = self.DOI_PATTERN.search(page.raw_text)
            if match:
                doi = match.group(1).rstrip('.')
                logger.info(f'DOI найден на странице {page.page_num}: {doi}.')
                return doi

        logger.info('DOI не найден в тексте.')
        return None


if __name__ == '__main__':
    from src.utils.page_extractor import PageExtractor
    dex = DOIExtractor()
    pex = PageExtractor()
    # file_path = '../../tests/data/Testing_paper.pdf'
    file_path = '../../tests/data/test_paper.pdf'
    pages_data = pex.extract(file_path)
    # print(pages_data)
    print(dex.extract(pages_data))