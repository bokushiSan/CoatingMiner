import os
import uuid
from pathlib import Path

STORAGE_PATH = os.getenv('STORAGE_PATH', 'data/raw_papers')

def generate_paper_id() -> str:
    """
    Генерация уникального id для статьи.

    Returns:
        paper_id (str): Уникальный UUID4 идентификатор в виде строки.
    """
    paper_id = str(uuid.uuid4())
    return paper_id

def save_pdf(file, paper_id: str) -> str:
    """
    Сохранение pdf-файла в хранилище под сгенерированным id статьи.

    Args:
        file: Объект загруженного файла, который должен иметь метод `file.read()` для чтения содержимого.
        paper_id (str): Уникальный идентификатор статьи, который будет использован в имени сохраняемого файла.

    Returns:
        file_path (str): Полный путь к сохраненному файлу.
    """

    Path(STORAGE_PATH).mkdir(parents=True, exist_ok=True)

    file_path = os.path.join(STORAGE_PATH, f"{paper_id}.pdf")

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path