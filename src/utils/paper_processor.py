import re
from src.utils.text_cleaner import TextCleaner
from src.utils.page_extractor import PageExtractor
from src.utils.section_extractor import SectionExtractor
from src.entities.models import ProcessedText

class PaperProcessor:
    """Обработка pdf-файла для выявления разделов статьи и текста в них."""

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
        if section_names is None:
            section_names = ['abstract', 'introduction', 'experimental', 'material and methods', 'results', 'conclusion']
        section_patterns = self._build_section_patterns(section_names)
        pages_data = self.page_extractor.extract(file_path)
        if sum(i.char_count for i in pages_data) < self.min_char:
            raise ValueError(f'Тут поменять Exception')

        raw_text = '\n'.join(t.raw_text for t in pages_data)
        clean_text = self.text_cleaner.clean(raw_text)

        sections = self.section_extractor.extract(clean_text, section_patterns)

        return ProcessedText(
            file_path=file_path,
            raw_text=raw_text,
            clean_text=clean_text,
            sections=sections,
        )

    @staticmethod
    def _build_section_patterns(section_names: list[str]) -> list[tuple[str, str]]:
        return [
            (name, rf'\b{re.escape(name)}\b')
            for name in section_names
        ]




# if __name__ == '__main__':
#     # print(os.listdir('../../tests/data'))
#     tcl = TextCleaner()
#     pex = PageExtractor()
#     sex = SectionExtractor()
#     pp = PaperProcessor(text_cleaner=tcl, page_extractor=pex, section_extractor=sex)
#     pr = pp.process(file_path='../../tests/data/test_paper.pdf')
#     # print("\n".join(pr.sections))
#     print(pr.sections.keys())