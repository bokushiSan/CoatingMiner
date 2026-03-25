import re
from src.utils.text_cleaner import TextCleaner
from src.utils.page_extractor import PageExtractor
from src.utils.section_extractor import SectionExtractor
from src.entities.models import ProcessedText

class PaperProcessor:
    """Обработка pdf-файла для выявления разделов статьи и текста в них."""

    DEFAULT_SECTION_NAMES = ['abstract', 'introduction', 'experimental', 'material and methods', 'results', 'conclusion']

    def __init__(
            self,
            text_cleaner: TextCleaner,
            page_extractor: PageExtractor,
            section_extractor: SectionExtractor,
            min_char: int = 100,

    ):
        self.min_char = min_char
        self.text_cleaner = text_cleaner
        self.page_extractor = page_extractor
        self.section_extractor = section_extractor

    def process(self, file_path: str, section_names: list[str] | None = None) -> ProcessedText:
        """

        Args:
            file_path: Путь к файлу.
            section_names:

        Returns:
            pr_text: Обработанный текст с разделом по секциям.
        """
        if section_names is None:
            section_names = self.DEFAULT_SECTION_NAMES
        section_patterns = self._build_section_patterns(section_names)
        pages_data = self.page_extractor.extract(file_path)
        if sum(i.char_count for i in pages_data) < self.min_char:
            raise ValueError(f'Тут поменять Exception')  #  TODO: тут менять

        raw_text = '\n'.join(t.raw_text for t in pages_data)
        clean_text = self.text_cleaner.clean(raw_text)

        sections = self.section_extractor.extract(clean_text, section_patterns)

        pr_text = ProcessedText(
            file_path=file_path,
            raw_text=raw_text,
            clean_text=clean_text,
            pages=pages_data,
            sections=sections,
        )

        return pr_text

    @staticmethod
    def _build_section_patterns(section_names: list[str]) -> list[tuple[str, str]]:
        """

        Args:
            section_names:

        Returns:
            pattern:
        """
        pattern = [
            (name, rf'\b{re.escape(name)}\b')
            for name in section_names
        ]
        return pattern


if __name__ == '__main__':
    tc = TextCleaner()
    pe = PageExtractor()
    se = SectionExtractor()
    pp = PaperProcessor(text_cleaner=tc, page_extractor=pe, section_extractor=se)
    section_names = ['Abstract', 'Introduction', 'Methodology', 'Results and discussion', 'References']
    pro = pp.process('../../tests/data/Testing_paper.pdf')

    print(pro.file_path)
    print(pro.raw_text)
    print(pro.clean_text)
    print(pro.pages)
    print(pro.sections)
    print(section_names)
    print(pro.sections.keys())
    print(pro.sections['results'])
