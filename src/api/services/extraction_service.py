import logging
from src.db.models import Paper, ExtractedData
from src.utils.paper_processor import PaperProcessor
from src.utils.text_cleaner import TextCleaner
from src.utils.page_extractor import PageExtractor
from src.utils.section_extractor import SectionExtractor
from src.utils.doi_extractor import DOIExtractor
from src.utils.metadata_fetcher import MetadataFetcher
from src.utils.llm_extractor import LLMExtractor
# from src.entities.models import ExtractionResult, PaperMetadata

logger = logging.getLogger(__name__)


class ExtractionService:

    def __init__(self, db):
        self.db = db
        self.paper_processor = PaperProcessor(
            text_cleaner=TextCleaner(),
            page_extractor=PageExtractor(),
            section_extractor=SectionExtractor(),
        )
        self.doi_extractor = DOIExtractor()
        self.metadata_fetcher = MetadataFetcher()
        self.llm_extractor = LLMExtractor()

    def process_data(
            self,
            paper: Paper
    ):
        try:
            self._set_status(paper, 'processing')
            pages = self.paper_processor.page_extractor.extract(paper.file_path)
            doi = self.doi_extractor.extract(pages)
            metadata = self.metadata_fetcher.get_metadata(doi)
            processed_text = self.paper_processor.process(paper.file_path)
            extraction = self.llm_extractor.extract(processed_text) # здесь будет llm_extractor
            self._set_status(paper, 'extracted')
            self._save_data(paper, metadata, extraction)
            self._set_status(paper, 'completed')

        except Exception as e:
            logger.error(f'Ошибка обработки статьи {paper.id}: {e}')
            self._set_status(paper, 'failed')
            # raise

    def _save_data(self, paper, metadata, extraction):
        extracted_data = ExtractedData(
            paper_id=paper.id,
            doi=metadata.doi,
            title=metadata.title,
            authors=metadata.authors,
            year=metadata.year,
            coating_material=extraction.coating_material,
            substrate_material=extraction.substrate_material
        )
        self.db.add(extracted_data)
        self.db.commit()
        logger.info(f'ExtractedData для {paper.id} сохранена')

    def _set_status(self, paper: Paper, status: str):
        paper.status = status
        self.db.commit()
        logger.info(f'Статья {paper.id}: статус -> {status}')
