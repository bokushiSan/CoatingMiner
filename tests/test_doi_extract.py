import pytest
from src.utils.doi_extractor import DOIExtractor
from src.entities.models import PageText


@pytest.mark.parametrize(
    'raw_text_doi',
    [
        'doi:10.1016/j.surfcoat.2020.125657',
        'DOI:10.1016/j.surfcoat.2020.125657',
        'Doi:10.1016/j.surfcoat.2020.125657',
        'doi 10.1016/j.surfcoat.2020.125657',
        'https://doi.org/10.1016/j.surfcoat.2020.125657',
        '10.1016/j.surfcoat.2020.125657',
        'Какой-то текст до doi: 10.1016/j.surfcoat.2020.125657',
        'doi: 10.1016/j.surfcoat.2020.125657, какой-то текст после',
        'Текст до, doi: 10.1016/j.surfcoat.2020.125657, текст после'
    ],
)
def test_extract_doi_formats(raw_text_doi: str):
    pages = [
        PageText(
            page_num=1,
            raw_text=raw_text_doi
        )
    ]
    extractor = DOIExtractor()
    result = extractor.extract(pages)
    expected = '10.1016/j.surfcoat.2020.125657'
    assert result == expected

@pytest.mark.parametrize(
    'raw_text_doi',
    [
        '',
        ' ',
        'Текст без DOI',
        'doi:',
        '10.abc/xyz"'
        'doi:abc/123',
        '10.1016',
    ],
)
def test_extract_invalid_doi(raw_text_doi: str):
    pages = [
        PageText(
            page_num=1,
            raw_text=raw_text_doi
        )
    ]
    extractor = DOIExtractor()
    result = extractor.extract(pages)
    assert result is None

@pytest.mark.parametrize(
    'max_pages, expected',
    [
        (1, None),
        (2, '10.1000/test'),
        (3, '10.1000/test'),
        (4, '10.1000/test'),
        (-1, None),
        (0, None)
    ],
)
def test_extract_max_pages(max_pages: int, expected: str):
    pages = [
        PageText(page_num=1, raw_text='no doi'),
        PageText(page_num=2, raw_text='doi:10.1000/test'),
        PageText(page_num=3, raw_text='doi:10.2000/another'),
    ]
    extractor = DOIExtractor(max_pages=max_pages)
    result = extractor.extract(pages)
    assert result == expected

@pytest.mark.parametrize(
    'max_pages',
    [
        0,
        -1,
        -10
    ]
)
def test_extract_invalid_max_pages(max_pages: int):
    pages = [
        PageText(page_num=1, raw_text='doi:10.1000/test')
    ]
    extractor = DOIExtractor(max_pages=max_pages)
    result = extractor.extract(pages)
    assert result is None


if __name__ == '__main__':
    test_extract_doi_formats()
    test_extract_invalid_doi()
    test_extract_max_pages()
    test_extract_invalid_max_pages()