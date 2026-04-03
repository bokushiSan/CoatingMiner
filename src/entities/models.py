from pydantic import BaseModel
from typing import Optional

class PageText(BaseModel):
    page_num: int
    raw_text: str

class ProcessedText(BaseModel):
    file_path: str
    raw_text: str
    clean_text: str
    pages: list[PageText]
    sections: dict[str, str] = {}

class PaperMetadata(BaseModel):
    doi: Optional[str] = None
    title: Optional[str] = None
    authors: Optional[list[str]] = []
    year: Optional[int] = None

class ExtractionResult(BaseModel):
    coating_material: Optional[str] = None
    substrate_material: Optional[str] = None