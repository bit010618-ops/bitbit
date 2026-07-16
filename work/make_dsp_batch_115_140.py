from pathlib import Path
import sys
import math

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
    PAGE_W,
    TEXT,
    draw_auto_math_text,
    formula_png,
    piecewise_png,
    register_fonts,
    wrap,
)
from make_dsp_batch_016_024 import BatchDoc, draw_formula
from make_dsp_batch_046_088 import draw_red_text
from make_dsp_batch_089_112 import draw_formula_left, draw_formula_rows


PDF_PATH = OUT_DIR / "DSP讲义重制_第五批_原PPT115-140页_频率响应与滤波器设计_内容版.pdf"
NOTE_PATH = OUT_DIR / "DSP讲义重制_第五批_原PPT115-140页_频率响应与滤波器设计_校对记录.md"


def f(name, expr, size=14, color="#111111"):
    return formula_png(f"b115_{name}", expr, size, color=color)


def para_red(doc, parts, size=9.4, leading=16):
    """Draw one or more lines with inline red emphasis. parts: [(text, color_name)]."""
    doc.ensure(leading * 3 + 8)
    c = doc.c
    x = MARGIN_X
    y = doc.y
    line_h = leading
    for text, color_name in parts:
        font = "CNB" if color_name in ("red", "blue", "purple") else "CN"
        if color_name == "red":
            fill = colors.HexColor("#D71920")
        elif color_name == "blue":
            fill = BLUE
        elif color_name == "purple":
            fill = colors.HexColor("#7B3FC6")
        else:
            fill = TEXT
        for line in wrap(text, MARGIN_X + CONTENT_W - x, font, size):
            width = draw_auto_math_text(
                c, x, y, line,
                font=font, size=size, color=fill,
            )
            x += width
            if x >= MARGIN_X + CONTENT_W - 2:
                x = MARGIN_X
                y -= line_h
    doc.y = y - line_h - 5
    c.setFillColor(TEXT)


def note_box(doc, title, text):
    lines = wrap(text, CONTENT_W - 26, "CN", 9.2)
    h = 30 + 15 * len(lines)
    doc.ensure(h + 12)
    c = doc.c
    x = MARGIN_X
    y = doc.y - h
    c.setStrokeColor(colors.HexColor("#A5D4FF"))
    c.setFillColor(colors.HexColor("#EEF8FF"))
    c.roundRect(x, y, CONTENT_W, h, 4, stroke=1, fill=1)
    c.setFillColor(BLUE_DARK)
    c.setFont("CNB", 9.6)
    c.drawString(x + 12, y + h - 20, title)
    c.setFillColor(TEXT)
    c.setFont("CN", 9.2)
    yy = y + h - 38
    for line in lines:
        c.drawString(x + 12, yy, line)
        yy -= 15
    doc.y = y - 12


def draw_homework_columns(doc, left_title, left_items, right_title, right_items):
    col_gap = 22
    col_w = (CONTENT_W - col_gap) / 2
    font = "CN"
    size = 8.2
    leading = 13

    def layout(items):
        rows = []
        for item in items:
            lines = wrap(item, col_w - 18, font, size)
            rows.append(lines)
        return rows

    left_rows = layout(left_items)
    right_rows = layout(right_items)
    left_count = 2 + sum(len(row) for row in left_rows)
    right_count = 2 + sum(len(row) for row in right_rows)
    height = max(left_count, right_count) * leading + 8
    doc.ensure(height)
    c = doc.c
    top = doc.y

    for col, title, rows in ((0, left_title, left_rows), (1, right_title, right_rows)):
        x = MARGIN_X + col * (col_w + col_gap)
        y = top
        c.setFillColor(TEXT)
        c.setFont("CNB", 9)
        c.drawString(x, y, title)
        y -= leading + 2
        c.setFont(font, size)
        for lines in rows:
            c.circle(x + 3, y + 3, 1.5, stroke=0, fill=1)
            for line_index, line in enumerate(lines):
                c.drawString(x + 11, y, line)
                y -= leading
            if not lines:
                y -= leading
    doc.y = top - height - 4


def draw_unit_circle(doc, zeros=None, poles=None, caption="", w=165, h=120):
    zeros = zeros or []
    poles = poles or []
    doc.ensure(h + 24)
    c = doc.c
    x = MARGIN_X + 35
    y = doc.y - 18
    cx = x + w / 2
    cy = y - h / 2
    r = min(w, h) * 0.34
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.white)
    c.setLineWidth(1)
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.line(cx - r - 26, cy, cx + r + 34, cy)
    c.line(cx + r + 34, cy, cx + r + 26, cy + 4)
    c.line(cx + r + 34, cy, cx + r + 26, cy - 4)
    c.line(cx, cy - r - 20, cx, cy + r + 22)
    c.line(cx, cy + r + 22, cx - 4, cy + r + 14)
    c.line(cx, cy + r + 22, cx + 4, cy + r + 14)
    c.setFillColor(colors.black)
    c.setFont("CN", 8.2)
    c.drawString(cx + r + 38, cy - 4, "Re[z]")
    c.drawString(cx + 4, cy + r + 24, "j Im[z]")
    c.drawCentredString(cx + r + 3, cy - 12, "1")
    c.drawCentredString(cx - r - 7, cy - 12, "-1")
    for ang, label in zeros:
        px = cx + r * math.cos(ang)
        py = cy + r * math.sin(ang)
        c.setStrokeColor(colors.red)
        c.line(px - 4, py - 4, px + 4, py + 4)
        c.line(px - 4, py + 4, px + 4, py - 4)
        if label:
            c.setFillColor(colors.black)
            label_y = py - 10 if label == "-ω0" else py + 4
            draw_auto_math_text(
                c, px + 5, label_y, label,
                font="CN", size=8.2, color=colors.black,
            )
    for ang, rad, label in poles:
        px = cx + r * rad * math.cos(ang)
        py = cy + r * rad * math.sin(ang)
        c.setFillColor(colors.black)
        c.circle(px, py, 3, stroke=1, fill=1)
        if label:
            draw_auto_math_text(
                c, px + 5, py + 4, label,
                font="CN", size=8.2, color=colors.black,
            )
    if caption:
        draw_auto_math_text(
            c, cx, cy - r - 28, caption,
            font="CN", size=8.6, color=TEXT, align="center",
        )
    doc.y -= h + 42


def draw_unit_and_response(doc, mode):
    doc.ensure(120)
    c = doc.c
    top = doc.y
    # Left zero-pole sketch.
    x0 = MARGIN_X + 50
    y0 = top - 12
    cx, cy, r = x0 + 88, y0 - 55, 42
    c.setStrokeColor(colors.blue)
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.setStrokeColor(colors.blue)
    c.line(cx - r - 18, cy, cx + r + 18, cy)
    c.line(cx, cy - r - 16, cx, cy + r + 18)
    c.setFillColor(colors.black)
    c.setFont("CN", 8)
    c.drawString(cx + r + 20, cy - 4, "Re[z]")
    c.drawString(cx + 4, cy + r + 18, "j Im[z]")
    z_ang = math.pi if mode == "lp_zero" else 0
    px = cx + r * math.cos(z_ang)
    py = cy + r * math.sin(z_ang)
    c.setStrokeColor(colors.red)
    c.circle(px, py, 4, stroke=1, fill=0)
    c.setStrokeColor(colors.red)
    c.line(cx - 4, cy - 4, cx + 4, cy + 4)
    c.line(cx - 4, cy + 4, cx + 4, cy - 4)
    # Right amplitude sketch.
    x1 = MARGIN_X + 290
    by = top - 94
    c.setStrokeColor(colors.red)
    c.line(x1, by, x1 + 210, by)
    c.line(x1, by, x1, by + 78)
    c.line(x1 + 210, by, x1 + 202, by + 4)
    c.line(x1 + 210, by, x1 + 202, by - 4)
    c.line(x1, by + 78, x1 - 4, by + 70)
    c.line(x1, by + 78, x1 + 4, by + 70)
    c.setFillColor(colors.black)
    c.setFont("CN", 8)
    c.drawString(x1 + 224, by - 4, "ω")
    c.drawString(x1 + 224, by - 14, "(rad)")
    c.drawString(x1 + 224, by - 25, "f (Hz)")
    mid_x = x1 + 100
    c.drawCentredString(x1, by - 12, "0")
    c.drawCentredString(mid_x, by - 12, "π")
    c.drawCentredString(x1 + 200, by - 12, "2π")
    half_fs_path = formula_png("b5_half_sampling_frequency", r"\frac{f_s}{2}", 16)
    fs_path = formula_png("b5_sampling_frequency", r"f_s", 16)
    for label_path, center_x in (
        (half_fs_path, mid_x),
        (fs_path, x1 + 200),
    ):
        label_image = Image.open(label_path)
        label_scale = min(44 / label_image.width, 20 / label_image.height)
        label_width = label_image.width * label_scale
        label_height = label_image.height * label_scale
        c.drawImage(
            ImageReader(str(label_path)),
            center_x - label_width / 2,
            by - 36,
            label_width,
            label_height,
            mask="auto",
        )
    c.drawRightString(x1 - 5, by + 57, "1")
    title_path = formula_png("b5_response_axis_title", r"|H(e^{j\omega})|", 10)
    title_image = Image.open(title_path)
    title_scale = min(72 / title_image.width, 14 / title_image.height)
    c.drawImage(
        ImageReader(str(title_path)),
        x1 + 8,
        by + 67,
        title_image.width * title_scale,
        title_image.height * title_scale,
        mask="auto",
    )
    c.setStrokeColor(colors.red)
    c.setDash(2, 2)
    if mode == "lp_zero":
        c.line(x1 + 200, by, x1 + 200, by + 60)
        c.line(mid_x, by, mid_x, by - 8)
    else:
        c.line(mid_x, by, mid_x, by + 60)
    c.setDash()
    c.setStrokeColor(colors.blue)
    pts = []
    for i in range(0, 160):
        t = i / 159
        xx = x1 + 200 * t
        if mode == "lp_zero":
            val = abs(math.cos(math.pi * t))
        else:
            val = abs(math.sin(math.pi * t))
        yy = by + 60 * val
        pts.append((xx, yy))
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1])
    doc.y -= 128


def draw_comb_diagrams(doc):
    doc.ensure(145)
    c = doc.c
    x0 = MARGIN_X + 55
    y0 = doc.y - 18
    cx, cy, r = x0 + 95, y0 - 62, 44
    c.setStrokeColor(colors.blue)
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.line(cx - r - 18, cy, cx + r + 28, cy)
    c.line(cx, cy - r - 18, cx, cy + r + 22)
    c.setStrokeColor(colors.red)
    for k in range(8):
        ang = 2 * math.pi * k / 8
        px, py = cx + r * math.cos(ang), cy + r * math.sin(ang)
        c.circle(px, py, 3, stroke=1, fill=0)
    c.line(cx - 5, cy - 5, cx + 5, cy + 5)
    c.line(cx - 5, cy + 5, cx + 5, cy - 5)
    c.setFillColor(colors.black)
    c.setFont("CN", 8.2)
    c.drawString(cx + r + 30, cy - 4, "Re[z]")
    c.drawString(cx + 4, cy + r + 24, "j Im[z]")
    draw_auto_math_text(c, cx, cy - r - 18, "N=8", font="CN", size=8.2, align="center")
    # Comb response.
    x1 = MARGIN_X + 285
    by = y0 - 102
    c.setStrokeColor(colors.blue)
    c.line(x1, by, x1 + 245, by)
    c.line(x1, by, x1, by + 92)
    c.line(x1 + 245, by, x1 + 237, by + 4)
    c.line(x1 + 245, by, x1 + 237, by - 4)
    c.setFillColor(colors.black)
    c.setFont("CN", 8.2)
    c.drawString(x1 + 250, by - 4, "ω")
    draw_auto_math_text(c, x1 + 5, by + 90, "|H(e^{jω})|", font="CN", size=8.2)
    c.drawCentredString(x1, by - 12, "0")
    c.drawCentredString(x1 + 122, by - 12, "π")
    c.drawCentredString(x1 + 235, by - 12, "2π")
    c.setStrokeColor(colors.magenta)
    last = None
    for i in range(0, 240):
        t = i / 239
        val = abs(math.sin(8 * math.pi * t))
        xx = x1 + 225 * t
        yy = by + 58 * val
        if last:
            c.line(last[0], last[1], xx, yy)
        last = (xx, yy)
    doc.y -= 152


def draw_s_z_mapping(doc):
    doc.ensure(132)
    c = doc.c
    x0, y0 = MARGIN_X + 25, doc.y - 15
    # s-plane.
    c.setStrokeColor(colors.black)
    c.line(x0, y0 - 64, x0 + 145, y0 - 64)
    c.line(x0 + 70, y0 - 105, x0 + 70, y0 - 20)
    c.setFillColor(colors.HexColor("#B3ECFF"))
    c.rect(x0 + 5, y0 - 102, 62, 76, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#FFB6D9"))
    c.rect(x0 + 73, y0 - 102, 62, 76, stroke=0, fill=1)
    c.setStrokeColor(colors.black)
    c.line(x0, y0 - 64, x0 + 145, y0 - 64)
    c.line(x0 + 70, y0 - 105, x0 + 70, y0 - 20)
    c.setFillColor(colors.black)
    c.setFont("CN", 8.4)
    c.drawString(x0 + 135, y0 - 59, "σ")
    c.drawString(x0 + 74, y0 - 18, "jω")
    c.drawCentredString(x0 + 40, y0 - 58, "①")
    c.drawCentredString(x0 + 105, y0 - 58, "②")
    c.drawCentredString(x0 + 70, y0 - 114, "s 平面")
    # z-plane.
    x1 = MARGIN_X + 300
    cx, cy, r = x1 + 90, y0 - 65, 40
    c.setFillColor(colors.HexColor("#FFB6D9"))
    c.rect(x1 + 18, y0 - 105, 145, 82, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#B3ECFF"))
    c.circle(cx, cy, r, stroke=0, fill=1)
    c.setStrokeColor(colors.red)
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.setStrokeColor(colors.black)
    c.line(x1 + 16, cy, x1 + 165, cy)
    c.line(cx, y0 - 110, cx, y0 - 18)
    c.setFillColor(colors.black)
    c.drawString(x1 + 165, cy - 4, "Re z")
    c.drawString(cx + 4, y0 - 17, "j Im z")
    c.drawCentredString(cx - 18, cy, "①")
    c.drawCentredString(cx + 52, cy - 35, "②")
    c.drawCentredString(cx, y0 - 116, "z 平面")
    doc.y -= 138


def draw_strip_mapping(doc):
    doc.ensure(128)
    c = doc.c
    x0 = MARGIN_X + 95
    y = doc.y - 20
    c.setStrokeColor(colors.black)
    c.line(x0, y - 92, x0, y - 8)
    c.line(x0 - 35, y - 50, x0 + 55, y - 50)
    c.setFillColor(colors.HexColor("#F6A6A6"))
    c.rect(x0 - 34, y - 74, 45, 22, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#9DF18D"))
    c.rect(x0 - 34, y - 36, 45, 22, stroke=0, fill=1)
    c.setFillColor(colors.black)
    c.setFont("CN", 8.2)
    for yy, lab in [(y - 18, "π/T"), (y - 50, "0"), (y - 82, "-π/T")]:
        draw_auto_math_text(
            c, x0 + 8, yy, lab, font="CN", size=8.2,
            color=colors.black, math_size=10.5, math_height=13,
        )
    c.drawCentredString(x0 + 7, y - 105, "s 平面水平条带")
    # z rectangle.
    x1 = MARGIN_X + 300
    c.setFillColor(colors.HexColor("#E044D8"))
    c.rect(x1, y - 90, 120, 78, stroke=1, fill=1)
    c.setStrokeColor(colors.black)
    c.line(x1 + 60, y - 90, x1 + 60, y - 12)
    c.line(x1, y - 50, x1 + 120, y - 50)
    c.setFillColor(colors.black)
    c.drawString(x1 + 124, y - 54, "Re[z]")
    c.drawString(x1 + 62, y - 9, "Im[z]")
    c.drawCentredString(x1 + 60, y - 105, "整个 z 平面")
    # Arrows.
    c.setStrokeColor(colors.black)
    c.line(x0 + 75, y - 38, x1 - 20, y - 35)
    c.line(x1 - 20, y - 35, x1 - 28, y - 31)
    c.line(x1 - 20, y - 35, x1 - 28, y - 40)
    c.line(x0 + 75, y - 62, x1 - 20, y - 65)
    c.line(x1 - 20, y - 65, x1 - 28, y - 61)
    c.line(x1 - 20, y - 65, x1 - 28, y - 70)
    doc.y -= 132


def draw_filter_map(doc):
    doc.ensure(170)
    c = doc.c
    y = doc.y - 24
    center_x = MARGIN_X + CONTENT_W / 2
    center_y = y - 70
    left_x = MARGIN_X + 42
    right_x = MARGIN_X + CONTENT_W - 172
    box_w = 135
    box_h = 24

    c.setFillColor(colors.HexColor("#00A896"))
    c.roundRect(center_x - 52, center_y - 16, 104, 34, 5, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("CNB", 10)
    c.drawCentredString(center_x, center_y - 3, "DSP 第二章下")
    branches = [
        ("拉氏变换与 Z 变换比较", left_x, y - 8, "s 平面与 z 平面映射；H(s) 到 H(z)"),
        ("滤波器设计", left_x, y - 92, "一阶；陷波；全通；最小相位"),
        ("模拟频率与数字频率换算", right_x, y - 8, "理想抽样信号频谱；傅里叶变换关系"),
        ("系统函数", right_x, y - 92, "定义；差分方程；稳定性；频率响应"),
    ]
    c.setStrokeColor(colors.black)
    for text, bx, by, detail in branches:
        c.line(center_x, center_y, bx + box_w / 2, by - box_h / 2)
        c.setFillColor(colors.HexColor("#ECEFF3"))
        c.roundRect(bx, by - box_h, box_w, box_h, 5, stroke=0, fill=1)
        c.setFillColor(TEXT)
        c.setFont("CN", 8.4)
        c.drawCentredString(bx + box_w / 2, by - 15, text)
        c.setFont("CN", 7.4)
        lines = wrap(detail, box_w + 30, "CN", 7.4)
        yy = by - 37
        for line in lines[:2]:
            c.drawString(bx - 6, yy, line)
            yy -= 11
    doc.y -= 170


def build_pdf():
    register_fonts()

    # Frequency response continuation.
    ex_exp = f("ex_exp", r"x(n)=e^{j\omega_0 n}", 15)
    conv_exp = f("conv_exp", r"y(n)=x(n)*h(n)=\sum_{m=-\infty}^{\infty}h(m)e^{j\omega_0(n-m)}", 12)
    h_inner = f("h_inner", r"=e^{j\omega_0 n}\sum_{m=-\infty}^{\infty}h(m)e^{-j\omega_0m}=e^{j\omega_0 n}H(e^{j\omega_0})", 12, "#7B3FC6")
    h_output = f("h_output", r"y(n)=|H(e^{j\omega_0})|e^{j[\omega_0n+\theta(\omega_0)]}", 14)
    sin_resp = f("sin_resp", r"y(n)=A|H(e^{j\omega_0})|\cos[\omega_0 n+\varphi+\theta(\omega_0)]", 15, "#D71920")
    lp_piece = piecewise_png(
        "b115_lp_piece",
        r"H(e^{j\omega})=",
        r"1,\ |\omega|\leq0.5\pi",
        r"0,\ 0.5\pi<|\omega|\leq\pi",
        fontsize=16,
    )
    h_lp = f("h_lp", r"h(n)=\frac{\sin(0.5\pi n)}{\pi n}", 14)
    lp_inputs = [
        f("lp_in_a", r"(a)\quad x(n)=\delta(n)+\delta(n-1)", 13),
        f("lp_in_b", r"(b)\quad x(n)=\cos(0.6\pi n)", 13),
        f("lp_in_c", r"(c)\quad x(n)=1+\cos(0.4\pi n)+\delta(n)", 13),
        f("lp_in_d", r"(d)\quad x(n)=5\sin(0.7\pi n)+10e^{j0.2\pi n}", 13),
    ]
    lp_solutions = [
        f("lp_sol_a", r"(a)\quad y(n)=h(n)+h(n-1)=\frac{\sin(0.5\pi n)}{\pi n}+\frac{\sin[0.5\pi(n-1)]}{\pi(n-1)}", 11),
        f("lp_sol_b", r"(b)\quad y(n)=|H(e^{j0.6\pi})|\cos(0.6\pi n)=0", 12),
        f("lp_sol_c", r"(c)\quad y(n)=\frac{\sin(0.5\pi n)}{\pi n}+\cos(0.4\pi n)+\frac{\sin(0.5\pi n)}{\pi n}", 11),
        f("lp_sol_d", r"(d)\quad y(n)=5\frac{\sin(0.5\pi n)}{\pi n}+10e^{j0.2\pi n}", 12),
    ]
    h_z_fact = f("h_z_fact", r"H(z)=A\frac{\prod_{r=1}^{N}(1-z_rz^{-1})}{\prod_{k=1}^{M}(1-p_kz^{-1})}", 17)
    h_e_fact = f("h_e_fact", r"H(e^{j\omega})=Ae^{j(M-N)\omega}\frac{\prod_{r=1}^{N}(e^{j\omega}-z_r)}{\prod_{k=1}^{M}(e^{j\omega}-p_k)}", 15)
    geom_mag = f("geom_mag", r"|H(e^{j\omega})|=A\frac{\prod_{r=1}^{N}A_r}{\prod_{k=1}^{M}B_k}", 24)
    geom_phase = f("geom_phase", r"\theta(\omega)=\sum_{r=1}^{N}\alpha_r-\sum_{k=1}^{M}\beta_k", 19)
    first_order = f("first_order", r"y(n)=b\,y(n-1)+x(n),\quad 0<b<1", 14)
    first_h = f("first_h", r"H(z)=\frac{z}{z-b}", 15)
    comb_h = f("comb_h", r"H(z)=1-z^{-N}=\frac{z^N-1}{z^N}", 15)
    comb_zeros = f("comb_zeros", r"z^N=1=e^{j2\pi k}\Rightarrow z=e^{j\frac{2\pi}{N}k},\quad k=0,1,\ldots,N-1", 13, "#D71920")
    ex3_q = f("ex3_q", r"y(n)=x(n)-x(n-2)", 15)
    ex3_h = f("ex3_h", r"H(z)=\frac{Y(z)}{X(z)}=1-z^{-2},\quad h(n)=\{1,0,-1\}", 14)
    ex3_freq = f("ex3_freq", r"H(e^{j\omega})=e^{-j\omega}[2j\sin\omega]=e^{j(-\omega+\frac{\pi}{2})}[2\sin\omega]", 13)
    ex3_out = f("ex3_out", r"x(n)=1+2(-1)^n+\cos(0.5\pi n)\Rightarrow y(n)=2\cos(0.5\pi n)", 13)

    # s/z and filter design.
    sz_map = f("sz_map", r"z=e^{sT}=re^{j\theta},\quad s=\sigma+j\Omega,\quad r=e^{\sigma T},\quad \theta=\Omega T", 13)
    r_sigma = f("r_sigma", r"\sigma=0\Rightarrow r=1,\quad \sigma>0\Rightarrow r>1,\quad \sigma<0\Rightarrow r<1", 13)
    w_omega = f("w_omega", r"\omega=\Omega T", 15)
    h_s_to_z = f("h_s_to_z", r"H(s)=\sum_{i=1}^{N}\frac{A_i}{s-s_i}\Rightarrow H(z)=\sum_{i=1}^{N}\frac{TA_i}{1-e^{s_iT}z^{-1}}", 13, "#D71920")
    hs_ex = f("hs_ex", r"H(s)=\frac{1}{s+1}\Rightarrow H(z)=\frac{T}{1-e^{-T}z^{-1}}", 14)
    hz_reverse = f("hz_reverse", r"H(s)=H(z)|_{z=e^{sT}}", 13)
    lp_zero_h = f("lp_zero_h", r"H(z)=\frac{z+1}{2z}=\frac{1}{2}(1+z^{-1}),\quad y(n)=\frac{1}{2}[x(n)+x(n-1)]", 12)
    hp_zero_h = f("hp_zero_h", r"H(z)=\frac{z-1}{2z}=\frac{1}{2}(1-z^{-1}),\quad y(n)=\frac{1}{2}[x(n)-x(n-1)]", 12)
    lp_pole_h = f("lp_pole_h", r"H(z)=\frac{1-a}{z-a},\quad 0<a<1", 14)
    lp_pole_zero = f("lp_pole_zero", r"H(z)=\frac{1-a}{2}\frac{z+1}{z-a},\quad 0<a<1", 14)
    notch_w = f("notch_w", r"\omega_0=2\pi\frac{50}{1000}=0.1\pi\;(\mathrm{rad})", 14)
    notch_relation = f("notch_relation", r"\frac{k}{N}=\frac{\omega}{2\pi}=\frac{f}{f_s}=\frac{\Omega}{\Omega_s}", 14, "#D71920")
    notch_h = f("notch_h", r"H(z)=\frac{1}{3.9}\frac{(z-e^{j\omega_0})(z-e^{-j\omega_0})}{z^2}", 14)
    ap_def = f("ap_def", r"|H(e^{j\omega})|=1,\quad 0\leq\omega\leq2\pi", 14)
    ap_general_main = f("ap_general_main", r"H_{ap}(z)=A\frac{\sum_{k=0}^{N}d_kz^{-N+k}}{\sum_{k=0}^{N}d_kz^{-k}}", 26)
    ap_general_conditions = f("ap_general_conditions", r"d_0=1,\qquad d_k\in\mathbb{R}", 12)
    ap_fact = f("ap_fact", r"H_{ap}(z)=A\frac{z^{-N}D(z^{-1})}{D(z)}=A\prod_{i=1}^{N}\frac{z^{-1}-p_i^*}{1-p_iz^{-1}}", 13)
    ap_mag = f("ap_mag", r"|H_{ap}(e^{j\omega})|=\left|A\frac{(e^{j\omega})^{-N}D(e^{-j\omega})}{D(e^{j\omega})}\right|=A", 12)
    min_fac = f("min_fac", r"H(z)=H_{\min}(z)H_{ap}(z)", 15)
    min_phase = f("min_phase", r"\arg[H(e^{j\omega})]=\arg[H_{\min}(e^{j\omega})]+\arg[H_{ap}(e^{j\omega})]", 13)
    min_grd = f("min_grd", r"\operatorname{grd}[H(e^{j\omega})]=\operatorname{grd}[H_{\min}(e^{j\omega})]+\operatorname{grd}[H_{ap}(e^{j\omega})]", 13)
    min_ex_q = f("min_ex_q", r"H(z)=\frac{(1-3z^{-1})(1-0.5z^{-1})}{(1-\frac{3}{4}z^{-1})(1-\frac{4}{3}z^{-1})}", 14)
    min_ex_ans = f("min_ex_ans", r"H(z)=\frac{(z-0.5)(z-\frac{1}{3})}{(z-\frac{3}{4})(z-\frac{3}{4})}\cdot\frac{(z-3)(z-\frac{3}{4})}{(z-\frac{4}{3})(z-\frac{1}{3})}=H_{\min}(z)H_{ap}(z)", 11)

    doc = BatchDoc(str(PDF_PATH))
    doc.section = "2.4 系统的频率响应"
    doc.header()

    # The sinusoidal steady-state section is carried by the previous batch tail page.

    doc.h2("例 4  理想低通频率响应")
    doc.p("已知理想低通频率响应，分别判断各输入通过系统后的稳态输出。")
    draw_formula_rows(doc, [lp_piece], max_h=30)
    doc.p("求以下输入经过该系统后的输出：")
    draw_formula_rows(doc, lp_inputs, max_h=22, left=True, indent=25)
    doc.p("解：先由频率响应求冲激响应，再分别利用卷积或正弦稳态响应。")
    draw_formula_rows(doc, [h_lp], max_h=30)
    draw_formula_rows(doc, lp_solutions, max_h=24, left=True, indent=25)
    note_box(doc, "814 考点提示", "遇到正弦输入时，先判断该频率是否落在通带；通带内保留，阻带内被滤除。")

    doc.h2("几何法求频率响应")
    draw_formula_rows(doc, [h_z_fact, h_e_fact], max_h=45, left=True, indent=18)
    doc.p("取单位圆上一点，零点到该点的向量长度记为 A_r，极点到该点的向量长度记为 B_k。")
    doc.ensure(90)
    draw_formula(doc, geom_mag, max_h=44, gap=5)
    draw_formula(doc, geom_phase, max_h=34, gap=5)
    para_red(doc, [("零点靠近单位圆会形成幅度谷；极点靠近单位圆会形成幅度峰。零点或极点在 z=0 时模长为 1，只影响相位。", "red")])
    draw_unit_circle(doc, zeros=[(math.pi, "-1")], poles=[(0, 0.55, "b")], caption="单位圆上任取一点观察零极点向量")

    doc.h2("例 1  一阶系统的频率响应")
    draw_formula_rows(doc, [first_order, first_h], max_h=28)
    doc.p("系统函数有一个零点在原点、一个极点在 z=b。低频处更靠近极点，幅度较大；高频处远离极点，幅度较小。")
    draw_formula_rows(doc, [f("fo_gain", r"|H(e^{j0})|=\frac{1}{1-b},\quad |H(e^{j\pi})|=\frac{1}{1+b}", 13)], max_h=27)
    draw_unit_circle(doc, zeros=[(0, "0")], poles=[(0, 0.55, "b")], caption="极点靠近 z=1，低频得到增强")

    doc.new_page()
    doc.h2("例 2  梳状滤波器")
    doc.p("已知系统函数，试定性画出幅频响应。")
    draw_formula(doc, comb_h, max_h=28)
    para_red(doc, [("求零点时先把 z 看作复变量，不要过早代入单位圆。", "purple")])
    draw_formula(doc, comb_zeros, max_h=30)
    draw_comb_diagrams(doc)
    draw_red_text(doc, "由于幅度响应像一把梳子，因此该系统又称梳状滤波器，常见于真题。")

    doc.h2("例 3  由差分方程求频率响应")
    draw_formula_rows(doc, [ex3_q, ex3_h, ex3_freq, ex3_out], max_h=29)
    doc.p("由系统函数可知系统因果且稳定。幅频响应为正弦项的幅值，相频响应为指数因子的相位。")

    doc.section = "2.5 拉氏变换与Z变换的比较"
    doc.h2("2.5.1 s 平面与 z 平面的映射关系")
    draw_formula_rows(doc, [sz_map, r_sigma], max_h=28)
    para_red(doc, [("s 平面的虚轴映射到 z 平面的单位圆；右半平面映射到单位圆外；左半平面映射到单位圆内。", "red")])
    draw_s_z_mapping(doc)
    draw_formula(doc, w_omega, max_h=28)
    doc.p("数字频率 ω 与模拟频率 Ω 通过抽样周期联系；宽为 2π/T 的水平条带会映射到整个 z 平面。")
    draw_strip_mapping(doc)
    draw_red_text(doc, "结论：Ω 与 ω 的映射是多值映射。")

    doc.h2("2.5.2 连续信号的拉氏变换与 Z 变换")
    doc.p("将模拟滤波器变成数字滤波器时，可用脉冲响应不变法：先求连续系统冲激响应，再时域抽样，最后作 Z 变换。")
    draw_formula_rows(doc, [h_s_to_z, hz_reverse, hs_ex], max_h=31)
    draw_red_text(doc, "应用场景：利用脉冲响应不变法将模拟滤波器变为数字滤波器。")

    doc.section = "2.6 滤波器设计"
    doc.h2("2.6.1 简单一阶滤波器设计")
    para_red(doc, [("设计原则：", "blue"), (" 要拒绝某个频率，就在单位圆对应频率处放零点；要突出某个频率，就在单位圆内对应频率处放极点。", "normal")])
    draw_red_text(doc, "实际体现的是零极点对幅频响应的影响。")
    doc.ensure(180)
    doc.p("由一个零点调节的低通滤波器：在 w=π 处设置零点，滤除高频分量。")
    draw_unit_and_response(doc, "lp_zero")
    draw_formula(doc, lp_zero_h, max_h=29)
    doc.ensure(180)
    doc.p("由一个零点调节的高通滤波器：在 w=0 处设置零点，滤除低频分量。")
    draw_unit_and_response(doc, "hp_zero")
    draw_formula(doc, hp_zero_h, max_h=29)
    doc.p("另一种低通思路是突出低频：在 w=0 附近设置极点。为了系统稳定，极点不能放在单位圆上。")
    draw_formula_rows(doc, [lp_pole_h, lp_pole_zero], max_h=30)

    doc.h2("2.6.2 数字陷波器设计")
    doc.p("陷波器是一种特殊的带阻滤波器，理想情况下阻带只有一个频率点，主要用于消除特定频率干扰。")
    draw_formula_rows(doc, [notch_w, notch_relation, notch_h], max_h=29)
    para_red(doc, [("这个 H(z) 的系数较难计算，主要掌握设计思想。", "red")])
    para_red(doc, [("设置一对共轭零点，是为了保证设计出来的滤波器为实系数。", "purple")])
    draw_unit_circle(doc, zeros=[(0.1 * math.pi, "ω0"), (-0.1 * math.pi, "-ω0")], poles=[(0, 0, "0")], caption="50 Hz 陷波器的零点放在 ±ω0")

    doc.h2("2.6.3 全通滤波器")
    doc.p("全通滤波器的幅度特性在整个频带上均为常数或 1，信号通过后幅度不变，仅相位发生变化。")
    draw_formula(doc, ap_def, max_h=31)
    doc.p("全通滤波器的系统函数的一般形式为：")
    draw_formula(doc, ap_general_main, max_h=72)
    draw_formula(doc, ap_general_conditions, max_h=20)
    draw_formula(doc, ap_fact, max_h=40)
    draw_formula(doc, ap_mag, max_h=34)
    draw_red_text(doc, "实系数全通滤波器的零极点具有共轭倒易关系；常用于相位校正，又称相位均衡器。")
    draw_red_text(doc, "稳定实系数全通滤波器的重要特性：相位在 [0,π] 内单调减小，群延迟为正。")

    doc.h2("2.6.4 最小相位滤波器")
    doc.p("逆系统定义为：系统函数 H_i(z) 与 H(z) 级联后总系统函数为 1。若系统与逆系统都因果稳定，则 H(z) 的全部零点和极点都在单位圆内。")
    draw_red_text(doc, "最小相位系统的零点和极点都在单位圆内。")
    draw_formula_rows(doc, [min_fac, min_phase, min_grd], max_h=30)
    doc.p("全通系统总是引入相位滞后且群延迟为正，因此最小相位部分具有最小相位滞后和最小群延迟。")
    doc.h2("例  最小相位分解")
    draw_formula_rows(doc, [min_ex_q, min_ex_ans], max_h=34)
    doc.p("单位圆内的零极点归入最小相位系统，其余因子配成全通系统。")

    doc.h2("本章下半部分导图")
    draw_filter_map(doc)

    doc.h2("第二章课后习题")
    zheng_items = [
        "8-17 求卷积，体会时域和频域两种求法。",
        "8-21（2）（4）用单边 z 变换求解差分方程。",
        "8-23 根据题目隐含条件确定收敛域，并判断稳定性。",
        "8-24 根据差分方程求单位脉冲响应及输出。",
        "8-25 根据系统框图写出差分方程。",
        "8-26 可在学过系统流图后再画。",
        "8-27 根据不同收敛域求原序列，并判断因果性和稳定性。",
        "8-29 根据差分方程求单位脉冲响应及输出。",
        "8-32 根据系统函数写差分方程、画结构图并求频率响应。",
        "8-33 根据零极点图画幅频响应。",
        "8-34、8-36、8-37：典型 z 域综合题。",
    ]
    gao_items = [
        "2-12 求输出及序列傅里叶变换。",
        "2-13 连续时间信号、采样信号和时域离散信号之间的关系。",
        "2-14 求简单序列的 z 变换及收敛域。",
        "2-15 求 z 变换、收敛域并画零极点图；第（2）问困难时可先看答案，第（3）问先展开序列再画图。",
        "2-17 利用 z 变换性质求 z 变换。",
        "2-18 由不同收敛域确定原序列。",
        "2-19 用部分分式展开法求反变换。",
        "2-23、2-24：典型 z 域综合题。",
        "2-25 分别从时域和频域求卷积。",
        "2-28 共轭对称与虚实部的对应关系。",
    ]
    draw_homework_columns(doc, "郑君里书", zheng_items, "高西全书", gao_items)

    doc.save()


if __name__ == "__main__":
    build_pdf()
    NOTE_PATH.write_text(
        "\n".join(
            [
                "# 第五批校对记录",
                "",
                "- 覆盖原 PPT 115-140 页：系统频率响应、s/z 映射比较、脉冲响应不变法、滤波器设计、全通和最小相位滤波器。",
                "- 保留红色/紫色重点：正弦稳态、梳状滤波器、Ω 到 ω 多值映射、陷波器频率换算、全通共轭倒易关系、最小相位结论。",
                "- 公式均以数学图像渲染；比值和除法采用分数形式；未使用源代码式题干公式。",
                "- 图像为重绘示意：单位圆零极点、幅频响应、s/z 平面映射和章节导图均去除源水印后重排。",
            ]
        ),
        encoding="utf-8",
    )
