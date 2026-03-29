import logging
import re
from src.entities.models import PageText

logger = logging.getLogger(__name__)


class DOIExtractor:
    """Извлечение DOI из текста первых N страниц pdf-файла статьи."""

    DOI_PATTERN = re.compile(
        r'\b(?:doi[:\s]*)?(10\.\d{4,9}/[^\s,\"\'<>]+)',
        re.IGNORECASE
    )

    def __init__(
            self,
            max_pages: int = 3
    ):
        """
        Args:
            max_pages: Количество страниц для поиска DOI.
        """
        self.max_pages = max_pages

    def extract(
            self,
            pages: list[PageText]
    ) -> str | None:
        """
        Извлечение DOI из первых max_page страниц pdf-файла.

        Args:
            pages: список PageText от PageExtractor.

        Returns:
            Первый найденный DOI или None.
        """
        if self.max_pages <= 0:
            logger.warning('Количество страниц должно быть положительно.')
            return None

        for page in pages[:self.max_pages]:
            match = self.DOI_PATTERN.search(page.raw_text)
            if match:
                doi = match.group(1).rstrip('.')
                logger.info(f'DOI найден на странице {page.page_num}: {doi}.')
                return doi

        logger.info('DOI не найден в тексте.')
        return None
