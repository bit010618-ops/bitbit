from pathlib import Path


SOURCE = Path(__file__).with_name("merge_full_handout.py").read_text(encoding="utf-8")


def test_merge_does_not_drop_formula_or_diagram_pages_by_text_length():
    assert "extract_text" not in SOURCE
    assert "current_batch_pdfs()" in SOURCE
    assert "writer.add_page(page)" in SOURCE
    assert "for page in PdfReader(path).pages" in SOURCE
