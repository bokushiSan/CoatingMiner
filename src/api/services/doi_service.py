import requests
from habanero import Crossref
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cr = Crossref()

class DOIService:  # TODO: пока в заморозке

    def __init__(self):
        pass

    def _get_pdf_url(self, doi) -> str:
        try:
            work = cr.works(ids=doi)
            logger.info(f'Получение списков')  # TODO: Тут поправить
            links = work['message'].get('link', [])

            if len(links) > 0:
                for l in links:
                    content_type = l.get('content-type', None)
                    if content_type == 'application/pdf':
                        url = l.get('URL', None)
                        if url:
                            return url

            else:
                return None  # TODO: тут надо подумать

        except Exception as e:
            pass  # TODO: тут надо подумать


# Этот роут в src/api/routes/paper.py после реализации doi -> pdf.
# @router.post('/upload_by_doi')
# def upload_by_doi(
#         doi,
#         db: Session = Depends(get_db)
# ):
#
#     try:
#         pdf_service = PDFService(db)
#         paper = pdf_service.process_doi(doi)
#
#         return {
#             'paper_id': paper.id,
#             'source_type': paper.source_type,
#             'file_path': paper.file_path,
#             'status': paper.status,
#         }
#     except Exception as e:
#         logger.info(f'Статья не добавлена: {e}')
#
# if __name__ == '__main__':
#     ds = DOIService()
#     url = ds._get_pdf_url('doi:10.1088/1742-6596/1393/1/012148')
#     print(url)