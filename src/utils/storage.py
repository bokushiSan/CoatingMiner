import os
import uuid
from pathlib import Path

STORAGE_PATH = os.getenv('STORAGE_PATH', 'data/raw_papers')

def generate_paper_id() -> uuid.UUID:
    """
    Генерация уникального id для статьи.

    Returns:
        paper_id: Уникальный UUID4 идентификатор в виде строки.
    """
    paper_id = uuid.uuid4()
    return paper_id

def save_pdf(pdf_file, paper_id: uuid.UUID) -> str:
    """
    Сохранение pdf-файла в хранилище под сгенерированным id статьи.

    Args:
        pdf_file: Объект загруженного файла, который должен иметь метод `file.read()` для чтения содержимого.
        paper_id: Уникальный идентификатор статьи, который будет использован в имени сохраняемого файла.

    Returns:
        file_path: Полный путь к сохраненному файлу.
    """
    Path(STORAGE_PATH).mkdir(parents=True, exist_ok=True)

    file_path = os.path.join(STORAGE_PATH, f"{paper_id}.pdf")

    with open(file_path, "wb") as buffer:
        buffer.write(pdf_file.file.read())

    return file_path