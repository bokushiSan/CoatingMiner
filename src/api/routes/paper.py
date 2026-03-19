import logging
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db.models import Paper
from src.ingestion.storage import generate_paper_id, save_pdf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix='/papers', tags=['papers'])

@router.post('/upload')
def upload_pdf(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):

    paper_id = generate_paper_id()

    file_path = save_pdf(file, paper_id)

    paper = Paper(
        id=paper_id,
        source_type='pdf',
        file_path=file_path,
        status='uploaded'
    )

    db.add(paper)
    db.commit()
    db.refresh(paper)

    return {
        'paper_id': paper.id,
        'status': paper.status
    }

@router.get('/{paper_id}/status')
def get_status(
        paper_id: str,
        db: Session = Depends(get_db)
):

    paper = db.query(Paper).filter(Paper.id == paper_id).first()

    if not paper:
        return {'error': 'paper not found'}

    return {
        'paper_id': paper.id,
        'status': paper.status
    }
