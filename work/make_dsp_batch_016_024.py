from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw, ImageFont

from make_dsp_sample_handout_v2 import (
    BLUE,
    BLUE_DARK,
    CONTENT_W,
    FORMULA_DIR,
    LINE,
    MARGIN_X,
    MUTED,
    OUT_DIR,
    PAGE_H,
    PAGE_W,
    PALE,
    TEXT,
    Doc,
    _open_trim_rgba,
    _paste_rgba,
    _trim_rgba,
    draw_discrete_axes_plot,
    draw_centered_multiline_text,
    draw_stem,
    formula_png,
    piecewise_png,
    register_fonts,
    normalize_display_formula_height,
    wrap,
)


PDF_PATH = OUT_DIR / "DSP讲义重制_第二批_原PPT16-45页_坐标轴明显加长版.pdf"
NOTE_PATH = OUT_DIR / "DSP讲义重制_第二批_原PPT16-45页_坐标轴明显加长版_校对记录.md"


def system_block_source_geometry():
    """Topology contract copied from source PPT pages 42 and 45."""
    return {
        "example9": {
            "delay_orientation": "vertical_stack",
            "gain_2_return": ("inter_delay_node", "horizontal_left", "diagonal_to_summer_right"),
            "gain_2_arrow_endpoint": "summer_lower_right_circumference",
            "gain_minus_1_return": ("second_delay_output", "horizontal_left", "vertical_to_summer_bottom"),
        },
        "example10": {
            "delay_orientation": "horizontal_chain",
            "output_minus_2_return": ("first_delay_output", "vertical_up", "summer_bottom"),
            "input_minus_2_return": ("first_delay_output", "extend_right", "vertical_down", "horizontal_left", "diagonal_to_input_summer"),
            "feedback_tap": "post_delay_right_extension",
            "gain_3_return": ("second_delay_output", "vertical_down", "horizontal_left", "summer_bottom"),
        },
    }


def system_block_arrow_geometry():
    return {
        'example9': {
            'arrow_count_at_diagonal_entry': 1,
            'endpoint_on_circumference': True,
            'diagonal_endpoint': 'lower_right',
            'bottom_endpoint': 'bottom',
        },
        'example10': {
            'arrow_count_at_diagonal_entry': 1,
            'endpoint_on_circumference': True,
            'diagonal_endpoint': 'lower_right',
            'bottom_endpoint': 'bottom',
        },
    }


def precise_arrow(c, x1, y1, x2, y2, head=7, wing=3.5):
    """Draw one vector-aligned arrowhead without intruding past its endpoint."""
    import math
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if not length:
        return
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    c.line(x1, y1, x2, y2)
    bx, by = x2 - head * ux, y2 - head * uy
    c.line(x2, y2, bx + wing * px, by + wing * py)
    c.line(x2, y2, bx - wing * px, by - wing * py)


class BatchDoc(Doc):
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
        self.y = 778


def draw_formula(doc, image_path, max_w=None, max_h=34, center=True, gap=12):
    max_h = normalize_display_formula_height(max_h)
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


def piecewise3_cn_png(name, lhs_expr, row1_expr, row2_expr, row3_cn="其他", fontsize=17):
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


def draw_formula_pair(doc, left_path, right_text, max_h=34):
    im = Image.open(left_path)
    iw, ih = im.size
    scale = min(250 / iw, 0.34)
    dw, dh = iw * scale, ih * scale
    text_x = MARGIN_X + 302
    lines = wrap(right_text, CONTENT_W - 310, "CN", 9.4)
    row_h = max(dh + 10, 14 * len(lines) + 6)
    doc.ensure(row_h + 8)
    c = doc.c
    c.setFillColor(BLUE)
    c.circle(MARGIN_X + 4, doc.y - dh / 2 + 4, 2.2, stroke=0, fill=1)
    c.drawImage(ImageReader(str(left_path)), MARGIN_X + 17, doc.y - dh + 4, dw, dh, mask="auto")
    c.setFillColor(TEXT)
    c.setFont("CN", 9.4)
    yy = doc.y - 8
    for line in lines:
        c.drawString(text_x, yy, line)
        yy -= 14
    doc.y -= row_h


def draw_system_block(doc, input_label, block_label, output_label):
    doc.ensure(72)
    c = doc.c
    y = doc.y
    x0 = MARGIN_X + 104
    block_w, block_h = 136, 42
    mid_y = y - 31
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    c.line(x0, mid_y, x0 + 92, mid_y)
    c.line(x0 + 92, mid_y, x0 + 84, mid_y + 4)
    c.line(x0 + 92, mid_y, x0 + 84, mid_y - 4)
    c.rect(x0 + 92, mid_y - block_h / 2, block_w, block_h, stroke=1, fill=0)
    c.line(x0 + 92 + block_w, mid_y, x0 + 92 + block_w + 92, mid_y)
    c.line(x0 + 92 + block_w + 92, mid_y, x0 + 92 + block_w + 84, mid_y + 4)
    c.line(x0 + 92 + block_w + 92, mid_y, x0 + 92 + block_w + 84, mid_y - 4)
    c.setFillColor(TEXT)
    c.setFont("CN", 9.0)
    c.drawCentredString(x0 + 46, mid_y + 16, input_label)
    draw_centered_multiline_text(c, x0 + 92 + block_w / 2, mid_y, block_label, "CN", 9.0)
    c.drawCentredString(x0 + 92 + block_w + 46, mid_y + 16, output_label)
    doc.y -= 68


def draw_example2_plot(doc):
    doc.ensure(168)
    draw_discrete_axes_plot(
        doc.c,
        MARGIN_X + 150,
        doc.y - 18,
        300,
        150,
        {-1: 1, 0: 4, 1: -2},
        n_min=-2,
        n_max=2,
        title="x(1-2n)",
        axis_v_min=-3.2,
        axis_v_max=6.4,
        value_label_offsets={-1: (13, 0)},
    )
    doc.y -= 168


def small_axis_geometry():
    return {"vertical_arrow_headroom": 12.0}


def draw_small_axis(c, x, y, w, h, values, label_right=None, direction=1):
    left = x + 8
    right = x + w - 8
    x0 = x + 12 if direction > 0 else right - 24
    y0 = y - h + 16
    top = y - 8
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.setLineWidth(0.8)
    arrow(c, x0 if direction > 0 else left, y0, right, y0)
    arrow(c, x0, y0, x0, top)
    max_value = max(values) if values else 1
    amplitude = top - y0 - small_axis_geometry()["vertical_arrow_headroom"]
    available = right - x0 - 18 if direction > 0 else x0 - left - 10
    step = available / max(1, len(values) - 1)
    sample_top = y0
    for idx, value in enumerate(values):
        px = x0 + direction * idx * step
        py = y0 + value / max_value * amplitude
        c.line(px, y0, px, py)
        c.circle(px, py, 2.2, stroke=1, fill=1)
        if idx == 0:
            sample_top = py
    if label_right:
        c.setFont("CN", 8.2)
        c.setFillColor(colors.black)
        c.drawString(x0 + 8, sample_top - 3, label_right)


def draw_ex4_plots(doc):
    doc.ensure(92)
    c = doc.c
    y = doc.y
    draw_small_axis(c, MARGIN_X + 168, y, 130, 74, [1, 0.72, 0.52, 0.38])
    draw_small_axis(c, MARGIN_X + 330, y, 150, 74, [1, 1, 1, 1], "1", direction=-1)
    doc.y -= 94


def draw_conv_vertical_working(doc):
    doc.ensure(150)
    c = doc.c
    x = MARGIN_X + 118
    y = doc.y
    step = 36
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.setLineWidth(0.8)
    c.setFont("CN", 12)

    def put(row_y, col, text="1"):
        c.drawCentredString(x + col * step, row_y, text)

    # Original PPT-style list convolution layout.
    for col in range(3):
        put(y - 10, col)
    for col in range(4):
        put(y - 28, col)
    c.line(x - 22, y - 36, x + 5 * step + 22, y - 36)

    for shift in range(3):
        for col in range(4):
            put(y - 58 - shift * 18, shift + col)
    c.line(x - 22, y - 118, x + 5 * step + 22, y - 118)

    for col, val in enumerate([1, 2, 3, 3, 2, 1]):
        put(y - 140, col, str(val))
    doc.y -= 158


def draw_img_at(c, image_path, x, y, max_w=60, max_h=18, center=True):
    im = Image.open(image_path)
    iw, ih = im.size
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    xx = x - dw / 2 if center else x
    c.drawImage(ImageReader(str(image_path)), xx, y - dh / 2, dw, dh, mask="auto")
    return dw, dh


def arrow(c, x1, y1, x2, y2):
    c.line(x1, y1, x2, y2)
    if abs(x2 - x1) >= abs(y2 - y1):
        sign = 1 if x2 >= x1 else -1
        c.line(x2, y2, x2 - sign * 7, y2 + 4)
        c.line(x2, y2, x2 - sign * 7, y2 - 4)
    else:
        sign = 1 if y2 >= y1 else -1
        c.line(x2, y2, x2 - 4, y2 - sign * 7)
        c.line(x2, y2, x2 + 4, y2 - sign * 7)


def draw_sum_node(c, x, y, symbol="+", r=15):
    c.circle(x, y, r, stroke=1, fill=0)
    draw_centered_multiline_text(c, x, y, symbol, "CNB", 14)


def draw_delay(c, x, y, w=52, h=32):
    c.rect(x, y - h / 2, w, h, stroke=1, fill=0)
    draw_centered_multiline_text(c, x + w / 2, y, "D", "CN", 12)


def draw_lti_interconnects(doc):
    doc.ensure(180)
    c = doc.c
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    y = doc.y - 28
    x = MARGIN_X + 92
    w, h = 74, 36
    arrow(c, x, y, x + 62, y)
    c.rect(x + 62, y - h / 2, w, h, stroke=1, fill=0)
    arrow(c, x + 62 + w, y, x + 62 + w + 62, y)
    c.rect(x + 62 + w + 62, y - h / 2, w, h, stroke=1, fill=0)
    arrow(c, x + 62 + w + 62 + w, y, x + 62 + w + 62 + w + 62, y)
    draw_img_at(c, formula_png("b034_x", r"x(n)", 12), x - 10, y + 18, max_w=44)
    draw_img_at(c, formula_png("b034_h1", r"h_1(n)", 12), x + 62 + w / 2, y, max_w=45)
    draw_img_at(c, formula_png("b034_h2", r"h_2(n)", 12), x + 62 + w + 62 + w / 2, y, max_w=45)
    draw_img_at(c, formula_png("b034_y", r"y(n)", 12), x + 62 + w + 62 + w + 78, y + 18, max_w=44)

    y2 = doc.y - 104
    x2 = MARGIN_X + 135
    arrow(c, x2, y2, x2 + 62, y2)
    c.line(x2 + 62, y2, x2 + 62, y2 + 28)
    c.line(x2 + 62, y2, x2 + 62, y2 - 28)
    c.rect(x2 + 62, y2 + 10, w, h, stroke=1, fill=0)
    c.rect(x2 + 62, y2 - 46, w, h, stroke=1, fill=0)
    c.line(x2 + 62 + w, y2 + 28, x2 + 62 + w + 34, y2 + 28)
    c.line(x2 + 62 + w, y2 - 28, x2 + 62 + w + 34, y2 - 28)
    c.line(x2 + 62 + w + 34, y2 + 28, x2 + 62 + w + 34, y2 - 28)
    arrow(c, x2 + 62 + w + 34, y2, x2 + 62 + w + 90, y2)
    draw_img_at(c, formula_png("b034_x2", r"x(n)", 12), x2 - 12, y2 + 18, max_w=44)
    draw_img_at(c, formula_png("b034_h1b", r"h_1(n)", 12), x2 + 62 + w / 2, y2 + 28, max_w=45)
    draw_img_at(c, formula_png("b034_h2b", r"h_2(n)", 12), x2 + 62 + w / 2, y2 - 28, max_w=45)
    draw_img_at(c, formula_png("b034_y2", r"y(n)", 12), x2 + 62 + w + 108, y2 + 18, max_w=44)
    doc.y -= 205


def draw_basic_ops(doc):
    doc.ensure(245)
    c = doc.c
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    x = MARGIN_X + 165
    y = doc.y - 34

    draw_sum_node(c, x + 70, y)
    arrow(c, x, y, x + 55, y)
    arrow(c, x + 70, y - 42, x + 70, y - 15)
    arrow(c, x + 85, y, x + 160, y)
    draw_img_at(c, formula_png("b041_x1", r"x_1(n)", 11), x - 18, y + 16, max_w=46)
    draw_img_at(c, formula_png("b041_x2", r"x_2(n)", 11), x + 91, y - 22, max_w=46)
    draw_img_at(c, formula_png("b041_sum", r"x_1(n)+x_2(n)", 11), x + 208, y + 16, max_w=92)

    y2 = y - 92
    draw_sum_node(c, x + 70, y2, symbol="×")
    arrow(c, x, y2, x + 55, y2)
    arrow(c, x + 70, y2 - 38, x + 70, y2 - 15)
    arrow(c, x + 85, y2, x + 160, y2)
    draw_img_at(c, formula_png("b041_x", r"x(n)", 11), x - 16, y2 + 16, max_w=42)
    draw_img_at(c, formula_png("b041_a", r"a", 11), x + 91, y2 - 24, max_w=24)
    draw_img_at(c, formula_png("b041_ax", r"a x(n)", 11), x + 198, y2 + 16, max_w=62)

    y3 = y2 - 84
    draw_delay(c, x + 44, y3)
    arrow(c, x - 28, y3, x + 44, y3)
    arrow(c, x + 96, y3, x + 166, y3)
    draw_img_at(c, formula_png("b041_xd", r"x(n)", 11), x - 50, y3 + 16, max_w=42)
    draw_img_at(c, formula_png("b041_xd1", r"x(n-1)", 11), x + 198, y3 + 16, max_w=62)
    doc.y -= 236


def draw_example9_block(doc):
    geometry = system_block_source_geometry()["example9"]
    doc.ensure(188)
    c = doc.c
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    cx = MARGIN_X + 125
    cy = doc.y - 42
    r = 16
    draw_sum_node(c, cx, cy, r=r)
    arrow(c, cx - 80, cy, cx - r, cy)
    arrow(c, cx + r, cy, cx + 285, cy)
    draw_img_at(c, formula_png("b042_xn", r"x(n)", 11), cx - 104, cy + 17, max_w=44)
    draw_img_at(c, formula_png("b042_yn", r"y(n)", 11), cx + 307, cy + 17, max_w=44)
    branch_x = cx + 196
    d_w, d_h = 58, 32
    d1_y, d2_y = cy - 54, cy - 112
    draw_delay(c, branch_x-d_w/2, d1_y, w=d_w, h=d_h)
    draw_delay(c, branch_x-d_w/2, d2_y, w=d_w, h=d_h)
    # Output is sampled into two vertical unit delays.
    arrow(c, branch_x, cy, branch_x, d1_y+d_h/2)
    arrow(c, branch_x, d1_y-d_h/2, branch_x, d2_y+d_h/2)
    # Source PPT 42: take the gain-2 branch from the node between D blocks.
    tap1_y=(d1_y-d_h/2 + d2_y+d_h/2)/2; feed1_x=cx+72
    c.line(branch_x,tap1_y,feed1_x,tap1_y)
    entry_x = cx + r * 0.72
    entry_y = cy - r * 0.72
    precise_arrow(c,feed1_x,tap1_y,entry_x,entry_y)
    # Second feedback: y(n-2) ---1--> bottom input, fully orthogonal.
    tap2_y=d2_y-d_h/2; feed2_x=cx-2
    c.line(branch_x,tap2_y,branch_x,tap2_y-20)
    c.line(branch_x,tap2_y-20,feed2_x,tap2_y-20)
    arrow(c,feed2_x,tap2_y-20,feed2_x,cy-r)
    c.setFont("CN",10); c.drawString(feed1_x+28,tap1_y-18,"2"); c.drawString(cx+55,tap2_y-8,"-1")
    doc.y -= 196


def draw_example10_block(doc):
    geometry = system_block_source_geometry()["example10"]
    doc.ensure(280)
    c = doc.c
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    x0 = MARGIN_X + 78
    y = doc.y - 158
    r = 16
    draw_sum_node(c, x0, y, r=r)
    d1x=x0+150; d2x=x0+275; yout=y+94; output_sum_x=x0+290
    arrow(c,x0-70,y,x0-r,y); arrow(c,x0+r,y,d1x,y)
    draw_img_at(c,formula_png("b045_xn",r"x(n)",11),x0-57,y+18,max_w=44)
    draw_img_at(c,formula_png("b045_gn",r"g(n)",11),x0+72,y+18,max_w=44)
    draw_delay(c,d1x,y)
    tap_x = d1x + 78
    c.line(d1x+52,y,tap_x,y)
    arrow(c,tap_x,y,d2x,y)
    draw_delay(c,d2x,y)
    draw_img_at(c,formula_png("b045_gn1",r"g(n-1)",10),d1x+26,y+28,max_w=56)
    draw_img_at(c,formula_png("b045_gn2",r"g(n-2)",10),d2x+26,y+28,max_w=56)
    # Source PPT 45: the first-delay output feeds both summers on separate rails.
    fb1_y=y-48
    c.line(tap_x,y,tap_x,fb1_y)
    c.line(tap_x,fb1_y,x0+66,fb1_y)
    diagonal = 2 ** -0.5
    precise_arrow(c,x0+66,fb1_y,x0+r*diagonal,y-r*diagonal)
    # Orthogonal +3 feedback from the second delay, on its own lower rail.
    fb2_y=y-118
    c.line(d2x+52,y,d2x+52,fb2_y); c.line(d2x+52,fb2_y,x0,fb2_y); arrow(c,x0,fb2_y,x0,y-r)
    c.setFont("CN",10); c.drawString(d1x+80,fb1_y-12,"-2"); c.drawString(d2x+45,fb2_y-12,"3")
    # Output equation y(n)=g(n)-2g(n-1), using a separate upper summer.
    c.line(x0+42,y,x0+42,yout); arrow(c,x0+42,yout,output_sum_x-r,yout)
    draw_img_at(c,formula_png("b045_yn_eq",r"y(n)=g(n)-2g(n-1)",13),x0+78,yout+23,max_w=190)
    c.line(tap_x,y,tap_x,yout-44); c.line(tap_x,yout-44,output_sum_x,yout-44); arrow(c,output_sum_x,yout-44,output_sum_x,yout-r)
    c.setFont("CN",10); c.drawString(output_sum_x+18,yout-38,"-2")
    draw_sum_node(c,output_sum_x,yout,r=r); arrow(c,output_sum_x+r,yout,output_sum_x+76,yout)
    draw_img_at(c,formula_png("b045_yn",r"y(n)",11),output_sum_x+88,yout+18,max_w=42)
    doc.y -= 300


def build_pdf():
    register_fonts()

    f_ex2_given = piecewise3_cn_png(
        "b016_ex2_given",
        r"x(n)=",
        r"3n+1,\ -1\leq n\leq1",
        r"1,\ 2\leq n\leq3",
        row3_cn="其余",
        fontsize=17,
    )
    f_ex2_case1 = formula_png("b016_ex2_case1", r"-1\leq 1-2n\leq1\quad\Rightarrow\quad 0\leq n\leq1", 14)
    f_ex2_value1 = formula_png("b016_ex2_value1", r"x(1-2n)=4-6n,\quad n=0,1", 14)
    f_ex2_case2 = formula_png("b016_ex2_case2", r"2\leq 1-2n\leq3\quad\Rightarrow\quad -1\leq n\leq -\frac{1}{2}", 14)
    f_ex2_value2 = formula_png("b016_ex2_value2", r"x(1-2n)=1,\quad n=-1", 14)

    f_system = formula_png("b017_system", r"y(n)=T[x(n)]", 17)
    f_super = formula_png("b018_super", r"T[x_1(n)+x_2(n)]=y_1(n)+y_2(n)", 14)
    f_homo = formula_png("b018_homo", r"T[a\,x(n)]=a\,y(n)", 14)
    f_linear = formula_png("b018_linear", r"T[a x_1(n)+b x_2(n)]=a y_1(n)+b y_2(n)", 16)
    f_time_shift = formula_png("b019_time_shift", r"y_2(n)=T[x_2(n)]=y_1(n-n_0)", 16)
    f_ex3_a = formula_png("b020_ex3_a", r"y(n)=x^2(n)", 16)
    f_ex3_b = formula_png("b020_ex3_b", r"y(n)=\sum_{k=n_0}^{n}x(k)", 16)
    f_ex3_a_nonlin = formula_png("b021_ex3_a_nonlin", r"T[a x(n)]=a^2x^2(n)\ne a x^2(n)", 14)
    f_ex3_a_ti = formula_png("b021_ex3_a_ti", r"T[x(n-n_0)]=y(n-n_0)", 14)
    f_ex3_b_lin = formula_png("b021_ex3_b_lin", r"T[a x_1(n)+b x_2(n)]=a y_1(n)+b y_2(n)", 14)
    f_ex3_b_tv = formula_png("b021_ex3_b_tv", r"T[x(n-n_1)]\ne y(n-n_1)", 14)
    f_impulse_decomp = formula_png(
        "b023_impulse_decomp",
        r"x(n)=\sum_{m=-\infty}^{\infty}x(m)\delta(n-m)",
        17,
    )
    f_lti_shift = formula_png("b023_lti_shift", r"T[\delta(n-m)]=h(n-m)", 14)
    f_lti_homo = formula_png("b023_lti_homo", r"T[x(m)\delta(n-m)]=x(m)h(n-m)", 14)
    f_lti_output = formula_png("b023_lti_output", r"y(n)=\sum_{m=-\infty}^{\infty}x(m)h(n-m)", 16)
    f_conv_def = formula_png("b023_conv_def", r"x(n)*y(n)=\sum_{m=-\infty}^{\infty}x(m)y(n-m)", 16)
    f_conv_identity = formula_png("b023_conv_identity", r"x(n)=x(n)*\delta(n),\qquad y(n)=x(n)*h(n)", 15)
    f_ex4_title = formula_png("b024_ex4_title", r"a^n u(n)*u(n),\qquad 0<a<1", 16)
    f_ex4_sum = formula_png(
        "b025_ex4_sum",
        r"\sum_{m=-\infty}^{\infty}a^m u(m)u(n-m)",
        15,
    )
    f_ex4_result = formula_png(
        "b025_ex4_result",
        r"a^n u(n)*u(n)=\frac{1-a^{n+1}}{1-a}u(n)",
        16,
    )
    f_ex5_title = formula_png("b026_ex5_title", r"R_3(n)*R_4(n)", 16)
    f_ex5_r3 = formula_png("b026_ex5_r3", r"R_3(n)=1,\quad n=0,1,2", 13)
    f_ex5_r4 = formula_png("b026_ex5_r4", r"R_4(n)=1,\quad n=0,1,2,3", 13)
    f_ex5_result = formula_png("b027_ex5_result", r"R_3(n)*R_4(n)=\{1,\ 2,\ 3,\ 3,\ 2,\ 1\}", 15)
    f_ex6_title = formula_png("b028_ex6_title", r"x(n)=a^n u(n),\quad h(n)=R_4(n),\quad y(n)=x(n)*h(n)", 15)
    f_ex6_sum = formula_png(
        "b029_ex6_sum",
        r"y(n)=h(n)*x(n)=\sum_{m=-\infty}^{+\infty}R_4(m)a^{\,n-m}u(n-m)",
        14,
    )
    f_ex6_bounds = formula_png("b029_ex6_bounds", r"m\leq n,\qquad 0\leq m\leq3", 16)
    f_ex6_mid_cond = formula_png("b029_ex6_mid_cond", r"0\leq n\leq3", 15)
    f_ex6_mid_sum = formula_png("b029_ex6_mid_sum", r"y(n)=\sum_{m=0}^{n}a^{\,n-m}", 16)
    f_ex6_mid_result = formula_png("b029_ex6_mid_result", r"y(n)=a^n\frac{1-a^{-n-1}}{1-a^{-1}}", 16)
    f_ex6_tail_cond = formula_png("b029_ex6_tail_cond", r"n\geq4", 15)
    f_ex6_tail_sum = formula_png("b029_ex6_tail_sum", r"y(n)=\sum_{m=0}^{3}a^{\,n-m}", 16)
    f_ex6_tail_result = formula_png("b029_ex6_tail_result", r"y(n)=a^n\frac{1-a^{-4}}{1-a^{-1}}", 16)
    f_ex7_question = formula_png(
        "b030_ex7_question",
        r"h(n)\ne0,\ N_0\leq n\leq N_1;\qquad x(n)\ne0,\ N_2\leq n\leq N_3",
        14,
    )
    f_ex7_interval = formula_png(
        "b031_ex7_interval",
        r"N_0+N_2\leq n\leq N_1+N_3,\qquad N_4=N_0+N_2,\quad N_5=N_1+N_3",
        14,
    )
    f_ex7_len = formula_png(
        "b032_ex7_len",
        r"M_h=N_1-N_0+1,\quad M_x=N_3-N_2+1,\quad M_y=M_h+M_x-1",
        14,
    )
    f_conv_comm = formula_png("b033_conv_comm", r"x(n)*h(n)=h(n)*x(n)", 16)
    f_conv_dist = formula_png("b033_conv_dist", r"x(n)*[h_1(n)+h_2(n)]=x(n)*h_1(n)+x(n)*h_2(n)", 15)
    f_conv_assoc = formula_png("b033_conv_assoc", r"x(n)*[h_1(n)*h_2(n)]=[x(n)*h_1(n)]*h_2(n)", 15)
    f_causal = formula_png("b036_causal", r"h(n)=0,\quad n<0", 16)
    f_causal_conv = formula_png("b036_causal_conv", r"y(n)=x(n)*h(n)=\sum_{m=-\infty}^{\infty}x(m)h(n-m)", 15)
    f_causal_future = formula_png("b036_causal_future", r"m>n\Rightarrow n-m<0,\qquad h(n-m)=0", 14)
    f_stable = formula_png("b037_stable", r"\sum_{n=-\infty}^{\infty}|h(n)|<\infty", 17)
    f_stable_bound = formula_png("b037_stable_bound", r"|y(n)|\leq M\sum_{m=-\infty}^{\infty}|h(m)|<\infty", 15)
    f_ex8_1 = formula_png("b038_ex8_1", r"y(n)=\sum_{k=0}^{N-1}x(n-k)", 15)
    f_ex8_2 = formula_png("b038_ex8_2", r"y(n)=\sum_{k=n-n_0}^{n+n_0}x(k)", 15)
    f_ex8_3 = formula_png("b038_ex8_3", r"y(n)=x(n-n_0)", 15)
    f_ex8_4 = formula_png("b038_ex8_4", r"h(n)=a^n u(n),\quad a>0", 15)
    f_diff = formula_png("b040_diff", r"y(n)=\sum_{i=0}^{M}b_i x(n-i)-\sum_{i=1}^{N}a_i y(n-i)", 17)
    f_ex9_ans = formula_png("b043_ex9_ans", r"y(n)-2y(n-1)+y(n-2)=x(n)", 16)
    f_ex10_q = formula_png("b044_ex10_q", r"y(n)+2y(n-1)-3y(n-2)=x(n)-2x(n-1)", 16)
    f_ex10_g1 = formula_png("b045_ex10_g1", r"g(n)+2g(n-1)-3g(n-2)=x(n)", 15)
    f_ex10_g2 = formula_png("b045_ex10_g2", r"y(n)=g(n)-2g(n-1)", 15)

    doc = BatchDoc(PDF_PATH)
    doc.section = "3. 时域离散系统"
    doc.start()

    # Chapter 3 title and system definition are carried by the sample tail page.
    # Section 3.1 is carried by the sample tail page.

    doc.h2("3.2 时不变（考点）")
    doc.p("设 x2(n)=x1(n-n0)，x1(n) 经过系统的输出为 y1(n)。如果对所有 n0，在任意 n 时刻输入 x1(n-n0)，输出都是 y1(n-n0)，则称该系统为时不变系统，用以下式子表达：")
    draw_formula(doc, f_time_shift, max_h=28)
    doc.note("判断口径", "先延时输入再过系统，与先过系统再延时输出；两条路径结果相同就是时不变。", compact=True)

    doc.h2("例 3  判断系统是否线性、是否时不变")
    doc.p("判断以下系统是否是线性，是否时不变。都满足时即为 LTI 系统。")
    draw_formula_pair(doc, f_ex3_a, "判断第一个系统。")
    draw_formula_pair(doc, f_ex3_b, "判断累加系统。")
    doc.h3("解")
    draw_formula_pair(doc, f_ex3_a_nonlin, "不满足齐次性，因此非线性。")
    draw_formula_pair(doc, f_ex3_a_ti, "输入延时后输出随之延时，因此时不变。")
    draw_formula_pair(doc, f_ex3_b_lin, "求和运算对输入保持叠加性和齐次性，因此线性。")
    draw_formula_pair(doc, f_ex3_b_tv, "由于求和下限固定，输入延时后求和范围不随输出同步延时，因此时变。")
    doc.exercise_space(38)

    doc.h2("3.3 线性时不变系统")
    doc.p("任意输入是否可以用输入和单位脉冲序列表示？")
    doc.p("由单位脉冲序列的筛选性质，可将任意序列写成：")
    draw_formula(doc, f_impulse_decomp, max_h=38)
    doc.p("设线性时不变系统输入为 δ(n) 时的输出是 h(n)，将 h(n) 称为冲激响应，即脉冲序列经过线性时不变系统后的输出。")
    draw_formula_pair(doc, f_lti_shift, "由时不变性得到。")
    draw_formula_pair(doc, f_lti_homo, "由齐次性得到。")
    doc.p("然后根据叠加性，输出为")
    draw_formula(doc, f_lti_output, max_h=36)
    doc.p("定义卷积：")
    draw_formula(doc, f_conv_def, max_h=36)
    doc.ensure(150)
    doc.p("那么任意序列与单位脉冲序列满足")
    draw_formula(doc, f_conv_identity, max_h=30)
    doc.note("考点提示", "线性时不变系统的核心是冲激响应 h(n)。后续卷积和、差分方程、系统框图都围绕 h(n) 或等价的系统关系展开。", compact=True)

    doc.h2("3.4 卷积和的计算（考点）")
    doc.h3("图解法")
    doc.p("例 4：计算下列卷积，条件为")
    draw_formula(doc, f_ex4_title, max_h=26)
    draw_ex4_plots(doc)
    doc.ensure(150)
    doc.h3("解")
    doc.p("原式为")
    draw_formula(doc, f_ex4_sum, max_h=32)
    doc.bullet([
        "n<0 时，u(n-m) 左移后与 a^m u(m) 无交集，卷积结果为 0。",
        "n≥0 时，非零区间产生有限项求和，结果为等比数列部分和。",
    ])
    draw_formula(doc, f_ex4_result, max_h=34)
    doc.exercise_space(28)

    doc.h3("列表法")
    doc.p("例 5：求")
    draw_formula(doc, f_ex5_title, max_h=24)
    doc.p("矩形序列可理解为连续若干个 1。列表卷积时，将一个序列逐项平移并纵向相加。")
    draw_formula(doc, f_ex5_r3, max_h=20)
    draw_formula(doc, f_ex5_r4, max_h=20)
    draw_conv_vertical_working(doc)
    draw_formula(doc, f_ex5_result, max_h=26)

    doc.h3("解析法")
    doc.p("例 6：设")
    draw_formula(doc, f_ex6_title, max_h=26)
    doc.p("由卷积定义得")
    draw_formula(doc, f_ex6_sum, max_h=34)
    doc.p("求上下限：只有当以下两个条件同时满足时，乘积才可能非零。")
    draw_formula(doc, f_ex6_bounds, max_h=24)
    doc.bullet([
        "n<0 时，不存在同时满足条件的 m，因此 y(n)=0。",
        "0≤n≤3 时，非零求和范围为 0≤m≤n。",
        "n≥4 时，非零求和范围为 0≤m≤3。",
    ])
    draw_formula(doc, f_ex6_mid_cond, max_h=20)
    draw_formula(doc, f_ex6_mid_sum, max_h=32)
    draw_formula(doc, f_ex6_mid_result, max_h=32)
    draw_formula(doc, f_ex6_tail_cond, max_h=20)
    draw_formula(doc, f_ex6_tail_sum, max_h=32)
    draw_formula(doc, f_ex6_tail_result, max_h=32)
    doc.note("考点提示", "解析法的关键不是死记结论，而是先写出卷积和，再由两个因子各自的非零区间求 m 的上下限。", compact=True)

    doc.h2("例 7  有限长序列卷积的范围")
    doc.p("已知 h(n) 与 x(n) 分别只在下列区间内非零，求输出 y(n) 的非零区间，并用长度 M_h、M_x 表示 M_y。")
    draw_formula(doc, f_ex7_question, max_h=28)
    doc.h3("解")
    doc.p("由卷积和")
    draw_formula(doc, f_lti_output, max_h=30)
    doc.p("可知 h(m) 非零要求 N0≤m≤N1；x(n-m) 非零要求 N2≤n-m≤N3。只有两个区间存在交集时，y(n) 才可能非零。")
    draw_formula(doc, f_ex7_interval, max_h=30)
    doc.p("有限长序列长度等于末端序号减起始序号再加 1，因此")
    draw_formula(doc, f_ex7_len, max_h=30)
    doc.p("814 考点提示：有限长序列卷积长度常直接考，输出长度等于两个输入长度相加再减 1。", size=9.2, leading=14)
    doc.exercise_space(10)

    doc.h2("3.5 卷积的性质")
    doc.p("卷积和常用的三个性质如下。计算前先观察能否利用这些性质化简。")
    doc.h3("1. 交换律")
    draw_formula(doc, f_conv_comm, max_h=28)
    doc.h3("2. 分配律")
    draw_formula(doc, f_conv_dist, max_h=30)
    doc.h3("3. 结合律")
    draw_formula(doc, f_conv_assoc, max_h=30)

    doc.h2("3.6 性质的作用")
    doc.p("卷积性质在系统互连中有直接解释。两个 LTI 系统串联时，等效冲激响应为卷积；并联后相加时，等效冲激响应为各支路冲激响应之和。")
    draw_lti_interconnects(doc)
    doc.note("方法选择", "求卷积时先看输入与输出表达式。序列较短可用列表或竖式；序列复杂时用作图或解析式；计算前优先尝试交换律、分配律和结合律。", compact=True)

    doc.h2("3.7 系统的因果性和稳定性")
    doc.h3("1. 因果性")
    doc.p("因果系统的当前输出只能由当前和过去输入决定，不能由未来输入决定。对线性时不变系统，有以下等价判据：")
    draw_formula(doc, f_causal, max_h=26)
    doc.p("利用卷积和可以看出：")
    draw_formula(doc, f_causal_conv, max_h=34)
    doc.p("若求和项对应未来输入，为了使输出与未来输入无关，必须满足下式，即冲激响应在负时间为 0。")
    draw_formula(doc, f_causal_future, max_h=26)
    doc.h3("2. 稳定性")
    doc.p("系统稳定，是指任意有界输入都产生有界输出。对 LTI 系统，稳定性与冲激响应绝对可和等价：")
    draw_formula(doc, f_stable, max_h=32)
    doc.p("若 |x(n)|<M，则")
    draw_formula(doc, f_stable_bound, max_h=34)
    doc.note("814 考点提示", "判断 LTI 系统时，因果看 h(n) 在 n<0 是否为 0；稳定看 h(n) 是否绝对可和。两个判据经常和系统函数、差分方程一起考。", compact=True)

    doc.h2("例 8  判断系统是否因果稳定")
    doc.p("分析以下系统是否为因果稳定系统。")
    draw_formula_pair(doc, f_ex8_1, "有限滑动和。")
    draw_formula_pair(doc, f_ex8_2, "中心随 n 变化的有限区间求和。")
    draw_formula_pair(doc, f_ex8_3, "延时或超前系统。")
    draw_formula_pair(doc, f_ex8_4, "LTI 系统，冲激响应为实指数序列。")
    doc.h3("解")
    doc.bullet([
        "1. 因果性：若 N<1，则会出现未来输入项，非因果；若 N>=1，则只含当前和过去输入，因果。稳定性：有限项求和，有界输入产生有界输出，稳定。",
        "2. 因果性：当 n0 不为 0 时，求和区间含未来输入，非因果；n0=0 时因果。稳定性：有限项求和，稳定。",
        "3. 因果性：n0<0 时为超前，非因果；n0>=0 时因果。稳定性：有界输入延时或超前后仍有界，稳定。",
        "4. 因果性：冲激响应在负时间为 0，因此因果。稳定性：当 a 介于 0 与 1 之间时绝对可和，稳定；当 a 大于或等于 1 时不稳定。",
    ])
    doc.exercise_space(22)

    doc.section = "4. 差分方程和系统框图"
    doc.h1("04 差分方程和系统框图")
    doc.h2("4.1 差分方程")
    doc.p("对模拟系统，常用微分方程描述输入和输出的关系；对时域离散系统，则用差分方程描述输入和输出的关系。一个 N 阶线性常系数差分方程可写为：")
    draw_formula(doc, f_diff, max_h=38)
    doc.p("差分方程的求解可以类比模拟系统微分方程的齐次解、特解，但直接求解较繁琐；后续通常借助 z 变换来处理。")

    doc.h2("4.2 系统框图")
    doc.p("数字信号处理的三种基本运算是加法、乘法和单位延迟。系统框图可由这些基本运算单元连接而成。")
    draw_basic_ops(doc)

    doc.h2("例 9  由系统框图写差分方程")
    doc.p("写出可以表示下图所示系统的差分方程。")
    draw_example9_block(doc)
    doc.h3("解")
    doc.p("由图可知，输入 x(n)、反馈项 2y(n-1) 与 -y(n-2) 在加法器处相加得到 y(n)，整理得：")
    draw_formula(doc, f_ex9_ans, max_h=30)
    doc.exercise_space(18)

    doc.h2("例 10  由差分方程画系统框图")
    doc.p("根据以下差分方程画出系统框图：")
    draw_formula(doc, f_ex10_q, max_h=32)
    doc.h3("解")
    doc.p("引入中间变量 g(n)，先把右端输入部分与左端反馈部分分开：")
    draw_formula(doc, f_ex10_g1, max_h=30)
    draw_formula(doc, f_ex10_g2, max_h=28)
    draw_example10_block(doc)
    doc.note("814 考点提示", "由框图写方程时先沿信号流标出各延时节点；由方程画框图时先把最高阶输出项整理成当前输出，再按延时、乘系数、相加三步搭建。", compact=True)

    doc.save()

    NOTE_PATH.write_text(
        """# DSP讲义重制_第二批_原PPT16-45页_校对记录

## 范围

- 原 PPT 页码：16-45
- 输出：`outputs/DSP讲义重制_第二批_原PPT16-45页_初稿.pdf`

## 内容处理

- 内容顺序按原 PPT：例 2 收尾、时域离散系统、线性、时不变、例 3、线性时不变系统、卷积和定义、例 4、例 5 列表法、例 6 解析法、例 7 有限长序列范围、卷积性质、因果稳定、例 8、差分方程和系统框图、例 9、例 10。
- 原 PPT 中的水印未进入重制 PDF。
- 公式均按参考讲义风格重新渲染为数学公式。
- `/` 形式未用于公式表达；涉及比值时使用分数形式。
- 例题按普通小节呈现，未使用大边框；保留适当书写空白。
- 系统互连图、基本运算图、例 9 和例 10 系统框图均重新绘制，未直接截取 PPT 水印图。

## 校对说明

- 本批未主动改写知识点含义，仅将 PPT 口语化/大字号内容改为讲义连续排版。
- 例 3 的判断结论按原 PPT 保留：`y(n)=x^2(n)` 非线性、时不变；累加系统线性、时变。
- 例 4 结论按原 PPT 保留：`a^n u(n)*u(n)=((1-a^{n+1})/(1-a))u(n)`，版面中改用分数形式显示。
- 例 5 列表法结果按原 PPT 保留为 `1,2,3,3,2,1`。
- 例 6 按原 PPT 的上下限分析分为 `n<0`、`0≤n≤3`、`n≥4` 三段。
- 例 7 保留原 PPT 结论：`N4=N0+N2`、`N5=N1+N3`、`My=Mh+Mx-1`。
- 因果性判据中将原 PPT 挤在一起的表达规范化为 `h(n)=0, n<0`。
- 稳定性判据保留为冲激响应绝对可和。
- 例 8 判断结论按原 PPT 保留，并把条件写成规范数学表达。
- 例 9 答案保留为 `y(n)-2y(n-1)+y(n-2)=x(n)`。
- 例 10 保留原 PPT 的中间变量法：`g(n)+2g(n-1)-3g(n-2)=x(n)`，`y(n)=g(n)-2g(n-1)`。
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    build_pdf()
    print(PDF_PATH)
