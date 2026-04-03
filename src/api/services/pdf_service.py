import os
import logging
from src.db.models import Paper
from src.utils.storage import generate_paper_id, save_pdf
from src.api.services.extraction_service import ExtractionService

logger = logging.getLogger(__name__)


class PDFService:
    """
    Сохранение (удаление, изменение) pdf-файла.
    """

    def __init__(self, db):
        self.db = db
        self.extraction_service = ExtractionService(db=self.db)

    def save_pdf(
            self,
            pdf_file,
            source_type: str
    ) -> Paper:
        """
        Сохранение pdf-файла из потока в файловую систему и БД.

        Args:
            pdf_file: pdf-файл.
            source_type: тип исходника (pdf, doi, url).

        Returns:
            paper: модель таблицы Paper.
        """
        paper_id = generate_paper_id()
        file_path = None

        try:
            file_path = save_pdf(pdf_file, paper_id)
            file_size = os.path.getsize(file_path)

            paper = Paper(
                id=paper_id,
                source_type=source_type,
                # source_value=None,
                file_path=file_path,
                file_size=file_size,
                status='uploaded'
            )

            self.db.add(paper)
            self.db.commit()
            self.db.refresh(paper)

            logger.info(f'Статья {paper_id} успешно сохранена')
            return paper

        except Exception as e:
            self.db.rollback()
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f'Файл {file_path} удален из-за ошибки')
            logger.error(f'Ошибка при сохранении статьи: {e}')
            raise ValueError(f'Не удалось сохранить PDF: {e}')  # TODO: Нужен кастомный класс исключения

    # def process_doi(
    #         self,
    #         doi: str
    # ):
    #     """
    #     Обработка загрузки по doi (doi -> pdf).
    #
    #     Args:
    #         doi (str): doi статьи
    #     """
    #     doi_service = DOIService()
    #     pdf_file = doi_service.get_url()
    #
    #     paper_pdf = self.save_pdf(pdf_file, source_type='doi')
    #     return paper_pdf

    def process_pdf(
            self,
            pdf_file
    ) -> Paper:
        """
        Обработка загрузки прямого pdf (pdf -> pdf).

        Args:
            pdf_file: pdf-файл.

        Returns:
            paper_pdf ():
        """
        paper_pdf = self.save_pdf(pdf_file, source_type='pdf')
        self.extraction_service.process_data(paper_pdf)
        return paper_pdf
