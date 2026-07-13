from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter, Transformation
from pypdf._page import PageObject
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas


SOURCE = Path(r"C:\Users\HP\Desktop\DPS课件\DSP课件.pdf")
OUTPUT = Path(r"C:\Users\HP\Documents\Codex\2026-07-01\zh\outputs\DSP课件_A4讲义版.pdf")

A4_WIDTH = 595.276
A4_HEIGHT = 841.89

LEFT = 28.0
RIGHT = 28.0
TOP = 36.0
BOTTOM = 34.0
GAP = 18.0


def add_page_chrome(page: PageObject, page_no: int, total_pages: int) -> None:
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(A4_WIDTH, A4_HEIGHT))
    c.setStrokeColor(HexColor("#d4d4d4"))
    c.setLineWidth(0.45)
    c.line(LEFT, A4_HEIGHT - TOP + 11, A4_WIDTH - RIGHT, A4_HEIGHT - TOP + 11)
    c.line(LEFT, BOTTOM - 11, A4_WIDTH - RIGHT, BOTTOM - 11)
    c.setFillColor(HexColor("#555555"))
    c.setFont("Helvetica", 8)
    c.drawCentredString(A4_WIDTH / 2, 14, f"{page_no} / {total_pages}")
    c.save()
    packet.seek(0)
    overlay = PdfReader(packet).pages[0]
    page.merge_page(overlay)


def merge_slide(target: PageObject, source_page: PageObject, slot_index: int) -> None:
    src_w = float(source_page.mediabox.width)
    src_h = float(source_page.mediabox.height)
    slot_w = A4_WIDTH - LEFT - RIGHT
    slot_h = (A4_HEIGHT - TOP - BOTTOM - GAP) / 2
    scale = min(slot_w / src_w, slot_h / src_h)
    out_w = src_w * scale
    out_h = src_h * scale
    x = LEFT + (slot_w - out_w) / 2
    if slot_index == 0:
        y = A4_HEIGHT - TOP - out_h
    else:
        y = BOTTOM
    transform = Transformation().scale(scale).translate(x, y)
    target.merge_transformed_page(source_page, transform)


def main() -> None:
    reader = PdfReader(str(SOURCE))
    writer = PdfWriter()
    total_out = (len(reader.pages) + 1) // 2

    for out_index, start in enumerate(range(0, len(reader.pages), 2), start=1):
        page = PageObject.create_blank_page(width=A4_WIDTH, height=A4_HEIGHT)
        merge_slide(page, reader.pages[start], 0)
        if start + 1 < len(reader.pages):
            merge_slide(page, reader.pages[start + 1], 1)
        add_page_chrome(page, out_index, total_out)
        writer.add_page(page)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("wb") as f:
        writer.write(f)

    print(OUTPUT)
    print(f"source_pages={len(reader.pages)} output_pages={total_out}")


if __name__ == "__main__":
    main()
