import logging
from src.entities.models import ExtractionResult, ProcessedText, PaperMetadata

logger = logging.getLogger(__name__)


class LLMExtractor:
    """
    Заглушка LLM extraction.
    """

    def extract(self, processed_text: ProcessedText, paper_metadata: PaperMetadata) -> ExtractionResult:
        logger.info('LLMExtractor: используется заглушка, возвращается пустой результат')
        return ExtractionResult(
            coating_material='TiN',
            substrate_material='R6M5',
        )
