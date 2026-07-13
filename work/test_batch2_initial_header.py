from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_batch_016_024.py").read_text(encoding="utf-8")


def test_first_page_header_matches_chapter_three_content():
    start = SCRIPT.index("doc = BatchDoc(PDF_PATH)")
    first_page = SCRIPT[start:SCRIPT.index("doc.h1", start)]
    assert 'doc.section = "3. 时域离散系统"' in first_page
    assert 'doc.section = "2. 时域离散信号"' not in first_page
