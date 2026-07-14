import os
from pathlib import Path
from math import cos, pi

ROOT = Path(__file__).resolve().parents[1]
MPL_DIR = ROOT / "work" / "mplcache"
MPL_DIR.mkdir(parents=True, exist_ok=True)
os.environ["MPLCONFIGDIR"] = str(MPL_DIR)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["mathtext.fontset"] = "stix"
matplotlib.rcParams["font.family"] = "STIXGeneral"
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True)
PDF_PATH = OUT_DIR / "DSP讲义重制_样章_前15页_坐标轴明显加长版.pdf"
NOTE_PATH = OUT_DIR / "DSP讲义重制_样章_校对记录.md"
FORMULA_DIR = ROOT / "work" / "formula_cache"
FORMULA_DIR.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = A4
MARGIN_X = 48
TOP = 778
BOTTOM = 58
CONTENT_W = PAGE_W - 2 * MARGIN_X

BLUE = colors.HexColor("#0875D1")
BLUE_DARK = colors.HexColor("#075B9C")
BLUE_LIGHT = colors.HexColor("#EAF5FF")
LINE = colors.HexColor("#CADCEB")
TEXT = colors.HexColor("#1F2933")
MUTED = colors.HexColor("#5E6B75")
PALE = colors.HexColor("#F6F9FC")


def register_fonts():
    fallback = r"C:\Windows\Fonts\simhei.ttf"
    for name, path in [
        ("CN", r"C:\Windows\Fonts\msyh.ttc"),
        ("CNB", r"C:\Windows\Fonts\msyhbd.ttc"),
        ("CNL", r"C:\Windows\Fonts\msyhl.ttc"),
    ]:
        try:
            pdfmetrics.registerFont(TTFont(name, path))
        except Exception:
            pdfmetrics.registerFont(TTFont(name, fallback))


def text_width(font, size, text):
    return pdfmetrics.stringWidth(text, font, size)


def centered_text_baselines(font_name, font_size, center_y, line_count, leading=None):
    """Return baselines whose rendered glyph group is centered at center_y."""
    if line_count <= 0:
        return []
    leading = leading or font_size * 1.35
    ascent = pdfmetrics.getAscent(font_name) * font_size / 1000
    descent = pdfmetrics.getDescent(font_name) * font_size / 1000
    first = center_y + (line_count - 1) * leading / 2 - (ascent + descent) / 2
    return [first - index * leading for index in range(line_count)]


def draw_centered_multiline_text(c, center_x, center_y, text, font_name="CNB",
                                 font_size=9.2, leading=None, color=TEXT):
    lines = str(text).split("\n")
    c.setFillColor(color)
    c.setFont(font_name, font_size)
    for line, baseline in zip(
        lines,
        centered_text_baselines(font_name, font_size, center_y, len(lines), leading),
    ):
        c.drawCentredString(center_x, baseline, line)


def wrap(text, width, font="CN", size=9.8):
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        line = ""
        for ch in para:
            if text_width(font, size, line + ch) <= width:
                line += ch
            else:
                if line:
                    lines.append(line)
                line = ch
        if line:
            lines.append(line)
    return lines


def formula_png(name, expr, fontsize=13, color="#111111"):
    path = FORMULA_DIR / f"{name}.png"
    fig = plt.figure(figsize=(0.01, 0.01), dpi=300)
    fig.patch.set_alpha(0)
    fig.text(0, 0, f"${expr}$", fontsize=fontsize, color=color)
    fig.savefig(path, dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    return path


def _paste_rgba(base, im, xy):
    base.alpha_composite(im, dest=(int(xy[0]), int(xy[1])))


def _trim_rgba(im):
    bbox = im.getbbox()
    return im.crop(bbox) if bbox else im


def _open_trim_rgba(path):
    return _trim_rgba(Image.open(path).convert("RGBA"))


def piecewise_png(name, lhs_expr, row1_expr, row2_expr=None, row2_cn=None, fontsize=18):
    path = FORMULA_DIR / f"{name}.png"
    lhs = _open_trim_rgba(formula_png(f"{name}_lhs", lhs_expr, fontsize))
    brace = _open_trim_rgba(
        formula_png(f"{name}_brace", r"\left\{\substack{\phantom{1}\\\phantom{0}}\right.", fontsize + 9)
    )
    row1 = _open_trim_rgba(formula_png(f"{name}_row1", row1_expr, fontsize))
    if row2_cn is None:
        row2 = _open_trim_rgba(formula_png(f"{name}_row2", row2_expr, fontsize))
    else:
        value = _open_trim_rgba(formula_png(f"{name}_row2_value", r"0,", fontsize))
        n_part = _open_trim_rgba(formula_png(f"{name}_row2_n", r"n", fontsize))
        cn_font = ImageFont.truetype(r"C:\Windows\Fonts\simsun.ttc", 72)
        probe = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
        d = ImageDraw.Draw(probe)
        cn_box = d.textbbox((0, 0), row2_cn, font=cn_font)
        cn_w = cn_box[2] - cn_box[0]
        cn_h = cn_box[3] - cn_box[1]
        cn_gap = 4
        n_gap = 16
        row2 = Image.new(
            "RGBA",
            (value.width + cn_gap + cn_w + n_gap + n_part.width, max(value.height, cn_h, n_part.height) + 6),
            (255, 255, 255, 0),
        )
        mid_y = row2.height // 2
        _paste_rgba(row2, value, (0, mid_y - value.height / 2))
        d = ImageDraw.Draw(row2)
        d.text((value.width + cn_gap, mid_y - cn_h / 2 - cn_box[1]), row2_cn, fill=(17, 17, 17, 255), font=cn_font)
        _paste_rgba(row2, n_part, (value.width + cn_gap + cn_w + n_gap, mid_y - n_part.height / 2))
        row2 = _trim_rgba(row2)

    gap_lhs = 4
    gap_brace = 1
    row_gap = 8
    formula_h = max(lhs.height, brace.height, row1.height + row2.height + row_gap)
    canvas_w = lhs.width + gap_lhs + brace.width + gap_brace + max(row1.width, row2.width) + 2
    canvas_h = formula_h + 4
    out = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 0))
    center_y = canvas_h // 2
    x = 0
    _paste_rgba(out, lhs, (x, center_y - lhs.height / 2))
    x += lhs.width + gap_lhs
    _paste_rgba(out, brace, (x, center_y - brace.height / 2))
    x += brace.width + gap_brace
    rows_h = row1.height + row_gap + row2.height
    row1_y = center_y - rows_h / 2
    row2_y = row1_y + row1.height + row_gap
    _paste_rgba(out, row1, (x, row1_y))
    _paste_rgba(out, row2, (x, row2_y))
    _trim_rgba(out).save(path)
    return path


def piecewise3_cn_png(name, lhs_expr, row1_expr, row2_expr, row3_cn="其余", fontsize=17):
    path = FORMULA_DIR / f"{name}.png"
    lhs = _open_trim_rgba(formula_png(f"{name}_lhs", lhs_expr, fontsize))
    brace = _open_trim_rgba(
        formula_png(f"{name}_brace", r"\left\{\substack{\phantom{1}\\\phantom{1}\\\phantom{1}}\right.", fontsize + 12)
    )
    row1 = _open_trim_rgba(formula_png(f"{name}_row1", row1_expr, fontsize))
    row2 = _open_trim_rgba(formula_png(f"{name}_row2", row2_expr, fontsize))
    value = _open_trim_rgba(formula_png(f"{name}_row3_value", r"0,", fontsize))
    n_part = _open_trim_rgba(formula_png(f"{name}_row3_n", r"n", fontsize))

    cn_font = ImageFont.truetype(r"C:\Windows\Fonts\simsun.ttc", 72)
    probe = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
    d = ImageDraw.Draw(probe)
    cn_box = d.textbbox((0, 0), row3_cn, font=cn_font)
    cn_w = cn_box[2] - cn_box[0]
    cn_h = cn_box[3] - cn_box[1]
    cn_gap = 4
    n_gap = 16
    row3 = Image.new(
        "RGBA",
        (value.width + cn_gap + cn_w + n_gap + n_part.width, max(value.height, cn_h, n_part.height) + 6),
        (255, 255, 255, 0),
    )
    mid_y = row3.height // 2
    _paste_rgba(row3, value, (0, mid_y - value.height / 2))
    d = ImageDraw.Draw(row3)
    d.text((value.width + cn_gap, mid_y - cn_h / 2 - cn_box[1]), row3_cn, fill=(17, 17, 17, 255), font=cn_font)
    _paste_rgba(row3, n_part, (value.width + cn_gap + cn_w + n_gap, mid_y - n_part.height / 2))
    row3 = _trim_rgba(row3)

    gap_lhs = 4
    gap_brace = 1
    row_gap = 13
    rows = [row1, row2, row3]
    rows_h = sum(r.height for r in rows) + row_gap * 2
    formula_h = max(lhs.height, brace.height, rows_h)
    canvas_w = lhs.width + gap_lhs + brace.width + gap_brace + max(r.width for r in rows) + 2
    canvas_h = formula_h + 4
    out = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 0))
    center_y = canvas_h // 2
    x = 0
    _paste_rgba(out, lhs, (x, center_y - lhs.height / 2))
    x += lhs.width + gap_lhs
    _paste_rgba(out, brace, (x, center_y - brace.height / 2))
    x += brace.width + gap_brace
    y = center_y - rows_h / 2
    for row in rows:
        _paste_rgba(out, row, (x, y))
        y += row.height + row_gap
    _trim_rgba(out).save(path)
    return path


def piecewise(lhs, rows):
    return ("piecewise", lhs, rows)


def piecewise_cases(lhs, cases_path):
    return ("piecewise_cases", lhs, cases_path)


def piecewise_cn(lhs, rows):
    return ("piecewise_cn", lhs, rows)


class Doc:
    def __init__(self, path):
        self.c = canvas.Canvas(str(path), pagesize=A4)
        self.page = 0
        self.section = "数字信号处理基础"
        self.y = TOP

    def header(self):
        self.page += 1
        c = self.c
        c.setFillColor(colors.HexColor("#333333"))
        c.setFont("CN", 8.7)
        c.drawString(MARGIN_X, PAGE_H - 24, "华理814DSP讲义")
        c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 24, self.section)
        c.setStrokeColor(colors.HexColor("#777777"))
        c.setLineWidth(0.55)
        c.line(MARGIN_X, PAGE_H - 31, PAGE_W - MARGIN_X, PAGE_H - 31)
        c.setFillColor(MUTED)
        c.setFont("CN", 8.2)
        c.drawCentredString(PAGE_W / 2, 28, f"{self.page}")
        self.y = TOP

    def start(self):
        self.header()

    def new_page(self, section=None):
        self.c.showPage()
        if section:
            self.section = section
        self.header()

    def ensure(self, height, section=None):
        if self.y - height < BOTTOM:
            self.new_page(section)

    def save(self):
        self.c.save()

    def h1(self, title, subtitle=None):
        # Chapter-level headings always begin on a fresh page.  The only
        # exception is the first heading drawn immediately after header().
        if self.y < TOP - 1:
            self.new_page()
        self.ensure(78)
        c = self.c
        c.setFillColor(BLUE)
        c.setFont("CNB", 22)
        c.drawString(MARGIN_X, self.y, title)
        c.setStrokeColor(BLUE)
        c.setLineWidth(2.1)
        c.line(MARGIN_X, self.y - 9, MARGIN_X + 82, self.y - 9)
        self.y -= 28
        if subtitle:
            c.setFillColor(MUTED)
            c.setFont("CN", 9.8)
            c.drawString(MARGIN_X, self.y, subtitle)
            self.y -= 22
        self.y -= 6

    def h2(self, text):
        self.ensure(42)
        c = self.c
        c.setFillColor(BLUE)
        c.roundRect(MARGIN_X, self.y - 20, 6, 20, 2, stroke=0, fill=1)
        c.setFillColor(TEXT)
        c.setFont("CNB", 14.0)
        c.drawString(MARGIN_X + 14, self.y - 15, text)
        self.y -= 33

    def h3(self, text):
        self.ensure(25)
        self.c.setFillColor(BLUE_DARK)
        self.c.setFont("CNB", 11.2)
        self.c.drawString(MARGIN_X, self.y, text)
        self.y -= 17

    def p(self, text, size=9.8, leading=16):
        lines = wrap(text, CONTENT_W, "CN", size)
        self.ensure(len(lines) * leading + 6)
        self.c.setFillColor(TEXT)
        self.c.setFont("CN", size)
        for line in lines:
            self.c.drawString(MARGIN_X, self.y, line)
            self.y -= leading
        self.y -= 4

    def bullet(self, items, size=9.4, leading=15):
        total = 0
        line_sets = []
        for item in items:
            ls = wrap(item, CONTENT_W - 18, "CN", size)
            line_sets.append(ls)
            total += len(ls) * leading + 3
        self.ensure(total + 3)
        c = self.c
        c.setFont("CN", size)
        for ls in line_sets:
            c.setFillColor(colors.black)
            c.circle(MARGIN_X + 3.5, self.y + 3.5, 2.2, stroke=0, fill=1)
            c.setFillColor(TEXT)
            for line in ls:
                c.drawString(MARGIN_X + 16, self.y, line)
                self.y -= leading
            self.y -= 3

    def note(self, title, body, compact=False):
        size = 8.8 if compact else 9.1
        lines = wrap(body, CONTENT_W - 30, "CN", size)
        h = 28 + len(lines) * 13
        self.ensure(h + 8)
        c = self.c
        c.setFillColor(colors.white)
        c.rect(MARGIN_X, self.y - h + 8, CONTENT_W, h, stroke=0, fill=1)
        c.setStrokeColor(colors.HexColor("#A8A8A8"))
        c.setLineWidth(0.55)
        c.rect(MARGIN_X, self.y - h + 8, CONTENT_W, h, stroke=1, fill=0)
        c.setFillColor(colors.HexColor("#222222"))
        c.setFont("CNB", 9.2)
        c.drawString(MARGIN_X + 13, self.y - 13, title)
        c.setFillColor(TEXT)
        c.setFont("CN", size)
        yy = self.y - 29
        for line in lines:
            c.drawString(MARGIN_X + 13, yy, line)
            yy -= 13
        self.y -= h + 8

    def formula_box(self, image_path, height=36):
        self.ensure(height + 10)
        c = self.c
        im = Image.open(image_path)
        iw, ih = im.size
        scale = min((CONTENT_W * 0.72) / iw, (height - 14) / ih)
        dw, dh = iw * scale, ih * scale
        x = MARGIN_X + (CONTENT_W - dw) / 2
        y = self.y - height + (height - dh) / 2
        c.drawImage(ImageReader(str(image_path)), x, y, dw, dh, mask="auto")
        self.y -= height + 12

    def formula_bullets(self, items, size=9.3, leading=23):
        self.ensure(len(items) * (leading + 3) + 4)
        c = self.c
        c.setFont("CN", size)
        for formula_path, text in items:
            c.setFillColor(colors.black)
            c.circle(MARGIN_X + 3.5, self.y + 3.5, 2.2, stroke=0, fill=1)
            im = Image.open(formula_path)
            iw, ih = im.size
            scale = min(260 / iw, 24 / ih)
            dw, dh = iw * scale, ih * scale
            c.drawImage(ImageReader(str(formula_path)), MARGIN_X + 18, self.y + 3 - dh / 2, dw, dh, mask="auto")
            c.setFillColor(TEXT)
            c.drawString(MARGIN_X + 278, self.y, text)
            self.y -= leading + 3

    def exercise_space(self, height=46):
        self.ensure(height + 4)
        self.y -= height + 4

    def table(self, headers, rows, col_w, row_h=34):
        h = row_h * (len(rows) + 1) + 14
        self.ensure(h)
        c = self.c
        x, y = MARGIN_X, self.y
        total_w = sum(col_w)
        c.setFillColor(colors.HexColor("#F0F0F0"))
        c.rect(x, y - row_h, total_w, row_h, stroke=0, fill=1)
        c.setFillColor(colors.black)
        c.setFont("CNB", 8.8)
        xx = x
        for i, head in enumerate(headers):
            c.drawCentredString(xx + col_w[i] / 2, y - 20, head)
            xx += col_w[i]
        y0 = y - row_h
        c.setFont("CN", 8.5)
        for r, row in enumerate(rows):
            c.setFillColor(colors.white if r % 2 == 0 else colors.HexColor("#F8F8F8"))
            c.rect(x, y0 - row_h, total_w, row_h, stroke=0, fill=1)
            c.setFillColor(TEXT)
            xx = x
            for i, text in enumerate(row):
                if isinstance(text, Path):
                    im = Image.open(text)
                    iw, ih = im.size
                    formula_h = 31 if "piecewise" in text.name else 18
                    scale = min((col_w[i] - 26) / iw, min(row_h - 10, formula_h) / ih)
                    dw, dh = iw * scale, ih * scale
                    c.drawImage(ImageReader(str(text)), xx + 18, y0 - row_h + (row_h - dh) / 2, dw, dh, mask="auto")
                elif isinstance(text, tuple) and text[0] == "piecewise":
                    _, lhs, case_rows = text
                    center_y = y0 - row_h / 2
                    lhs_x = xx + 18
                    c.setFillColor(TEXT)
                    c.setFont("CN", 8.8)
                    c.drawString(lhs_x, center_y - 2, lhs)
                    brace_x = lhs_x + text_width("CN", 8.8, lhs) + 6
                    case_x = brace_x + 19
                    c.setFont("Times-Roman", 28)
                    c.drawString(brace_x, center_y - 13, "{")
                    c.setFont("CN", 8.2)
                    c.drawString(case_x, center_y + 4, case_rows[0])
                    c.drawString(case_x, center_y - 11, case_rows[1])
                elif isinstance(text, tuple) and text[0] == "piecewise_cases":
                    _, lhs, cases_path = text
                    center_y = y0 - row_h / 2
                    lhs_x = xx + 18
                    c.setFillColor(TEXT)
                    c.setFont("CN", 10.8)
                    lhs_w = text_width("CN", 10.8, lhs)
                    im = Image.open(cases_path)
                    iw, ih = im.size
                    scale = min((col_w[i] - 32 - lhs_w) / iw, min(row_h - 8, 31) / ih)
                    dw, dh = iw * scale, ih * scale
                    c.drawString(lhs_x, center_y - 4, lhs)
                    c.drawImage(
                        ImageReader(str(cases_path)),
                        lhs_x + lhs_w + 4,
                        center_y - dh / 2,
                        dw,
                        dh,
                        mask="auto",
                    )
                elif isinstance(text, tuple) and text[0] == "piecewise_cn":
                    _, lhs, case_rows = text
                    center_y = y0 - row_h / 2
                    lhs_x = xx + 18
                    c.setFillColor(TEXT)
                    c.setFont("CN", 10.8)
                    lhs_w = text_width("CN", 10.8, lhs)
                    brace_x = lhs_x + lhs_w + 3
                    value_right_x = brace_x + 31
                    condition_x = value_right_x + 5
                    top_y = center_y + 7
                    bottom_y = center_y - 10
                    c.drawString(lhs_x, center_y - 4, lhs)
                    c.setFont("Times-Roman", 35)
                    c.drawString(brace_x, center_y - 16, "{")
                    c.setFont("CN", 10.5)
                    c.drawRightString(value_right_x, top_y, case_rows[0][0])
                    c.drawString(condition_x, top_y, case_rows[0][1])
                    c.drawRightString(value_right_x, bottom_y, case_rows[1][0])
                    c.drawString(condition_x, bottom_y, case_rows[1][1])
                else:
                    lines = wrap(text, col_w[i] - 12, "CN", 8.5)[:2]
                    yy = y0 - 14
                    for line in lines:
                        c.drawString(xx + 6, yy, line)
                        yy -= 11
                xx += col_w[i]
            y0 -= row_h
        c.setStrokeColor(colors.HexColor("#9A9A9A"))
        c.rect(x, y - row_h * (len(rows) + 1), total_w, row_h * (len(rows) + 1), stroke=1, fill=0)
        xx = x
        for w in col_w[:-1]:
            xx += w
            c.line(xx, y, xx, y - row_h * (len(rows) + 1))
        self.y -= row_h * (len(rows) + 1) + 16


def draw_flow(doc):
    """Reproduce the source PPT processing chain without decorative restyling."""
    doc.ensure(66)
    c = doc.c
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.setLineWidth(0.8)
    y = doc.y - 25
    h = 34
    x = MARGIN_X + 5
    input_w = 42
    boxes = [
        (58, "预滤波"),
        (66, "A/D转换"),
        (72, "数字信号\n处理"),
        (66, "D/A转换"),
        (58, "平滑滤波"),
    ]
    gap = 17
    c.setFont("Times-Italic", 11)
    c.drawString(x, y - 4, "x(t)")
    cursor = x + input_w
    for index, (width, label) in enumerate(boxes):
        _axis_arrow(c, cursor, y, cursor + gap - 3, y)
        bx = cursor + gap
        c.rect(bx, y - h / 2, width, h, stroke=1, fill=0)
        draw_centered_multiline_text(
            c, bx + width / 2, y, label, "CN", 8.5, leading=12, color=colors.black
        )
        cursor = bx + width
    _axis_arrow(c, cursor, y, cursor + gap - 3, y)
    c.setFont("Times-Italic", 11)
    c.drawString(cursor + gap + 2, y - 4, "y(t)")
    doc.y -= 62


def signal_classification_axis_geometry():
    return {
        "sample_scale": 28.0,
        "vertical_arrow_headroom": 12.0,
        "vertical_negative_tail": 24.0,
        "highest_labeled_tick": 2,
    }


def draw_signal_classification_examples(doc):
    """Source page 3: analog curve above a discrete-time stem plot."""
    doc.ensure(205)
    c = doc.c
    x = MARGIN_X + 150
    y_top = doc.y - 10
    w = 205
    h = 78
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.setLineWidth(0.8)

    # Analog signal: source uses crossing axes and one smooth rising curve.
    x0 = x + w * 0.48
    y0 = y_top - h * 0.56
    _axis_arrow(c, x + 15, y0, x + w - 8, y0)
    _axis_arrow(c, x0, y_top - h + 4, x0, y_top - 2)
    path = c.beginPath()
    path.moveTo(x + 28, y0 + 12)
    path.curveTo(x + 66, y0 + 9, x + 94, y0 + 28, x + 126, y0 + 38)
    path.curveTo(x + 149, y0 + 46, x + 164, y0 + 48, x + 177, y0 + 47)
    c.drawPath(path, stroke=1, fill=0)

    # Discrete signal: preserve the source's vertical placement and labels.
    y2 = y_top - 102
    left, right = x + 12, x + w - 8
    base = y2 - 47
    vx = x + w * 0.46
    sample_values = {-2: 0, -1: 0.8, 0: 0.5, 1: 1.5, 2: 0}
    geometry = signal_classification_axis_geometry()
    vertical_top = (
        base
        + max(max(sample_values.values()), geometry["highest_labeled_tick"])
        * geometry["sample_scale"]
        + geometry["vertical_arrow_headroom"]
    )
    _axis_arrow(c, left, base, right, base)
    _axis_arrow(c, vx, base - geometry["vertical_negative_tail"], vx, vertical_top)
    c.setFont("CN", 7.3)
    c.drawString(vx + 7, y2 - 5, "x(n)")
    label_geometry = discrete_axis_label_geometry()
    for n in range(-2, 3):
        px = vx + n * 36
        c.line(px, base - 2, px, base + 2)
        if n == 0:
            offset = label_geometry["origin_tick"]
            c.drawString(px + offset["x_offset"], base + offset["y_offset"], "0")
        else:
            offset = label_geometry["regular_tick"]
            c.drawCentredString(px + offset["x_offset"], base + offset["y_offset"], str(n))
    for n, value in sample_values.items():
        px = vx + n * 36
        py = base + value * geometry["sample_scale"]
        c.line(px, base, px, py)
        c.circle(px, py, 2.3, stroke=1, fill=1)
    for tick_value in (1, 2):
        tick_y = base + tick_value * geometry["sample_scale"]
        c.line(vx, tick_y, vx + 6, tick_y)
        c.drawRightString(vx - 5, tick_y - 2.5, str(tick_value))
    c.drawString(right + 2, base - 10, "n")
    doc.y -= 200


def draw_rect_sequence_example(doc):
    """Source page 7: R_N(n) example for N=2."""
    doc.ensure(122)
    c = doc.c
    x = MARGIN_X + 280
    y = doc.y - 4
    w, h = 170, 92
    left, right = x + 12, x + w - 8
    base = y - h + 26
    vx = x + 38
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.setLineWidth(0.8)
    _axis_arrow(c, left, base, right, base)
    _axis_arrow(c, vx, base - 5, vx, y - 2)
    c.setFont("CN", 7.5)
    c.drawString(vx + 7, y - 8, "R_N(n)")
    label_geometry = discrete_axis_label_geometry()
    for n in range(0, 3):
        px = vx + n * 47
        c.line(px, base - 2, px, base + 2)
        if n == 0:
            offset = label_geometry["origin_tick"]
            c.drawString(px + offset["x_offset"], base + offset["y_offset"], "0")
        else:
            offset = label_geometry["regular_tick"]
            c.drawCentredString(px + offset["x_offset"], base + offset["y_offset"], str(n))
        value = 1 if n in (0, 1) else 0
        py = base + value * 42
        c.line(px, base, px, py)
        c.circle(px, py, 2.5, stroke=1, fill=1)
    c.drawRightString(vx - 7, base + 39, "1")
    c.drawString(right + 3, base - 10, "n")
    c.setFont("CN", 10)
    c.drawString(MARGIN_X + 205, doc.y - 54, "例如 N=2")
    doc.y -= 118


def _draw_source_cosine(c, x, y, w, h, omega, title_path):
    left, right = x + 6, x + w - 7
    base = y - h * 0.53
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.setLineWidth(0.65)
    _axis_arrow(c, left, base, right, base)
    step = (right - left - 10) / 16
    center = (left + right) / 2
    for n in range(-8, 9):
        value = cos(omega * n)
        px = center + n * step
        py = base + value * (h * 0.32)
        c.line(px, base, px, py)
        c.circle(px, py, 1.35, stroke=1, fill=1)
    c.setFont("CN", 6.2)
    c.drawString(right + 1, base + 2, "n")
    im = Image.open(title_path)
    iw, ih = im.size
    scale = min((w - 10) / iw, 12 / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(title_path)), x + (w - dw) / 2, y - 9, dw, dh, mask="auto")


def draw_oscillation_nine(doc):
    """Source page 12: all nine cosine sequence examples in a 3x3 grid."""
    c = doc.c
    titles = [
        formula_png("osc_0", r"x[n]=\cos(0n)=1", 9),
        formula_png("osc_pi8", r"x[n]=\cos(\pi n/8)", 9),
        formula_png("osc_pi4", r"x[n]=\cos(\pi n/4)", 9),
        formula_png("osc_pi2", r"x[n]=\cos(\pi n/2)", 9),
        formula_png("osc_pi", r"x[n]=\cos(\pi n)", 9),
        formula_png("osc_3pi2", r"x[n]=\cos(3\pi n/2)", 9),
        formula_png("osc_7pi4", r"x[n]=\cos(7\pi n/4)", 9),
        formula_png("osc_15pi8", r"x[n]=\cos(15\pi n/8)", 9),
        formula_png("osc_2pi", r"x[n]=\cos(2\pi n)=1", 9),
    ]
    omegas = [0, pi / 8, pi / 4, pi / 2, pi, 3 * pi / 2, 7 * pi / 4, 15 * pi / 8, 2 * pi]
    cell_w, cell_h = 155, 88
    x0 = MARGIN_X + 6
    row_h = 93
    for row in range(3):
        doc.ensure(row_h)
        y0 = doc.y
        for col in range(3):
            i = row * 3 + col
            _draw_source_cosine(c, x0 + col * 164, y0, cell_w, cell_h, omegas[i], titles[i])
        doc.y -= row_h


def draw_scale_transform_triplet(doc):
    """Source page 14: x(n), x(n/2), and x(2n) with source-relative geometry."""
    doc.ensure(142)
    source = {-3: 3, -2: 2, -1: 4, 0: 2, 1: 2, 2: 3, 3: 1}
    expanded = {n: (source[n // 2] if n % 2 == 0 and n // 2 in source else 0) for n in range(-6, 7)}
    compressed = {-1: source[-2], 0: source[0], 1: source[2]}
    items = [
        (source, -4, 4, formula_png("scale_xn", r"x(n)", 11)),
        (expanded, -7, 7, formula_png("scale_xhalf", r"x(n/2)", 11)),
        (compressed, -2, 2, formula_png("scale_x2n", r"x(2n)", 11)),
    ]
    x0 = MARGIN_X + 2
    widths = [150, 188, 150]
    cursor = x0
    for (values, n_min, n_max, title), width in zip(items, widths):
        draw_discrete_axes_plot(
            doc.c,
            cursor,
            doc.y,
            width,
            112,
            values,
            n_min=n_min,
            n_max=n_max,
            title=title,
            x_tick_labels={-1, 0, 1},
            x_tick_positions={-1, 0, 1},
        )
        cursor += width + 6
    doc.y -= 138


def draw_formula_plain(doc, image_path, max_w=None, max_h=34, center=True, gap=12):
    doc.ensure(max_h + gap)
    c = doc.c
    im = Image.open(image_path)
    iw, ih = im.size
    max_w = max_w or CONTENT_W * 0.86
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    x = MARGIN_X + (CONTENT_W - dw) / 2 if center else MARGIN_X
    y = doc.y - dh
    c.drawImage(ImageReader(str(image_path)), x, y, dw, dh, mask="auto")
    doc.y -= dh + gap


def _axis_arrow(c, x1, y1, x2, y2):
    c.line(x1, y1, x2, y2)
    if abs(x2 - x1) >= abs(y2 - y1):
        c.line(x2, y2, x2 - 6, y2 + 3.5)
        c.line(x2, y2, x2 - 6, y2 - 3.5)
    else:
        c.line(x2, y2, x2 - 3.5, y2 - 6)
        c.line(x2, y2, x2 + 3.5, y2 - 6)


def _nice_tick_labels(n_min, n_max):
    nums = list(range(n_min, n_max + 1))
    if len(nums) <= 7:
        return set(nums)
    labels = {0}
    if n_min <= -1 <= n_max:
        labels.add(-1)
    if n_min <= 1 <= n_max:
        labels.add(1)
    labels.add(n_min)
    labels.add(n_max)
    return labels


def discrete_axis_label_geometry():
    """Shared clearances for labels around discrete-time axes."""
    return {
        "origin_tick": {"x_offset": 5, "y_offset": -20, "anchor": "left"},
        "regular_tick": {"x_offset": 0, "y_offset": -13},
        "positive_zero_sample_value": {"x_offset": -6, "y_offset": -2},
    }


def discrete_axis_geometry():
    """Physical clearances shared by every discrete-time stem axis."""
    return {
        "minimum_vertical_arrow_clearance": 12.0,
    }


def fit_axis_range_for_clearance(
    value_min,
    value_max,
    sample_max,
    plot_span,
    minimum_clearance,
):
    """Expand the upper value range until the rendered gap is large enough."""
    if plot_span <= minimum_clearance or value_max <= value_min:
        return value_min, value_max
    usable_fraction = (plot_span - minimum_clearance) / plot_span
    required_max = value_min + (sample_max - value_min) / usable_fraction
    return value_min, max(value_max, required_max)


def draw_discrete_axes_plot(
    c,
    x,
    y,
    w,
    h,
    values,
    n_min=None,
    n_max=None,
    title=None,
    value_labels=True,
    x_tick_labels=None,
    x_tick_positions=None,
    axis_v_min=None,
    axis_v_max=None,
    title_position="below",
    value_label_offsets=None,
):
    """Draw a discrete-time stem plot in the original handout style."""
    if not values:
        return
    if n_min is None:
        n_min = min(values)
    if n_max is None:
        n_max = max(values)
    n_min = min(n_min, min(values), 0)
    n_max = max(n_max, max(values), 0)
    v_min = min(0, min(values.values()))
    v_max = max(1, max(values.values()))
    if v_min == v_max:
        v_max = v_min + 1

    pad_l, pad_r, pad_t, pad_b = 16, 15, 18, 24
    left, right = x + pad_l, x + w - pad_r
    top, bottom = y - pad_t, y - h + pad_b
    x_span = right - left
    y_span = top - bottom
    # Keep arrow heads outside the last tick/sample.  The old padding made the
    # right arrow touch the terminal stem and the vertical arrow touch n=0.
    n_pad = max(1.25, (n_max - n_min) * 0.18)
    v_bottom_pad = max(0.25, (v_max - v_min) * 0.12)
    v_top_pad = max(1.35, (v_max - v_min) * 0.82)
    axis_n_min = n_min - n_pad
    axis_n_max = n_max + n_pad
    axis_v_min = v_min - v_bottom_pad if axis_v_min is None else axis_v_min
    axis_v_max = v_max + v_top_pad if axis_v_max is None else axis_v_max
    geometry = discrete_axis_geometry()
    axis_v_min, axis_v_max = fit_axis_range_for_clearance(
        value_min=axis_v_min,
        value_max=axis_v_max,
        sample_max=max(values.values()),
        plot_span=y_span,
        minimum_clearance=geometry["minimum_vertical_arrow_clearance"],
    )

    x0 = left + (0 - axis_n_min) / (axis_n_max - axis_n_min or 1) * x_span
    y0 = bottom + (0 - axis_v_min) / (axis_v_max - axis_v_min or 1) * y_span

    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.setLineWidth(0.9)
    _axis_arrow(c, left, y0, right, y0)
    _axis_arrow(c, x0, bottom, x0, top)

    c.setFont("CN", 7.6)
    tick_labels = _nice_tick_labels(n_min, n_max) if x_tick_labels is None else set(x_tick_labels)
    tick_positions = set(range(n_min, n_max + 1)) if x_tick_positions is None else set(x_tick_positions)
    label_geometry = discrete_axis_label_geometry()
    for n in range(n_min, n_max + 1):
        px = left + (n - axis_n_min) / (axis_n_max - axis_n_min or 1) * x_span
        if n in tick_positions:
            c.line(px, y0 - 2.2, px, y0 + 2.2)
        if n in tick_labels:
            if n == 0:
                offset = label_geometry["origin_tick"]
                c.drawString(px + offset["x_offset"], y0 + offset["y_offset"], "0")
            else:
                offset = label_geometry["regular_tick"]
                c.drawCentredString(px + offset["x_offset"], y0 + offset["y_offset"], str(n))

    for n, v in sorted(values.items()):
        px = left + (n - axis_n_min) / (axis_n_max - axis_n_min or 1) * x_span
        py = bottom + (v - axis_v_min) / (axis_v_max - axis_v_min or 1) * y_span
        c.setLineWidth(1.0)
        c.line(px, y0, px, py)
        c.circle(px, py, 2.8, stroke=1, fill=1)
        if value_labels and abs(v) > 1e-8:
            if value_labels == "ones":
                if abs(abs(v) - 1) > 1e-6:
                    continue
                label = "1" if v > 0 else "-1"
            else:
                label = f"{v:g}" if isinstance(v, float) else str(v)
            label_dx, label_dy = (value_label_offsets or {}).get(n, (0, 0))
            if n == 0 and v > 0:
                offset = label_geometry["positive_zero_sample_value"]
                c.drawRightString(
                    px + offset["x_offset"] + label_dx,
                    py + offset["y_offset"] + label_dy,
                    label,
                )
            else:
                c.drawCentredString(px + label_dx, py + (7 if v >= 0 else -14) + label_dy, label)

    c.setFont("CN", 7.5)
    c.drawString(right + 3, y0 + 4, "n")
    if title:
        if isinstance(title, Path):
            im = Image.open(title)
            iw, ih = im.size
            scale = min(82 / iw, 15 / ih)
            dw, dh = iw * scale, ih * scale
            if title_position == "axis_top":
                title_x = x0 + 10
                title_y = top - dh + 2
            else:
                title_x = x + (w - dw) / 2
                title_y = y - h - 7
            c.drawImage(ImageReader(str(title)), title_x, title_y, dw, dh, mask="auto")
        else:
            c.setFillColor(colors.black)
            c.setFont("CN", 9.0)
            if title_position == "axis_top":
                c.drawString(x0 + 10, top - 8, title)
            else:
                c.drawCentredString(x + w / 2, y - h - 8, title)


def draw_example2_plot(doc):
    doc.ensure(168)
    c = doc.c
    draw_discrete_axes_plot(
        c,
        MARGIN_X + 150,
        doc.y - 18,
        300,
        150,
        {-1: 1, 0: 4, 1: -2},
        n_min=-2,
        n_max=2,
        title=formula_png("sample_ex2_plot_label", r"x(1-2n)", 11),
        x_tick_labels={-1, 0, 1},
        x_tick_positions={-1, 0, 1},
        axis_v_min=-3.2,
        axis_v_max=6.4,
        title_position="axis_top",
        value_label_offsets={-1: (3, 0)},
    )
    doc.y -= 168


def draw_stem(c, x, y, w, h, values, n_min, n_max, title="", value_labels=True):
    draw_discrete_axes_plot(c, x, y, w, h, values, n_min=n_min, n_max=n_max, title=title, value_labels=value_labels)


def stem_block(doc):
    doc.ensure(130)
    draw_stem(doc.c, MARGIN_X + 66, doc.y, 360, 105, {-1: 1, 0: 2, 1: 1, 2: 3}, -2, 3, "例：{1, 2, 1, 3}，其中 n=0 对应第二项")
    doc.y -= 134


def oscillation_block(doc):
    doc.ensure(100)
    x0 = MARGIN_X + 10
    labels = [
        formula_png("omega_0", r"\omega=0", 10),
        formula_png("omega_pi_4", r"\omega=\frac{\pi}{4}", 10),
        formula_png("omega_pi_2", r"\omega=\frac{\pi}{2}", 10),
        formula_png("omega_pi", r"\omega=\pi", 10),
    ]
    for i, om in enumerate([0, pi / 4, pi / 2, pi]):
        vals = {n: cos(om * n) for n in range(0, 9)}
        draw_stem(doc.c, x0 + i * 118, doc.y, 104, 86, vals, 0, 8, labels[i], value_labels="ones")
    doc.y -= 103


def append_chapter3_intro(doc, formula, superposition, homogeneity, linearity):
    """Use the remaining sample-tail space for the next chapter opening."""
    doc.section = "3. 时域离散系统"
    doc.h1("03 时域离散系统")
    doc.p("设输入为 x(n)，经过时域离散系统后的输出为 y(n)，输入和输出的关系可写为：")
    draw_formula_plain(doc, formula, max_h=28, gap=6)
    doc.ensure(82, section="3. 时域离散系统")
    c=doc.c; cy=doc.y-36; x=MARGIN_X+110
    c.setStrokeColor(colors.black); c.setLineWidth(0.9)
    c.line(x-62,cy,x,cy)
    c.line(x+135,cy,x+205,cy)
    c.line(x-8,cy+4,x,cy); c.line(x-8,cy-4,x,cy)
    c.line(x+197,cy+4,x+205,cy); c.line(x+197,cy-4,x+205,cy)
    c.rect(x,cy-22,135,44,stroke=1,fill=0)
    c.setFont("CN",9); c.setFillColor(TEXT)
    c.drawString(x-42,cy+13,"x(n)")
    draw_centered_multiline_text(c, x+67.5, cy, "T[·]", "CN", 9, color=TEXT)
    c.drawString(x+154,cy+13,"y(n)")
    doc.y-=72
    doc.h2("3.1 线性（考点）")
    doc.p("系统线性等价于同时满足叠加性和齐次性。")
    doc.h3("1. 叠加性")
    draw_formula_plain(doc, superposition, max_h=24, gap=4)
    doc.h3("2. 齐次性")
    draw_formula_plain(doc, homogeneity, max_h=24, gap=4)
    doc.p("若同时满足以上两条，则系统满足线性组合关系：",size=9.2,leading=13)
    draw_formula_plain(doc, linearity, max_h=25, gap=4)


def build_pdf():
    register_fonts()
    f_sampling = formula_png(
        "sampling",
        r"x[n]=x_a(t)|_{t=nT}=x_a(nT),\qquad n\in\mathbf{Z}",
        15,
    )
    f_period_1 = formula_png(
        "period_1",
        r"e^{j\omega(n+N)}=e^{j\omega n}\quad\Longleftrightarrow\quad e^{j\omega N}=1",
        15,
    )
    f_period_2 = formula_png(
        "period_2",
        r"\omega N=2\pi k,\ k\in\mathbf{Z}\quad\Longleftrightarrow\quad \frac{2\pi}{\omega}\in\mathbf{Q}",
        15,
    )
    f_delta = piecewise_png("seq_delta_piecewise_ref", r"\delta[n]=", r"1,\ n=0", r"0,\ n\ne0", fontsize=18)
    f_step = piecewise_png("seq_step_piecewise_ref", r"u[n]=", r"1,\ n\geq0", r"0,\ n<0", fontsize=18)
    f_rect = piecewise_png("seq_rect_piecewise_ref", r"R_N(n)=", r"1,\ 0\leq n\leq N-1", row2_cn="其他", fontsize=18)
    f_real_exp = formula_png("seq_real_exp", r"x(n)=a^n u(n)", 16)
    f_sin = formula_png("seq_sin", r"x(n)=\sin(\omega n)", 16)
    f_complex_exp = formula_png("seq_complex_exp", r"x(n)=C e^{j\omega n}", 16)
    f_rule_frac = formula_png("rule_frac", r"\frac{2\pi}{\omega}", 14)
    f_rule_ab_eq = formula_png("rule_ab_eq", r"\frac{2\pi}{\omega}=\frac{A}{B}", 14)
    f_ex1_a = formula_png("ex1_a", r"e^{j5n}:\ \frac{2\pi}{5}", 14)
    f_ex1_b = formula_png("ex1_b", r"e^{j\frac{2\pi n}{12}}:\ \frac{2\pi}{\frac{2\pi}{12}}=12", 14)
    f_ex1_c = formula_png("ex1_c", r"e^{j\frac{8\pi n}{31}}:\ \frac{2\pi}{\frac{8\pi}{31}}=\frac{31}{4}", 14)
    f_ex2_given = piecewise3_cn_png(
        "sample_ex2_given",
        r"x(n)=",
        r"3n+1,\ -1\leq n\leq1",
        r"1,\ 2\leq n\leq3",
        row3_cn="其余",
        fontsize=17,
    )
    f_ex2_case1 = formula_png("sample_ex2_case1", r"-1\leq 1-2n\leq1\quad\Rightarrow\quad 0\leq n\leq1", 14)
    f_ex2_value1 = formula_png("sample_ex2_value1", r"x(1-2n)=4-6n,\quad n=0,1", 14)
    f_ex2_case2 = formula_png("sample_ex2_case2", r"2\leq 1-2n\leq3\quad\Rightarrow\quad -1\leq n\leq-\frac{1}{2}", 14)
    f_ex2_value2 = formula_png("sample_ex2_value2", r"x(1-2n)=1,\quad n=-1", 14)
    f_system_intro = formula_png("sample_ch3_system", r"y(n)=T[x(n)]", 17)
    f_super_intro = formula_png("sample_ch3_super", r"T[x_1(n)+x_2(n)]=y_1(n)+y_2(n)", 13)
    f_homo_intro = formula_png("sample_ch3_homo", r"T[a x(n)]=a y(n)", 13)
    f_linear_intro = formula_png("sample_ch3_linear", r"T[a x_1(n)+b x_2(n)]=a y_1(n)+b y_2(n)", 14)

    doc = Doc(PDF_PATH)
    doc.start()

    doc.h2("1.1 信号的分类")
    doc.p("数字信号处理的对象可以从“时间变量是否连续”和“幅值是否连续”两个角度分类。理解这一点，是学习采样、量化和离散系统分析的入口。")
    doc.table(
        ["类型", "时间变量", "幅值", "典型说明"],
        [
            ["模拟信号", "连续", "连续", "传感器输出、语音电压等"],
            ["时域离散信号", "离散", "可连续取值", "由采样得到，尚未量化"],
            ["数字信号", "离散", "离散", "采样后再量化、编码得到"],
        ],
        [96, 122, 122, 159],
        36,
    )
    draw_signal_classification_examples(doc)
    doc.bullet([
        "数字信号一定是时域离散的，但时域离散信号不一定是数字信号。",
        "采样只让时间变量离散化；量化和编码才让幅值以数字形式表示。",
    ])

    doc.h2("1.2 模拟信号的数字处理")
    doc.p("实际系统中，许多输入和输出仍然是模拟量。数字信号处理方法的基本思想，是先把模拟信号转换成数字序列，在数字域完成处理，再按需要恢复为模拟信号。")
    draw_flow(doc)
    doc.bullet([
        "预滤波：限制输入带宽，降低混叠风险。",
        "A/D 转换：通常包括采样、量化、编码三个步骤。",
        "数字处理：在离散时间/数字域完成滤波、频谱分析、调制解调等运算。",
        "D/A 与平滑滤波：将数字序列转换成连续时间信号，并抑制重构后的阶梯和高频分量。",
    ])
    doc.note("814 考法提示", "采样类题目常把采样频率、最高频率、混叠和理想重构放在一起考。复习时同时记住 f_s ≥ 2f_m 的条件，以及数字频率 Ω = ωT 的映射关系。", compact=True)

    doc.section = "2. 时域离散信号"
    doc.h2("2.1 时域离散信号的表示")
    doc.p("设连续时间模拟输入信号，以采样间隔 T 等间隔取样，得到的时域离散信号可写为")
    doc.formula_box(f_sampling, 36)
    doc.p("这里 n 是整数序号，T 是相邻两次采样之间的时间间隔。原课件中常写作 x(n)，本讲义统一采用更常见的离散时间记号 x[n]，含义不变。")
    doc.bullet([
        "集合表示：用 {x[n]} 或列出若干样值，通常用下划线或标注说明 n=0 的位置。",
        "函数表示：给出 x[n] 关于 n 的表达式，例如 x[n]=n+1。",
        "图形表示：用离散竖线图表示每个整数 n 上的样值。",
    ])
    stem_block(doc)

    doc.h2("2.2 常用离散序列")
    doc.table(
        ["序列", "定义", "说明"],
        [
            ["单位脉冲 δ[n]", f_delta, "离散系统中最基本的测试序列。"],
            ["单位阶跃 u[n]", f_step, "常用于表示因果序列。"],
            ["矩形序列 R_N[n]", f_rect, "长度为 N 的有限长序列。"],
            ["实指数序列", f_real_exp, "a 的大小决定衰减或增长。"],
            ["正弦序列", f_sin, "离散频率以 2π 为周期。"],
            ["复指数序列", f_complex_exp, "判断周期性时注意频率与 2π 的比值是否为有理数。"],
        ],
        [95, 255, 149],
        36,
    )
    draw_rect_sequence_example(doc)
    doc.p("这些序列既是离散系统分析的基本积木，也是卷积、差分方程、频域变换中的常用输入。后续讨论系统响应时，单位脉冲响应 h[n] 将起到核心作用。")

    doc.ensure(220)
    doc.h2("2.3 复指数序列的周期")
    doc.p("若存在正整数 N，使复指数序列在所有整数 n 上重复，则称该序列为周期序列，最小的正整数 N 称为基波周期。")
    doc.formula_box(f_period_1, 36)
    doc.formula_box(f_period_2, 36)
    doc.formula_bullets([
        (f_rule_frac, "为无理数，则该复指数序列不是周期序列。"),
        (f_rule_frac, "为整数，则该整数就是周期。"),
        (f_rule_ab_eq, "且 A、B 互素，则最小周期为 A。"),
    ])
    doc.h3("例 1  求下列序列的周期")
    doc.y -= 8
    doc.formula_bullets([
        (f_ex1_a, "为无理数，因此不是周期序列。"),
        (f_ex1_b, "最小周期 N=12。"),
        (f_ex1_c, "最小周期 N=31。"),
    ])
    doc.note("考点连接", "离散时间频率以 2π 为周期，ω 与 ω+2πm 对应同一个序列。这个性质会在 DTFT、DFT 和采样频谱题中反复出现。", compact=True)

    doc.h2("2.3-2.4 振荡速率与序列运算")
    doc.p("连续时间正弦信号的频率越大，振荡越快；但在离散时间中，频率以 2π 为周期。通常只需关注 0 到 π 的频率范围，超过 π 后会与低频序列发生等价或折叠关系。")
    draw_oscillation_nine(doc)
    doc.bullet([
        "相加：c[n]=a[n]+b[n]，要求在同一 n 上逐点相加。",
        "相乘：c[n]=a[n]b[n]，要求在同一 n 上逐点相乘。",
        "移位：x[n-n0] 表示原序列右移 n0 个单位；x[n+n0] 表示原序列左移 n0 个单位。",
    ])

    doc.h2("2.4 序列的变换")
    doc.bullet([
        "翻转：x[-n] 是 x[n] 关于 n=0 的镜像。",
        "抽取：x[Mn] 只保留原序列中序号能被 M 对应取到的样值，常表现为时间轴压缩。",
        "插值：当自变量为 n 与 M 的比值时，可理解为在相邻样值之间插入 M-1 个零，再按新的整数序号表示。",
    ])
    doc.p("处理复合变换时，建议先看括号内的新自变量，例如 x[1-2n]；再列出使 1-2n 落入原序列非零区间的整数 n。这样比直接凭直觉平移、翻转更稳。")
    draw_scale_transform_triplet(doc)
    doc.ensure(55)
    doc.h3("例 2  画出 x[1-2n] 的图像")
    doc.p("已知序列如下，画出 x(1-2n) 的图像。", size=9.2, leading=13)
    draw_formula_plain(doc, f_ex2_given, max_h=62, gap=6)
    doc.h3("解")
    draw_formula_plain(doc, f_ex2_case1, max_h=22, gap=5)
    draw_formula_plain(doc, f_ex2_value1, max_h=22, gap=5)
    draw_formula_plain(doc, f_ex2_case2, max_h=22, gap=5)
    draw_formula_plain(doc, f_ex2_value2, max_h=22, gap=5)
    draw_example2_plot(doc)
    append_chapter3_intro(doc, f_system_intro, f_super_intro, f_homo_intro, f_linear_intro)

    doc.save()

    NOTE_PATH.write_text(
        """# DSP讲义重制_样章_校对记录

## 本次调整

- 将样章改为连续讲义排版：页面剩余空间会接入下一节内容，减少大面积空白。
- 删除样章说明后改为连续排版：第一页剩余空间直接接入第二章开头，避免大面积空白。
- 关键公式已用 matplotlib mathtext 渲染为透明数学公式图后嵌入 PDF，不再显示为原始代码式文本。
- 公式统一采用参考讲义的衬线数学字体风格；分段函数大括号右侧紧接取值，不留大段空白。
- 流程图所有节点统一白底蓝框，避免中间节点浅蓝填充不一致。
- 单位脉冲、单位阶跃、矩形序列已改为分段函数；实指数、正弦、复指数序列已改为数学公式。
- 所有比值和除法在版面中使用分数形式，不使用斜杠形式。
- 例 2 已补全解题步骤和最终图像；例题下方只保留适当书写空白，不加横线或大边框。
- 删除首页“处理原则”提示框。
- 保留“教材讲义风”主视觉：A4 纵向、蓝色标题层级、表格、流程图、离散序列图。
- 例题仍按普通小节呈现，不做大边框。
- 华理 814 相关提示只保留在采样与离散频率周期等相关位置。

## 样章范围

- 原始文件：`C:\\Users\\HP\\Desktop\\DPS课件\\DSP课件.pdf`
- 范围：前 15 页 PPT 内容
- 参考文件：`C:\\Users\\HP\\Desktop\\讲义、做题本\\华理814真题.pdf`
- 输出：`outputs/DSP讲义重制_样章_前15页_流程图白底版.pdf`
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    build_pdf()
    print(PDF_PATH)
