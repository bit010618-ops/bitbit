"""Regression checks for the assembled DSP handout PDF."""

from pathlib import Path
import re
import unittest

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
FINAL_PDF = ROOT / 'outputs' / '华理814DSP讲义_完整彩色A4版.pdf'


def page_content_bytes(page):
    contents = page.get_contents()
    if contents is None:
        return 0
    streams = contents if isinstance(contents, list) else [contents]
    return sum(len(stream.get_data()) for stream in streams)


def page_chapter_number(page):
    text = page.extract_text() or ''
    match = re.search(r'(?m)^(\d+)\.\s', text)
    return int(match.group(1)) if match else None


def is_allowed_chapter_end(page_number, pages):
    if page_number >= len(pages):
        return False
    current = page_chapter_number(pages[page_number - 1])
    following = page_chapter_number(pages[page_number])
    return current is not None and following is not None and current != following


class HandoutRegressionTests(unittest.TestCase):
    def test_final_handout_has_no_near_blank_pages(self):
        reader = PdfReader(str(FINAL_PDF))
        near_blank = [
            number
            for number, page in enumerate(reader.pages[2:], start=3)
            # A full-page vector diagram may contain little extractable text.
            # Treat a page as near blank only when both text and drawing stream
            # are sparse, so source-faithful FFT/IIR/FIR diagrams are retained.
            if (
                len((page.extract_text() or '').strip()) < 100
                and page_content_bytes(page) < 5000
                and not is_allowed_chapter_end(number, reader.pages)
            )
        ]
        self.assertEqual(near_blank, [], f'Near-blank pages found: {near_blank}')

    def test_final_handout_starts_with_cover_then_directory(self):
        reader = PdfReader(str(FINAL_PDF))
        cover = reader.pages[0].extract_text() or ''
        directory = reader.pages[1].extract_text() or ''
        self.assertIn('华理814 DSP讲义', cover)
        self.assertNotIn('目录', cover)
        self.assertIn('目录', directory)

    def test_extracted_text_stays_inside_every_page(self):
        violations = []
        with pdfplumber.open(FINAL_PDF) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                for word in page.extract_words():
                    if (
                        word['x0'] < -1
                        or word['x1'] > page.width + 1
                        or word['top'] < -1
                        or word['bottom'] > page.height + 1
                    ):
                        violations.append((page_number, word['text']))
        self.assertEqual(violations, [], f'Text outside page bounds: {violations[:20]}')

    def test_embedded_images_stay_inside_every_page(self):
        violations = []
        with pdfplumber.open(FINAL_PDF) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                for image in page.images:
                    if (
                        image['x0'] < -1
                        or image['x1'] > page.width + 1
                        or image['y0'] < -1
                        or image['y1'] > page.height + 1
                    ):
                        violations.append((page_number, image.get('name', 'image')))
        self.assertEqual(violations, [], f'Images outside page bounds: {violations[:20]}')


if __name__ == '__main__':
    unittest.main()
