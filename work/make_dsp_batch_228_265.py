from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from PIL import Image

from make_dsp_sample_handout_v2 import (
    BLUE,
    BLUE_DARK,
    CONTENT_W,
    MARGIN_X,
    OUT_DIR,
    TEXT,
    formula_png,
    register_fonts,
    normalize_display_formula_height,
    wrap,
)
from make_dsp_batch_016_024 import BatchDoc, draw_formula
from make_dsp_batch_046_088 import draw_red_text


PDF_PATH = OUT_DIR / "DSP讲义重制_第八批_原PPT228-265页_FFT_内容版.pdf"
NOTE_PATH = OUT_DIR / "DSP讲义重制_第八批_原PPT228-265页_FFT_校对记录.md"


FIG_DIR = Path("work/figures/source_crops_fft")


def f(name, expr, size=14, color="#111111"):
    return formula_png(f"b228_{name}", expr, size, color=color)


def img_size(path):
    im = Image.open(path)
    return im.size


def draw_formula_center(doc, path, max_w=None, max_h=36, gap=10):
    draw_formula(doc, path, max_w=max_w, max_h=max_h, gap=gap)


def draw_source_figure(doc, filename, max_h=220, gap=12, max_w=None):
    path = FIG_DIR / filename
    doc.ensure(max_h + gap + 8)
    c = doc.c
    iw, ih = img_size(path)
    max_w = max_w or CONTENT_W
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    x = MARGIN_X + (CONTENT_W - dw) / 2
    c.drawImage(ImageReader(str(path)), x, doc.y - dh, dw, dh, mask="auto")
    doc.y -= dh + gap


def draw_formula_left(doc, path, max_w=None, max_h=36, gap=9, x_offset=0):
    max_h = normalize_display_formula_height(max_h)
    doc.ensure(max_h + gap)
    c = doc.c
    iw, ih = img_size(path)
    max_w = max_w or CONTENT_W * 0.94
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(path)), MARGIN_X + x_offset, doc.y - dh, dw, dh, mask="auto")
    doc.y -= dh + gap


def draw_formula_at(c, expr, name, x, y, max_w=80, max_h=16, size=8.5, color="#111111", bg=False):
    path = f(name, expr, size, color=color)
    iw, ih = img_size(path)
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    if bg:
        c.setFillColor(colors.white)
        c.rect(x - 1.5, y - 1.0, dw + 3, dh + 2, stroke=0, fill=1)
        c.setFillColor(TEXT)
    c.drawImage(ImageReader(str(path)), x, y, dw, dh, mask="auto")
    return dw, dh


def draw_label_formula(doc, label, path, max_h=30, gap=9):
    max_h = normalize_display_formula_height(max_h)
    doc.ensure(max_h + 18)
    c = doc.c
    c.setFont("CNB", 9.8)
    c.setFillColor(BLUE_DARK)
    c.drawString(MARGIN_X, doc.y - 15, label)
    iw, ih = img_size(path)
    scale = min((CONTENT_W - 118) / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(path)), MARGIN_X + 112, doc.y - dh - 2, dw, dh, mask="auto")
    doc.y -= max(max_h, dh + 4) + gap
    c.setFillColor(TEXT)


def draw_formula_list(doc, items, max_h=30):
    for item in items:
        if len(item) == 3:
            label, path, row_h = item
        else:
            label, path = item
            row_h = max_h
        draw_label_formula(doc, label, path, max_h=row_h)


def draw_bullet_list(doc, items, font_size=9.2, gap=5):
    c = doc.c
    for item in items:
        lines = wrap(item, CONTENT_W - 20, "CN", font_size)
        h = len(lines) * (font_size + 4) + gap
        doc.ensure(h + 4)
        c.setFillColor(BLUE)
        c.circle(MARGIN_X + 4, doc.y - font_size, 2.2, stroke=0, fill=1)
        c.setFillColor(TEXT)
        c.setFont("CN", font_size)
        yy = doc.y - font_size - 3
        for line in lines:
            c.drawString(MARGIN_X + 18, yy, line)
            yy -= font_size + 4
        doc.y -= h


def draw_note_box(doc, title, lines, red_title=False):
    wrapped = []
    total = 0
    for line in lines:
        ws = wrap(line, CONTENT_W - 24, "CN", 9.1)
        wrapped.append(ws)
        total += len(ws)
    h = 30 + total * 14 + 10
    doc.ensure(h + 10)
    c = doc.c
    y = doc.y - h
    c.setStrokeColor(colors.HexColor("#A5D4FF"))
    c.setFillColor(colors.HexColor("#F3FAFF"))
    c.roundRect(MARGIN_X, y, CONTENT_W, h, 4, stroke=1, fill=1)
    c.setFont("CNB", 9.8)
    c.setFillColor(colors.HexColor("#D71920") if red_title else BLUE_DARK)
    c.drawString(MARGIN_X + 12, y + h - 20, title)
    c.setFont("CN", 9.1)
    c.setFillColor(TEXT)
    yy = y + h - 39
    for ws in wrapped:
        for line in ws:
            c.drawString(MARGIN_X + 12, yy, line)
            yy -= 14
    doc.y = y - 12


def draw_small_table(doc, headers, rows, col_widths=None, font_size=9.0, row_h=25):
    col_widths = col_widths or [CONTENT_W / len(headers)] * len(headers)
    h = row_h * (len(rows) + 1)
    doc.ensure(h + 12)
    c = doc.c
    x0 = MARGIN_X
    y = doc.y - row_h
    c.setFillColor(BLUE_DARK)
    c.rect(x0, y, sum(col_widths), row_h, stroke=0, fill=1)
    c.setFont("CNB", font_size)
    c.setFillColor(colors.white)
    x = x0
    for head, cw in zip(headers, col_widths):
        c.drawCentredString(x + cw / 2, y + 8, head)
        x += cw
    c.setStrokeColor(colors.HexColor("#C9DDEC"))
    yy = y - row_h
    c.setFont("CN", font_size)
    for i, row in enumerate(rows):
        c.setFillColor(colors.HexColor("#F4F8FB") if i % 2 else colors.white)
        c.rect(x0, yy, sum(col_widths), row_h, stroke=1, fill=1)
        c.setFillColor(TEXT)
        x = x0
        for cell, cw in zip(row, col_widths):
            if isinstance(cell, Path):
                iw, ih = img_size(cell)
                scale = min((cw - 8) / iw, (row_h - 6) / ih)
                dw, dh = iw * scale, ih * scale
                c.drawImage(ImageReader(str(cell)), x + (cw - dw) / 2, yy + (row_h - dh) / 2, dw, dh, mask="auto")
            else:
                c.drawCentredString(x + cw / 2, yy + 8, cell)
            x += cw
        yy -= row_h
    doc.y -= h + 12


def arrow(c, x1, y1, x2, y2, color=BLUE_DARK, lw=1.0):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x1, y1, x2, y2)
    if x2 >= x1:
        c.line(x2, y2, x2 - 5, y2 + 3)
        c.line(x2, y2, x2 - 5, y2 - 3)
    else:
        c.line(x2, y2, x2 + 5, y2 + 3)
        c.line(x2, y2, x2 + 5, y2 - 3)


def draw_simple_flow(doc, labels, width=82, height=32, gap=18):
    doc.ensure(height + 34)
    c = doc.c
    total = len(labels) * width + (len(labels) - 1) * gap
    x = MARGIN_X + (CONTENT_W - total) / 2
    y = doc.y - height - 10
    for i, label in enumerate(labels):
        c.setStrokeColor(BLUE)
        c.setLineWidth(1.1)
        c.setFillColor(colors.white)
        c.roundRect(x, y, width, height, 4, stroke=1, fill=1)
        c.setFillColor(BLUE_DARK)
        c.setFont("CNB", 8.8)
        c.drawCentredString(x + width / 2, y + 11, label)
        if i < len(labels) - 1:
            arrow(c, x + width + 3, y + height / 2, x + width + gap - 4, y + height / 2, BLUE)
        x += width + gap
    doc.y -= height + 30
    c.setFillColor(TEXT)


def draw_fft_split_tree(doc):
    doc.ensure(120)
    c = doc.c
    y = doc.y - 20
    x0 = MARGIN_X + 40
    levels = [
        [(x0, y - 30, "N 点 DFT")],
        [(x0 + 170, y - 8, "N/2 点 DFT"), (x0 + 170, y - 60, "N/2 点 DFT")],
        [(x0 + 345, y - 2, "N/4 点 DFT"), (x0 + 345, y - 36, "N/4 点 DFT"), (x0 + 345, y - 70, "N/4 点 DFT")],
    ]
    def box(x, yy, text):
        c.setStrokeColor(BLUE)
        c.setFillColor(colors.white)
        c.roundRect(x, yy, 92, 28, 3, stroke=1, fill=1)
        c.setFont("CNB", 8.4)
        c.setFillColor(BLUE_DARK)
        c.drawCentredString(x + 46, yy + 9, text)
    for level in levels:
        for x, yy, text in level:
            box(x, yy, text)
    arrow(c, x0 + 92, y - 16, x0 + 170, y + 6, BLUE)
    arrow(c, x0 + 92, y - 16, x0 + 170, y - 46, BLUE)
    arrow(c, x0 + 262, y + 6, x0 + 345, y + 12, BLUE)
    arrow(c, x0 + 262, y + 6, x0 + 345, y - 22, BLUE)
    arrow(c, x0 + 262, y - 46, x0 + 345, y - 56, BLUE)
    c.setFont("CN", 8.8)
    c.setFillColor(TEXT)
    c.drawString(x0 + 20, y - 100, "复乘次数：")
    draw_formula_at(c, r"N^2\rightarrow\frac{N^2}{2}\rightarrow\frac{N^2}{4}\rightarrow\cdots", "fft_tree_count", x0 + 83, y - 106, max_w=190, max_h=18, size=9.5)
    doc.y -= 135


def draw_butterfly(doc, negative_power=False, label_prefix="X"):
    doc.ensure(90)
    c = doc.c
    x0 = MARGIN_X + 150
    y0 = doc.y - 18
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.9)
    c.line(x0, y0, x0 + 210, y0 - 48)
    c.line(x0, y0 - 48, x0 + 210, y0)
    c.circle(x0 + 105, y0 - 24, 3, stroke=1, fill=1)
    draw_formula_at(c, rf"{label_prefix}_1(k)", f"bf_{label_prefix}_in1", x0 - 72, y0 - 7, max_w=60, max_h=16, size=9.2)
    draw_formula_at(c, rf"{label_prefix}_2(k)", f"bf_{label_prefix}_in2", x0 - 72, y0 - 55, max_w=60, max_h=16, size=9.2)
    draw_formula_at(c, rf"{label_prefix}_1(k)+W_N^k{label_prefix}_2(k)", f"bf_{label_prefix}_out1", x0 + 220, y0 - 7, max_w=135, max_h=16, size=9.0)
    draw_formula_at(c, rf"{label_prefix}_1(k)-W_N^k{label_prefix}_2(k)", f"bf_{label_prefix}_out2", x0 + 220, y0 - 55, max_w=135, max_h=16, size=9.0)
    draw_formula_at(c, r"W_N^k", f"bf_{label_prefix}_wn", x0 + 42, y0 - 44, max_w=46, max_h=14, size=8.8, bg=True)
    doc.y -= 85


def draw_dit_flow(doc, full=False):
    h = 170 if full else 128
    doc.ensure(h + 20)
    c = doc.c
    x_left = MARGIN_X + 36
    y_top = doc.y - 24
    ys = [y_top - i * 17 for i in range(8)]
    inputs = ["x(0)", "x(4)", "x(2)", "x(6)", "x(1)", "x(5)", "x(3)", "x(7)"]
    outputs = [f"X({i})" for i in range(8)]
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.setFont("CN", 7.5)
    for yy, lab in zip(ys, inputs):
        c.drawRightString(x_left - 8, yy - 2, lab)
        c.circle(x_left, yy, 2, stroke=1, fill=1)
    x1, x2, x3, x4 = x_left + 95, x_left + 205, x_left + 315, x_left + 430
    for yy, lab in zip(ys, outputs):
        c.drawString(x4 + 10, yy - 2, lab)
        c.circle(x4, yy, 2, stroke=1, fill=1)
    def pair(xa, xb, i, j, w="W_8^0"):
        c.line(xa, ys[i], xb, ys[i])
        c.line(xa, ys[j], xb, ys[j])
        c.line(xb, ys[i], xb + 40, ys[j])
        c.line(xb, ys[j], xb + 40, ys[i])
        c.circle(xb + 20, (ys[i] + ys[j]) / 2, 2, stroke=1, fill=1)
        safe = w.replace("_", "").replace("^", "p")
        draw_formula_at(c, w, f"dit_{safe}_{i}_{j}", xb + 24, (ys[i] + ys[j]) / 2 - 6, max_w=36, max_h=11, size=8.0, bg=True)
    for i in range(0, 8, 2):
        pair(x_left, x1, i, i + 1, "W_8^0")
    pair(x1 + 40, x2, 0, 2, "W_8^0")
    pair(x1 + 40, x2, 1, 3, "W_8^2")
    pair(x1 + 40, x2, 4, 6, "W_8^0")
    pair(x1 + 40, x2, 5, 7, "W_8^2")
    for i, w in zip(range(4), ["W_8^0", "W_8^1", "W_8^2", "W_8^3"]):
        pair(x2 + 40, x3, i, i + 4, w)
    for i in range(8):
        c.line(x3 + 40, ys[i], x4, ys[i])
    c.setFont("CNB", 8.6)
    c.setFillColor(BLUE_DARK)
    c.drawCentredString((x_left + x4) / 2, ys[-1] - 28, "基 2-DIT-FFT 蝶形流图（N=8）")
    doc.y -= h
    c.setFillColor(TEXT)


def draw_dif_flow(doc):
    h = 160
    doc.ensure(h + 20)
    c = doc.c
    x_left = MARGIN_X + 40
    y_top = doc.y - 22
    ys = [y_top - i * 17 for i in range(8)]
    outs = ["X(0)", "X(4)", "X(2)", "X(6)", "X(1)", "X(5)", "X(3)", "X(7)"]
    c.setFont("CN", 7.5)
    c.setStrokeColor(colors.black)
    for i, yy in enumerate(ys):
        c.drawRightString(x_left - 8, yy - 2, f"x({i})")
        c.circle(x_left, yy, 2, stroke=1, fill=1)
        c.drawString(x_left + 445, yy - 2, outs[i])
    def line(a, b, cidx, didx):
        c.line(a, ys[cidx], b, ys[didx])
    x1, x2, x3, x4 = x_left + 120, x_left + 245, x_left + 360, x_left + 435
    for i in range(4):
        line(x_left, x1, i, i)
        line(x_left, x1, i + 4, i)
        line(x_left, x1, i, i + 4)
        line(x_left, x1, i + 4, i + 4)
        c.circle(x1, ys[i], 2, stroke=1, fill=1)
        c.circle(x1, ys[i + 4], 2, stroke=1, fill=1)
        draw_formula_at(c, rf"W_N^{i}", f"dif_wn_{i}", x1 + 6, ys[i + 4] - 6, max_w=36, max_h=11, size=8.0, bg=True)
    for i in range(0, 8, 2):
        line(x1, x2, i, i)
        line(x1, x2, i + 1, i)
        line(x1, x2, i, i + 1)
        line(x1, x2, i + 1, i + 1)
        c.circle(x2, ys[i], 2, stroke=1, fill=1)
        c.circle(x2, ys[i + 1], 2, stroke=1, fill=1)
    for i in range(0, 8, 2):
        c.line(x2, ys[i], x3, ys[i])
        c.line(x2, ys[i + 1], x3, ys[i + 1])
        c.line(x3, ys[i], x3 + 32, ys[i + 1])
        c.line(x3, ys[i + 1], x3 + 32, ys[i])
        c.circle(x3 + 16, (ys[i] + ys[i + 1]) / 2, 2, stroke=1, fill=1)
    for i in range(8):
        c.line(x3 + 32, ys[i], x4, ys[i])
        c.circle(x4, ys[i], 2, stroke=1, fill=1)
    c.setFont("CNB", 8.6)
    c.setFillColor(BLUE_DARK)
    c.drawCentredString((x_left + x4) / 2, ys[-1] - 28, "基 2-DIF-FFT 蝶形流图（N=8）")
    doc.y -= h
    c.setFillColor(TEXT)


def draw_fft_convolution_flow(doc, n_label="N"):
    doc.ensure(118)
    c = doc.c
    y1 = doc.y - 30
    y2 = doc.y - 74
    x = MARGIN_X + 30
    def box(xb, yb, text, w=70):
        c.setStrokeColor(BLUE)
        c.setFillColor(colors.white)
        c.roundRect(xb, yb - 14, w, 28, 3, stroke=1, fill=1)
        c.setFont("CNB", 8)
        c.setFillColor(BLUE_DARK)
        c.drawCentredString(xb + w / 2, yb - 4, text)
        c.setFillColor(TEXT)
    c.setFont("CN", 8.6)
    c.drawString(x, y1 - 4, "x(n)")
    c.drawString(x, y2 - 4, "h(n)")
    for yy in [y1, y2]:
        arrow(c, x + 35, yy, x + 72, yy, BLUE)
        box(x + 72, yy, f"补零至{n_label}点", 88)
        arrow(c, x + 160, yy, x + 190, yy, BLUE)
        box(x + 190, yy, f"{n_label}点 FFT", 75)
    c.circle(x + 300, (y1 + y2) / 2, 10, stroke=1, fill=0)
    c.setFont("CNB", 12)
    c.drawCentredString(x + 300, (y1 + y2) / 2 - 4, "×")
    arrow(c, x + 265, y1, x + 290, (y1 + y2) / 2, BLUE)
    arrow(c, x + 265, y2, x + 290, (y1 + y2) / 2, BLUE)
    arrow(c, x + 310, (y1 + y2) / 2, x + 345, (y1 + y2) / 2, BLUE)
    box(x + 345, (y1 + y2) / 2, f"{n_label}点 IFFT", 82)
    arrow(c, x + 427, (y1 + y2) / 2, x + 470, (y1 + y2) / 2, BLUE)
    c.setFont("CN", 8.6)
    c.drawString(x + 474, (y1 + y2) / 2 - 4, "y(n)")
    doc.y -= 112


def build():
    register_fonts()
    doc = BatchDoc(PDF_PATH)
    doc.section = "4. 快速傅里叶变换"
    doc.header()

    doc.h2("4 快速傅里叶变换")
    doc.p("本章把 DFT 的计算量问题、基 2 FFT 的时间抽取与频率抽取、IFFT，以及实序列 FFT 的利用方式连成一条线。下面内容按原课件顺序重排。")
    doc.h2("4.1 快速傅里叶变换的定义")
    doc.p("设有限长序列，其非零值长度为 N。若直接计算一次 DFT，每一个频点都要把 N 项相乘相加；N 个频点累计后计算量迅速增大。")
    draw_formula_center(doc, f("dft_def", r"X(k)=\sum_{n=0}^{N-1}x(n)W_N^{kn},\qquad 0\leq k\leq N-1", 15), max_h=34)
    draw_small_table(
        doc,
        ["", "复数乘法", "复数加法"],
        [
            ["一点 DFT", f("one_mul", r"N", 13), f("one_add", r"N-1", 13)],
            ["N 点 DFT", f("n_mul", r"N^2", 13), f("n_add", r"N(N-1)", 13)],
        ],
        [CONTENT_W * 0.30, CONTENT_W * 0.35, CONTENT_W * 0.35],
    )
    draw_red_text(doc, "FFT 用于减少计算量，但本质还是 DFT。FFT 仅仅是 DFT 的一种快速算法。")
    draw_red_text(doc, "FFT 提高运算效率的本质：利用旋转因子的周期性和对称性，将长序列分解为短序列。")
    doc.h2("旋转因子的相关性质")
    draw_formula_list(
        doc,
        [
            ("定义", f("wn_def", r"W_N^{kn}=e^{-j\frac{2\pi}{N}kn}", 14)),
            ("对称性", f("wn_sym", r"W_N^{-kn}=W_N^{(N-n)k}=W_N^{(N-k)n}", 13.5)),
            ("周期性", f("wn_per", r"W_N^{kn}=W_N^{(N+n)k}=W_N^{(N+k)n}", 13.5)),
            ("可约性", f("wn_red1", r"W_N^{kn}=W_{Nm}^{knm},\qquad W_N^{kn}=W_{\frac{N}{m}}^{\frac{kn}{m}}", 13.5), 34),
            ("特殊点", f("wn_sp", r"W_N^0=W_N^N=1,\quad W_N^{N/2}=-1,\quad W_N^{k+N/2}=-W_N^k", 13), 34),
        ],
        max_h=31,
    )
    draw_source_figure(doc, "fft_split_tree_235.png", max_h=235)

    doc.h2("4.2 快速傅里叶变换的分类")
    draw_note_box(doc, "FFT 分类", ["时间抽取法：DIT，Decimation-In-Time。", "频率抽取法：DIF，Decimation-In-Frequency。"])

    doc.h2("基于时间抽取的基 2 FFT")
    doc.p("设输入序列长度 N=2^M。按时间顺序进行奇偶分解，把长序列逐步分解为越来越短的子序列；若 N 不满足 2^M，可加零补长。")
    draw_source_figure(doc, "fft_dit_design_238.png", max_h=230)
    draw_formula_center(doc, f("dit_split", r"x_1(r)=x(2r),\qquad x_2(r)=x(2r+1),\qquad r=0,1,\cdots,\frac{N}{2}-1", 13.2), max_h=32)
    draw_formula_center(doc, f("dit_sum1", r"X(k)=\sum_{r=0}^{N/2-1}x(2r)W_N^{2kr}+\sum_{r=0}^{N/2-1}x(2r+1)W_N^{k(2r+1)}", 12.8), max_h=34)
    draw_formula_center(doc, f("dit_sum2", r"X(k)=X_1(k)+W_N^kX_2(k),\qquad 0\leq k\leq\frac{N}{2}-1", 14), max_h=32)
    draw_formula_center(doc, f("dit_sum3", r"X\left(k+\frac{N}{2}\right)=X_1(k)-W_N^kX_2(k)", 14), max_h=32)
    draw_source_figure(doc, "fft_butterfly_241.png", max_h=175)
    draw_source_figure(doc, "fft_dit_one_stage_242.png", max_h=230)
    draw_source_figure(doc, "fft_dit_full_245.png", max_h=260)
    draw_red_text(doc, "基 2-DIT-FFT 算法复数乘法次数：")
    draw_formula_center(doc, f("dit_mul_count", r"\frac{N}{2}M=\frac{N}{2}\log_2 N", 16), max_h=34)
    draw_small_table(
        doc,
        ["方法", "复数乘法", "复数加法"],
        [["DFT", f("dft_count_mul", r"N^2", 13), f("dft_count_add", r"N(N-1)", 13)], ["FFT", f("fft_count_mul", r"\frac{N}{2}\log_2N", 13), f("fft_count_add", r"N\log_2N", 13)]],
        [CONTENT_W * 0.30, CONTENT_W * 0.35, CONTENT_W * 0.35],
    )
    doc.h2("例 1  64 点 DFT 的运算时间")
    doc.p("已知平均每次复乘用 1 us，每次复加用 0.1 us。计算 64 点 DFT 时，比较直接 DFT 与 FFT 的时间。")
    draw_formula_list(
        doc,
        [
            ("直接复乘", f("ex64_dft_mul", r"T_1=N^2\cdot1\cdot10^{-6}=4.096\times10^{-3}\ {\rm s}", 12.5), 28),
            ("直接复加", f("ex64_dft_add", r"T_2=N(N-1)\cdot0.1\cdot10^{-6}=4.032\times10^{-3}\ {\rm s}", 12.5), 28),
            ("直接总计", f("ex64_dft_total", r"T=T_1+T_2=8.128\times10^{-3}\ {\rm s}", 12.8), 28),
            ("FFT 复乘", f("ex64_fft_mul", r"T_1=\frac{N}{2}\log_2N\cdot1\cdot10^{-6}=1.92\times10^{-4}\ {\rm s}", 12.5), 30),
            ("FFT 复加", f("ex64_fft_add", r"T_2=N\log_2N\cdot0.1\cdot10^{-6}=3.84\times10^{-4}\ {\rm s}", 12.5), 30),
            ("FFT 总计", f("ex64_fft_total", r"T=T_1+T_2=5.76\times10^{-4}\ {\rm s}", 12.8), 28),
        ],
        max_h=30,
    )

    doc.h2("基于频率抽取的基 2 FFT")
    doc.p("频率抽取法先把序列前后对半分开，再按频率下标的偶奇分组。")
    draw_formula_center(doc, f("dif_split1", r"X(k)=\sum_{n=0}^{N/2-1}x(n)W_N^{kn}+\sum_{n=0}^{N/2-1}x\left(n+\frac{N}{2}\right)W_N^{k\left(n+\frac{N}{2}\right)}", 12.4), max_h=38)
    draw_formula_center(doc, f("dif_split2", r"X(k)=\sum_{n=0}^{N/2-1}\left[x(n)+x\left(n+\frac{N}{2}\right)(-1)^k\right]W_N^{kn}", 13), max_h=32)
    draw_formula_center(doc, f("dif_even", r"X(2r)=\sum_{n=0}^{N/2-1}\left[x(n)+x\left(n+\frac{N}{2}\right)\right]W_{N/2}^{rn}", 13), max_h=32)
    draw_formula_center(doc, f("dif_odd", r"X(2r+1)=\sum_{n=0}^{N/2-1}\left[x(n)-x\left(n+\frac{N}{2}\right)\right]W_N^n W_{N/2}^{rn}", 13), max_h=34)
    draw_formula_list(
        doc,
        [
            ("定义 1", f("dif_x1", r"x_1(n)=x(n)+x\left(n+\frac{N}{2}\right)", 13), 28),
            ("定义 2", f("dif_x2", r"x_2(n)=\left[x(n)-x\left(n+\frac{N}{2}\right)\right]W_N^n", 13), 30),
            ("偶频点", f("dif_even_x", r"X(2r)=\sum_{n=0}^{N/2-1}x_1(n)W_{N/2}^{rn}=X_1(k)", 13), 30),
            ("奇频点", f("dif_odd_x", r"X(2r+1)=\sum_{n=0}^{N/2-1}x_2(n)W_{N/2}^{rn}=X_2(k)", 13), 30),
        ],
        max_h=32,
    )
    draw_source_figure(doc, "fft_dif_one_stage_250.png", max_h=235)
    draw_source_figure(doc, "fft_dif_full_251.png", max_h=245)
    draw_note_box(doc, "结论", ["频率抽取法和时间抽取法总的计算量相同；区别主要在输入/输出顺序和每一级蝶形结构的位置。"])

    doc.h2("4.3 快速傅里叶反变换 IFFT")
    draw_formula_list(
        doc,
        [
            ("DFT", f("ifft_dft", r"X(k)=\sum_{n=0}^{N-1}x(n)W_N^{kn},\qquad 0\leq k\leq N-1", 13.5), 32),
            ("IDFT", f("ifft_idft", r"x(n)=\frac{1}{N}\sum_{k=0}^{N-1}X(k)W_N^{-kn},\qquad 0\leq n\leq N-1", 13.5), 34),
        ],
        max_h=34,
    )
    draw_formula_list(
        doc,
        [
            ("旋转因子", f("ifft_note_rot", r"W_N^k\rightarrow W_N^{-k}", 13.5), 26),
            ("输出系数", f("ifft_note_scale", r"\frac{1}{N}", 14), 24),
            ("输入输出", f("ifft_note_swap", r"X(k)\leftrightarrow x(n)", 13.5), 24),
        ],
        max_h=26,
    )
    draw_source_figure(doc, "fft_ifft_253.png", max_h=235)

    doc.h2("FFT 方法求线性卷积")
    draw_red_text(doc, "线性卷积直接法的乘法次数：")
    draw_formula_center(doc, f("lin_conv_count", r"N_1N_2", 16), max_h=25)
    draw_source_figure(doc, "fft_conv_flow_254.png", max_h=225)
    draw_formula_center(doc, f("conv_condition", r"N\geq N_1+N_2-1", 15), max_h=26)
    draw_formula_center(doc, f("conv_fft_result", r"y(n)=IDFT[X(k)H(k)]=x(n)\circledast_N h(n)=y_l(n)", 13), max_h=30)
    draw_formula_center(doc, f("conv_fft_count", r"3\cdot\frac{N}{2}\log_2N+N", 15), max_h=28)
    doc.h2("例 2  复序列卷积的 FFT 计算量")
    doc.p("长度 8000 的复序列与长度 100 的复序列卷积，比较直接卷积、基 2 FFT 和 1024 点重叠相加法。")
    draw_formula_list(
        doc,
        [
            ("直接卷积", f("ex_conv_direct", r"8000\times100=8\times10^5", 14), 28),
            ("补零长度", f("ex_conv_8192", r"8000+100-1=8099,\quad N=8192", 13), 28),
        ],
        max_h=28,
    )
    draw_source_figure(doc, "fft_conv_8192_256.png", max_h=125)
    draw_formula_center(doc, f("ex_overlap_m", r"M+100-1=1024\Rightarrow M=925,\qquad \left\lceil\frac{8000}{925}\right\rceil=9", 13), max_h=32)
    draw_formula_center(doc, f("ex_overlap_count", r"(10+9)\cdot\frac{1024}{2}\log_2 1024+9\cdot1024=106496", 13.5), max_h=32)

    doc.h2("4.4 实序列的 FFT 算法")
    doc.p("实际工作中输入通常是实序列；若把它直接看作虚部为零的复序列，会增加存储量和运算时间。")
    draw_bullet_list(doc, ["一次 N 点 FFT 计算两个 N 点实序列的 FFT。", "一次 N/2 点 FFT 计算一个 N 点实序列的 FFT。"])
    doc.h2("一次 N 点 FFT 计算两个 N 点实序列")
    draw_formula_center(doc, f("real_two_y", r"y(n)=x_1(n)+jx_2(n)", 15), max_h=24)
    draw_formula_list(
        doc,
        [
            ("分解", f("real_y_parts", r"Y(k)=Y_{ep}(k)+Y_{op}(k)", 14), 25),
            ("实部", f("real_x1_time", r"x_1(n)=Re[y(n)]=\frac{1}{2}[y(n)+y^*(n)]", 13), 30),
            ("虚部", f("real_x2_time", r"jx_2(n)=jIm[y(n)]=\frac{1}{2}[y(n)-y^*(n)]", 13), 30),
            ("第一路", f("real_x1_freq", r"X_1(k)=Y_{ep}(k)=\frac{1}{2}[Y(k)+Y^*(N-k)]", 13), 30),
            ("第二路", f("real_x2_freq", r"X_2(k)=\frac{1}{j}Y_{op}(k)=\frac{1}{2j}[Y(k)-Y^*(N-k)]", 13), 32),
        ],
        max_h=32,
    )
    doc.h2("一次 N/2 点 FFT 计算一个 N 点实序列")
    draw_formula_list(
        doc,
        [
            ("构造", f("real_half_x", r"x_1(n)=x(2n),\qquad x_2(n)=x(2n+1),\qquad y(n)=x_1(n)+jx_2(n)", 12.8), 32),
            ("变换", f("real_half_y", r"X_1(k)=DFT[x_1(n)]=Y_{ep}(k),\qquad X_2(k)=DFT[x_2(n)]=\frac{1}{j}Y_{op}(k)", 12.8), 34),
            ("对称性", f("real_half_sym", r"X(N-k)=X^*(k)", 15, color="#D71920"), 26),
            ("合成", f("real_half_combine", r"X(k)=X_1(k)+W_N^kX_2(k),\quad X\left(k+\frac{N}{2}\right)=X_1(k)-W_N^kX_2(k)", 13), 36),
        ],
        max_h=34,
    )
    doc.h2("例 3  8 点 DFT 分解为两个 4 点 DFT")
    draw_formula_list(
        doc,
        [
            ("偶奇抽取", f("ex8_split", r"x_1(n)=x(2n),\qquad x_2(n)=x(2n+1),\qquad n=0,1,2,3", 13), 30),
            ("构造", f("ex8_y", r"y(n)=x_1(n)+jx_2(n)", 14), 24),
            ("4 点 FFT", f("ex8_yk", r"Y(k)=Y_{ep}(k)+Y_{op}(k)", 14), 24),
            ("分解", f("ex8_x12", r"X_1(k)=Y_{ep}(k),\qquad X_2(k)=-jY_{op}(k),\quad k=0,1,2,3", 13), 32),
            ("合成", f("ex8_combine", r"X(k)=X_1(k)+W_8^kX_2(k),\qquad X(k+4)=X_1(k)-W_8^kX_2(k)", 13), 34),
        ],
        max_h=34,
    )
    doc.ensure(285)
    doc.h2("例 3 蝶形合成示意")
    draw_source_figure(doc, "fft_real_butterfly_261.png", max_h=230)

    doc.h2("第四章小结")
    draw_note_box(
        doc,
        "章节导图",
        [
            "FFT 定义：与 DFT 运算量比较，理解 FFT 只是 DFT 的快速算法。",
            "FFT 分类：基于时间抽取的基 2 FFT 与基于频率抽取的基 2 FFT；重点是会画图、会计算。",
            "IFFT：旋转因子取负指数，输出端乘 1/N。",
            "实序列 FFT：一次 N 点 FFT 算两个实序列，或一次 N/2 点 FFT 算一个实序列。",
        ],
    )
    doc.h2("第四章课后习题")
    draw_bullet_list(
        doc,
        [
            "4-3：一次 N 点 FFT 计算两个 N 点实序列的 FFT。",
            "4-4 第（1）问：一次 N/2 点 FFT 计算一个 N 点实序列的 FFT；第（2）问感兴趣的同学可做。",
            "习 4.1：FFT 是利用什么来减少计算量？",
            "习 4.2：分别画出 8 点基 2 DIT-FFT 和 DIF-FFT 的运算流图。",
            "习 4.3：直接计算 N=16 的 DFT 需要多少次复数乘法、复数加法；使用基 2 FFT 算法需要多少次复数乘法。",
        ],
    )
    doc.h2("课后习题答案")
    draw_bullet_list(
        doc,
        [
            "解 4.1：利用旋转因子的周期性和对称性来减少计算量，不是蝶形运算。",
            "解 4.2：运算流图可参考本章 DIT 与 DIF 两张 N=8 流图。",
            "解 4.3：直接 DFT 复数乘法 256 次，复数加法 240 次；基 2 FFT 复数乘法 32 次。",
        ],
    )

    doc.save()
    NOTE_PATH.write_text(
        "# 第八批校对记录\n\n"
        "- 范围：原 PPT 228-265，第四章《快速傅里叶变换》。\n"
        "- 保留内容：FFT 定义、DIT/DIF 推导、蝶形运算、IFFT、FFT 求线性卷积、实序列 FFT、例题、章节导图、课后题和答案。\n"
        "- 明确修正：原 PPT 259 中“由 X(K) 可以求得”按上下文改为由 Y(k) 分解得到两个实序列的 DFT。\n"
        "- 待抽检：DIT/DIF 流图线条、公式上下标大小、课后题末尾位置。\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    build()
