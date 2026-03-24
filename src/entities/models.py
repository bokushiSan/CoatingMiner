from pydantic import BaseModel

class PageText(BaseModel):
    page_num: int
    raw_text: str
    char_count: int


class ProcessedText(BaseModel):
    file_path: str
    raw_text: str
    clean_text: str
    sections: dict[str, str] = {}