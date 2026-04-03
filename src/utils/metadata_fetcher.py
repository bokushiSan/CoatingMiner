import logging
from habanero import Crossref
from src.entities.models import PaperMetadata

logger = logging.getLogger(__name__)


class MetadataFetcher:
    """Извлечение метаданных статьи - DOI, Название, авторы, год."""

    def __init__(
            self
    ):
        self.cr = Crossref()

    def get_metadata(
            self,
            doi: str
    ):
        try:
            work = self.cr.works(ids=doi)
            work_data = work['message']
        except Exception as e:
            raise ValueError(f'Тут кастомное исключение {e}')  # TODO: кастомное исключение

        title = self._get_title(work_data)
        authors = self._get_authors(work_data)

        year = None  # TODO: нужно поправить get_year
        # year = self._get_year(work_data)

        paper_metadata = PaperMetadata(
            doi=doi,
            title=title,
            authors=authors,
            year=year
        )
        return paper_metadata

    @staticmethod
    def _get_title(data: dict) -> str | None:
        title = data.get('title', [])
        if title:
            return title[0]
        return None

    @staticmethod
    def _get_authors(data: dict) -> list:
        author_data = data.get('author', [])
        authors = []
        for author in author_data:
            last_name = author.get('family', '')
            initials = author.get('given', '')
            full_name = f'{last_name} {initials}'.strip()
            if full_name:
                authors.append(full_name)
        return authors

    # @staticmethod
    # def _get_year(data: dict) -> int | None:
    #     year_data = data.get('published-print', {})
    #     print(year_data)
    #     print(year_data['date-parts'][0][0])
    #     print(year_data.get(['date-parts'][0][0]))
    #     year = year_data.get(['date-parts'][0][0], None)
    #     return year
