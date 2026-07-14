from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
from pathlib import Path
import sys

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "work"
OUTPUT = ROOT / "outputs" / "华理814DSP讲义_完整彩色A4版.pdf"
sys.path.insert(0, str(WORK))

BATCH_SCRIPTS = [
    "make_dsp_sample_handout_v2.py",
    "make_dsp_batch_016_024.py",
    "make_dsp_batch_046_088.py",
    "make_dsp_batch_089_112.py",
    "make_dsp_batch_115_140.py",
    "make_dsp_batch_141_184.py",
    "make_dsp_batch_185_227.py",
    "make_dsp_batch_228_265_redraw.py",
    "make_dsp_batch_266_300_redraw.py",
    "make_dsp_batch_301_332_redraw.py",
    "make_dsp_batch_333_366_redraw.py",
    "make_dsp_batch_367_399_redraw.py",
    "make_dsp_batch_400_436_redraw.py",
]


def current_batch_pdfs() -> list[Path]:
    paths: list[Path] = []
    for index, filename in enumerate(BATCH_SCRIPTS, 1):
        script = WORK / filename
        spec = spec_from_file_location(f"dsp_batch_{index}", script)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"无法加载生成脚本：{script}")
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        path = Path(module.PDF_PATH)
        if not path.exists():
            raise FileNotFoundError(path)
        paths.append(path)
    return paths


def make_cover() -> object:
    packet = BytesIO()
    width, height = A4
    c = canvas.Canvas(packet, pagesize=A4)
    ink = colors.HexColor("#20252B")
    rule = colors.HexColor("#A7AAAD")
    c.setFillColor(colors.white)
    c.rect(0, 0, width, height, stroke=0, fill=1)
    c.setStrokeColor(rule)
    c.setLineWidth(0.7)
    c.line(70, height - 176, width - 70, height - 176)
    c.setFillColor(ink)
    c.setFont("CNB", 30)
    c.drawCentredString(width / 2, height - 250, "华理814 DSP讲义")
    c.setFont("CN", 17)
    c.drawCentredString(width / 2, height - 292, "数字信号处理")
    c.setStrokeColor(rule)
    c.line(150, height - 320, width - 150, height - 320)
    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


def make_directory(chapter_starts: list[int]) -> object:
    packet = BytesIO()
    width, height = A4
    c = canvas.Canvas(packet, pagesize=A4)
    c.setFillColor(colors.white)
    c.rect(0, 0, width, height, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#303438"))
    c.setFont("CN", 9.2)
    c.drawString(42, height - 23, "华理814DSP讲义")
    c.drawRightString(width - 42, height - 23, "目录")
    c.setStrokeColor(colors.HexColor("#8B8F93"))
    c.setLineWidth(0.55)
    c.line(42, height - 31, width - 42, height - 31)
    c.setFillColor(colors.HexColor("#20252B"))
    c.setFont("CNB", 25)
    c.drawString(52, height - 91, "目录")
    c.setStrokeColor(colors.HexColor("#777B7F"))
    c.setLineWidth(0.8)
    c.line(52, height - 101, 118, height - 101)

    entries = [
        "第一章  时域离散信号和系统",
        "第二章  时域离散信号和系统的频域分析",
        "第三章  离散傅里叶变换 DFT",
        "第四章  快速傅里叶变换 FFT",
        "第五章  IIR 系统网络结构与滤波器设计",
        "第六章  FIR 系统网络结构与滤波器设计",
        "第七章  多采样率数字信号处理",
    ]
    y = height - 150
    for label, page_number in zip(entries, chapter_starts):
        c.setFillColor(colors.HexColor("#1F2937"))
        c.setFont("CN", 12)
        c.drawString(58, y, label)
        label_width = c.stringWidth(label, "CN", 12)
        c.setStrokeColor(colors.HexColor("#B8B8B8"))
        c.setDash(1.5, 2.5)
        c.line(64 + label_width, y + 2, width - 75, y + 2)
        c.setDash()
        c.setFillColor(colors.HexColor("#303438"))
        c.setFont("CN", 11)
        c.drawRightString(width - 58, y, str(page_number))
        y -= 46
    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


def page_number_overlay(width: float, height: float, number: int) -> object:
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.setFillColor(colors.white)
    c.rect(width / 2 - 31, 12, 62, 24, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#6B7280"))
    c.setFont("CN", 8.2)
    c.drawCentredString(width / 2, 27, str(number))
    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


def build() -> Path:
    from make_dsp_sample_handout_v2 import register_fonts

    register_fonts()
    pdfs = current_batch_pdfs()
    counts = [len(PdfReader(path).pages) for path in pdfs]

    # Displayed page 1 is the directory.  The first content page is page 2.
    batch_starts: list[int] = []
    cursor = 2
    for count in counts:
        batch_starts.append(cursor)
        cursor += count
    chapter_starts = [
        batch_starts[0],
        batch_starts[2],
        batch_starts[5],
        batch_starts[7],
        batch_starts[8],
        batch_starts[10],
        batch_starts[12],
    ]

    writer = PdfWriter()
    for path in pdfs:
        for page in PdfReader(path).pages:
            writer.add_page(page)
    writer.insert_page(make_cover(), 0)
    starts = chapter_starts
    writer.insert_page(make_directory(starts), 1)

    for physical_index, page in enumerate(writer.pages):
        if physical_index == 0:
            continue
        printed_page = physical_index
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        page.merge_page(page_number_overlay(width, height, printed_page))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("wb") as handle:
        writer.write(handle)
    print(OUTPUT)
    print("pages", len(writer.pages))
    return OUTPUT


if __name__ == "__main__":
    build()
