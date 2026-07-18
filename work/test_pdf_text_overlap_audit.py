from pathlib import Path
import sys

from reportlab.pdfgen import canvas


WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(WORK))

from audit_pdf_text_overlap import find_text_overlaps


def _pdf(path, baselines):
    c = canvas.Canvas(str(path), pagesize=(300, 300))
    c.setFont("Helvetica", 10)
    for index, baseline in enumerate(baselines):
        c.drawString(40, baseline, f"body line {index}")
    c.save()


def test_detects_two_body_lines_that_visibly_overlap(tmp_path):
    path = tmp_path / "overlap.pdf"
    _pdf(path, [240, 245])
    findings = find_text_overlaps(path)
    assert len(findings) == 1
    assert findings[0]["page"] == 1


def test_allows_normal_body_line_spacing(tmp_path):
    path = tmp_path / "clear.pdf"
    _pdf(path, [240, 224])
    assert find_text_overlaps(path) == []
