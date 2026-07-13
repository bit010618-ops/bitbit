from pathlib import Path

from pypdf import PdfReader

from make_dsp_sample_handout_v2 import Doc, register_fonts


def test_h1_starts_a_new_page_when_current_page_has_content(tmp_path: Path):
    register_fonts()
    output = tmp_path / "chapter-break.pdf"
    doc = Doc(output)
    doc.section = "第一章"
    doc.start()
    doc.p("上一章正文")
    doc.section = "第二章"
    doc.h1("第二章 新章标题")
    doc.save()

    reader = PdfReader(output)
    assert len(reader.pages) == 2
    assert "第二章 新章标题" not in (reader.pages[0].extract_text() or "")
    assert "第二章 新章标题" in (reader.pages[1].extract_text() or "")
