import logging
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from src.api.services.pdf_service import PDFService
from src.db.database import get_db
from src.db.models import Paper, ExtractedData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix='/papers', tags=['papers'])

@router.post('/upload_by_pdf')
def upload_by_pdf(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    try:
        pdf_service = PDFService(db)
        paper = pdf_service.process_pdf(file)

        return {
            'paper_id': paper.id,
            'source_type': paper.source_type,
            'file_path': paper.file_path,
            'status': paper.status,
        }
    except Exception as e:
        logger.error(f'Статья не добавлена: {e}')
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/{paper_id}/status')
def get_status(
        paper_id: str,
        db: Session = Depends(get_db)
):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()

    if not paper:
        logger.error(f'Тут ошибка.')  # TODO: тут поправить
        raise HTTPException(status_code=404, detail='Paper not found')

    return {
        'paper_id': paper.id,
        'status': paper.status
    }
