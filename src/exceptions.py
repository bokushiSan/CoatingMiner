class CoatingMinerError(Exception):
    """Базовое исключение проекта."""
    pass


class FileNotPDFError(CoatingMinerError):
    """Загруженный файл не является .pdf-файлом."""
    pass


# class FileTooLargeError(CoatingMinerError):
#     def __init__(self, file_size, limit_size):
#         pass
