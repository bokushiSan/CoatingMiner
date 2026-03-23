import os
import fitz
import re
from dataclasses import dataclass, field

@dataclass
class PageText:
    page_num: int
    raw_text: str
    char_count: int


@dataclass
class ProcessedText:
    file_path: str
    raw_text: str
    clean_text: str
    sections: dict[str, str] = field(default_factory=dict)


class PaperProcessor:

    def __init__(self, min_char: int = 100, ):
        self.min_char = min_char


    def process(self, file_path, section_names: list[str] = ['abstract', 'introduction', 'experimental', 'results', 'conclusion']):
        section_names = section_names
        section_patterns = self._build_section_patterns(section_names)
        pages_data = self._extract_pages(file_path)
        if sum([i.char_count for i in pages_data]) < self.min_char:
            raise ValueError(f'Тут поменять Exception')

        raw_text = '\n'.join(t.raw_text for t in pages_data)
        clean_text = self._clean_text(raw_text)

        prtxt = ProcessedText(file_path=file_path, raw_text=raw_text, clean_text=clean_text)
        sections = self._extract_sections(clean_text, section_patterns)

        return ProcessedText(
            file_path=file_path,
            raw_text=raw_text,
            clean_text=clean_text,
            sections=sections,
        )

    def _build_section_patterns(self, section_names) -> list:
        return [
            (name, rf'\b{re.escape(name)}\b')
            for name in section_names
        ]

    def _extract_pages(self, file_path) -> list:
        """
        """
        all_pages_data = []
        doc = fitz.open(file_path)
        for idx, page in enumerate(doc):
            pagetext = page.get_text()
            pt = PageText(
                page_num=idx + 1,
                raw_text=pagetext,
                char_count=len(pagetext)
            )
            all_pages_data.append(pt)
        doc.close()
        return all_pages_data

    def _clean_text(self, text: str) -> str:
        """
        """
        text = re.sub(r'-\n(\w)', r'\1', text)  # удаление переносов: 'Т-\nекст' -> 'Текст'
        text = re.sub(r'\n\d+\n', '\n',
                      text)  # удаление строк, состоящих только из цифр: 'Текст\n88\nТекст' -> 'Текст\nТекст'
        text = re.sub(r'\n{3,}', '\n\n', text)  # удаление множественных пустых строк (2+ пустые строки в одну): 'Текст\n\n\n\n\nТекст' -> 'Текст\n\nТекст'
        return text

    def _extract_sections(self, clean_text, section_patterns):
        lines = clean_text.split('\n')
        sections: dict[str, str] = {}
        current_name = 'preamble'
        current_lines: list[str] = []

        for line in lines:
            matched = self._match_section_header(line, section_patterns)
            if matched:
                if current_lines:
                    sections[current_name] = '\n'.join(current_lines).strip()
                current_name = matched
                current_lines = []
            else:
                current_lines.append(line)

            if current_lines:
                sections[current_name] = '\n'.join(current_lines).strip()

        return sections

    def _match_section_header(self, textline: str, section_patterns) -> str | None:
        """
        """
        stripped = textline.strip()
        if not stripped or len(stripped) > 60:
            return None

        normalized = self._normalize_line(stripped)

        for name, pattern in section_patterns:
            if re.search(pattern, normalized, re.IGNORECASE):
                return name
        return None

    def _normalize_line(self, text: str) -> str:
        """
        Убираем всё, кроме букв и пробелов между словами
        """
        text = re.sub(r'[\t\n\r]', ' ', text)  # пробельные символы -> пробел
        text = re.sub(r'\d', '', text)  # убираем цифры-разделители
        text = re.sub(r'(?<!\s)\s(?=\S)', '', text)  # "T E X T" -> "TEXT"
        return text.strip()


if __name__ == '__main__':
    # print(os.listdir('../../tests/data'))
    pp = PaperProcessor()
    pr = pp.process(file_path='../../tests/data/test_paper.pdf')
    # print("\n".join(pr.sections))
    print(pr.sections.keys())