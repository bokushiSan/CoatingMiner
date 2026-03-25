from pydantic import BaseModel
from typing import Optional

class PageText(BaseModel):
    page_num: int
    raw_text: str
    char_count: int

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
