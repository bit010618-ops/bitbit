from pathlib import Path

from pypdf import PdfReader

import make_dsp_batch_046_088 as batch3
import make_dsp_batch_089_112 as batch4
import make_dsp_batch_141_184 as batch6


def test_chapter_end_sections_do_not_create_orphan_pages():
    expected_pages = {
        batch3.PDF_PATH: 8,
        batch4.PDF_PATH: 6,
        batch6.PDF_PATH: 8,
    }

    actual_pages = {
        path: len(PdfReader(str(path)).pages)
        for path in expected_pages
    }

    assert actual_pages == expected_pages


def test_compacted_chapter_ends_keep_their_final_content():
    source_expectations = {
        Path(batch3.__file__): ["本章导图与课后题", "按原课件课后题继续练习"],
        Path(batch4.__file__): ["系统的频率响应：正弦稳态", "正弦稳态响应"],
        Path(batch6.__file__): ["课后习题", "3-23 DFT 和 DTFT 的关系"],
    }

    for source_path, required_text in source_expectations.items():
        source = source_path.read_text(encoding="utf-8")
        for text in required_text:
            assert text in source
