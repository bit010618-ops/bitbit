from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from PIL import Image

from make_dsp_sample_handout_v2 import (
    BLUE,
    CONTENT_W,
    FORMULA_DIR,
    LINE,
    MARGIN_X,
    OUT_DIR,
    TEXT,
    draw_auto_math_block,
    draw_discrete_axes_plot,
    formula_png,
    register_fonts,
    normalize_display_formula_height,
    wrap,
)
from make_dsp_batch_016_024 import BatchDoc, draw_formula


PDF_PATH = OUT_DIR / "DSP讲义重制_第三批_原PPT46-88页_z变换DTFT_性质补全版.pdf"
NOTE_PATH = OUT_DIR / "DSP讲义重制_第三批_原PPT46-88页_z变换DTFT_性质补全版_校对记录.md"
SOURCE_AXIS_BLUE = colors.HexColor("#0046D8")
SOURCE_SAMPLE_RED = colors.HexColor("#E60012")


def draw_formula_left(doc, image_path, max_w=None, max_h=30, gap=10, indent=0):
    max_h = normalize_display_formula_height(max_h)
    doc.ensure(max_h + gap)
    c = doc.c
    im = Image.open(image_path)
    iw, ih = im.size
    max_w = max_w or CONTENT_W * 0.82
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    x = MARGIN_X + indent
    y = doc.y - dh
    c.drawImage(ImageReader(str(image_path)), x, y, dw, dh, mask="auto")
    doc.y -= dh + gap


def draw_formula_rows(doc, rows, max_h=24, gap=7):
    for image_path in rows:
        draw_formula(doc, image_path, max_h=max_h, gap=gap)


def append_chapter_review(doc):
    doc.h2("本章导图与课后题")
    doc.p("本阶段已经完成 Z 变换、逆 Z 变换、Z 变换性质以及 DTFT 定义与性质。",size=9.2,leading=13)
    doc.bullet([
        "复习时把变换式、收敛域和对应时域序列放在一起判断。",
        "重点练习右边序列、左边序列、双边序列以及由 ROC 反推序列。",
        "DTFT 性质需同时记住名称与公式，特别是位移、调制、反褶、共轭对称和卷积。",
    ], leading=13)
    doc.h3("课后题")
    doc.p("按原课件课后题继续练习 Z 变换与 DTFT，涉及单边/双边变换时务必写明收敛域。", size=9.2, leading=13)


def draw_property(doc, label, formulas, max_h=24, gap=8):
    max_h = normalize_display_formula_height(max_h)
    if not isinstance(formulas, (list, tuple)):
        formulas = [formulas]
    row_h = max_h * len(formulas) + 8
    doc.ensure(row_h + gap)
    c = doc.c
    y_top = doc.y
    c.setFillColor(TEXT)
    c.setFont("CNB", 10.2)
    c.drawString(MARGIN_X, y_top - 14, label)
    y = y_top
    for image_path in formulas:
        im = Image.open(image_path)
        iw, ih = im.size
        scale = min((CONTENT_W - 158) / iw, max_h / ih)
        dw, dh = iw * scale, ih * scale
        x = MARGIN_X + 152 + (CONTENT_W - 158 - dw) / 2
        y -= dh + 2
        c.drawImage(ImageReader(str(image_path)), x, y, dw, dh, mask="auto")
        y -= 5
    doc.y = min(doc.y - row_h - gap, y - gap)


def draw_red_text(doc, text, size=9.4, leading=17):
    lines = wrap(text, CONTENT_W, "CNB", size)
    doc.ensure(len(lines) * leading + 8)
    bottom = draw_auto_math_block(
        doc.c,
        MARGIN_X,
        doc.y + size - leading,
        text,
        CONTENT_W,
        font="CNB",
        size=size,
        leading=leading,
        color=colors.HexColor("#D71920"),
    )
    doc.c.setFillColor(TEXT)
    doc.y = bottom + leading - size - 14


def draw_formula_table(doc, headers, rows, col_widths, row_h=42):
    total_h = row_h * (len(rows) + 1)
    doc.ensure(total_h + 12)
    c = doc.c
    x0 = MARGIN_X
    y0 = doc.y
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.setFillColor(BLUE)
    c.rect(x0, y0 - row_h, sum(col_widths), row_h, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("CNB", 9.5)
    x = x0
    for head, w in zip(headers, col_widths):
        c.drawCentredString(x + w / 2, y0 - row_h / 2 - 3, head)
        x += w
    c.setFillColor(TEXT)
    for r, row in enumerate(rows):
        yy = y0 - row_h * (r + 2)
        if r % 2 == 0:
            c.setFillColor(colors.HexColor("#F6F9FC"))
            c.rect(x0, yy, sum(col_widths), row_h, stroke=0, fill=1)
        c.setFillColor(TEXT)
        x = x0
        for cell, w in zip(row, col_widths):
            c.setStrokeColor(LINE)
            c.rect(x, yy, w, row_h, stroke=1, fill=0)
            if isinstance(cell, Path):
                im = Image.open(cell)
                iw, ih = im.size
                scale = min((w - 12) / iw, (row_h - 10) / ih)
                dw, dh = iw * scale, ih * scale
                c.drawImage(ImageReader(str(cell)), x + (w - dw) / 2, yy + (row_h - dh) / 2, dw, dh, mask="auto")
            else:
                c.setFont("CN", 9.2)
                c.drawCentredString(x + w / 2, yy + row_h / 2 - 3, cell)
            x += w
    x = x0
    c.setStrokeColor(LINE)
    for w in col_widths:
        c.rect(x, y0 - total_h, w, total_h, stroke=1, fill=0)
        x += w
    doc.y -= total_h + 14


def draw_source_mini(doc, source_name, caption, max_h=112):
    src = Path("work/pdfs/source_pages_046_090") / source_name
    if not src.exists():
        return
    doc.ensure(max_h + 28)
    c = doc.c
    im = Image.open(src)
    iw, ih = im.size
    scale = min((CONTENT_W * 0.62) / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    x = MARGIN_X + (CONTENT_W - dw) / 2
    y = doc.y - dh
    c.drawImage(ImageReader(str(src)), x, y, dw, dh)
    c.setFillColor(TEXT)
    c.setFont("CN", 8.8)
    c.drawCentredString(MARGIN_X + CONTENT_W / 2, y - 12, caption)
    doc.y = y - 24


def draw_dtft_mapping(doc):
    doc.ensure(116)
    c = doc.c
    y = doc.y - 10
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.setLineWidth(1.0)
    x1 = MARGIN_X + 90
    x2 = MARGIN_X + 310
    cy = y - 55

    def axis(cx, cy, w, h, xlabel, ylabel):
        c.line(cx - w / 2, cy, cx + w / 2, cy)
        c.line(cx + w / 2, cy, cx + w / 2 - 6, cy + 3)
        c.line(cx + w / 2, cy, cx + w / 2 - 6, cy - 3)
        c.line(cx, cy - h / 2, cx, cy + h / 2)
        c.line(cx, cy + h / 2, cx - 3, cy + h / 2 - 6)
        c.line(cx, cy + h / 2, cx + 3, cy + h / 2 - 6)
        c.setFont("CN", 8.4)
        c.drawString(cx + w / 2 + 4, cy - 4, xlabel)
        c.drawString(cx + 4, cy + h / 2 + 2, ylabel)
        c.drawString(cx - 10, cy - 13, "O")

    axis(x1, cy, 140, 86, "Re s", "j Im s")
    c.setFont("CN", 8.4)
    c.drawString(x1 - 28, cy + 20, "虚轴")

    axis(x2, cy, 150, 104, "Re z", "Im z")
    c.circle(x2, cy, 38, stroke=1, fill=0)
    c.line(x2, cy, x2 + 32, cy + 22)
    c.setFont("CN", 8.4)
    c.drawString(x2 + 36, cy + 18, "ω")
    c.drawString(x2 + 41, cy - 12, "+1")
    label = formula_png("b079_unit_circle_label", r"z=e^{j\omega}", 11)
    im = Image.open(label)
    scale = min(65 / im.width, 18 / im.height)
    dw, dh = im.width * scale, im.height * scale
    c.drawImage(ImageReader(str(label)), x2 + 42, cy + 26, dw, dh, mask="auto")
    doc.y = y - 104


def draw_dtft_conj_example_plots(doc):
    panel_gap = 82
    doc.ensure(panel_gap * 3 + 8)
    c = doc.c
    y = doc.y
    half_label = formula_png(
        "b087_plot_half_label", r"\frac{1}{2}", 10, color="#E60012"
    )
    negative_half_label = formula_png(
        "b087_plot_negative_half_label", r"-\frac{1}{2}", 10, color="#E60012"
    )
    panels = [
        ("e", {-1: 0.5, 0: 1, 1: 0.5}),
        ("o", {-1: -0.5, 0: 0, 1: 0.5}),
        (None, {0: 1, 1: 1}),
    ]

    def arrow(x1, y1, x2, y2):
        c.line(x1, y1, x2, y2)
        if x1 == x2:
            c.line(x2, y2, x2 - 3.5, y2 - 6)
            c.line(x2, y2, x2 + 3.5, y2 - 6)
        else:
            c.line(x2, y2, x2 - 6, y2 + 3.5)
            c.line(x2, y2, x2 - 6, y2 - 3.5)

    def formula_label(image_path, center_x, center_y, max_w=24, max_h=17):
        im = Image.open(image_path)
        iw, ih = im.size
        scale = min(max_w / iw, max_h / ih)
        dw, dh = iw * scale, ih * scale
        c.drawImage(
            ImageReader(str(image_path)),
            center_x - dw / 2,
            center_y - dh / 2,
            dw,
            dh,
            mask="auto",
        )

    x = MARGIN_X + 255
    width = 205
    x0 = x + 88
    x_step = 34
    for index, (subscript, values) in enumerate(panels):
        top_y = y - index * panel_gap
        y0 = top_y - 48
        c.setStrokeColor(SOURCE_AXIS_BLUE)
        c.setFillColor(SOURCE_AXIS_BLUE)
        c.setLineWidth(1.1)
        arrow(x + 8, y0, x + width - 8, y0)
        arrow(x0, y0 - 20, x0, top_y - 6)
        c.setFont("CNB", 8.5)
        for n in range(-2, 3):
            px = x0 + n * x_step
            c.line(px, y0 - 2.5, px, y0 + 2.5)
            if n == 0:
                c.drawString(px + 5, y0 - 14, "0")
            else:
                c.drawCentredString(px, y0 - 14, str(n))
        c.drawString(x + width - 3, y0 - 4, "n")
        c.setFont("Times-Italic", 14)
        c.drawString(x0 + 8, top_y - 11, "h")
        title_x = x0 + 17
        if subscript:
            c.setFont("Times-Italic", 8)
            c.drawString(title_x, top_y - 15, subscript)
            title_x += 7
        c.setFont("Times-Italic", 14)
        c.drawString(title_x, top_y - 11, "(n)")

        c.setStrokeColor(SOURCE_SAMPLE_RED)
        c.setFillColor(SOURCE_SAMPLE_RED)
        c.setLineWidth(1.2)
        for n, value in sorted(values.items()):
            px = x0 + n * x_step
            py = y0 + value * 28
            c.line(px, y0, px, py)
            c.circle(px, py, 2.5, stroke=1, fill=1)
            if value == 1:
                c.setFont("CNB", 7.5)
                c.drawString(px + 10, py + 2, "1")
            elif value == 0.5:
                formula_label(half_label, px + 10, py + 10)
            elif value == -0.5:
                formula_label(negative_half_label, px, py - 13)
    doc.y -= panel_gap * 3


def build_pdf():
    register_fonts()

    f_sampling = formula_png(
        "b050_sampling_laplace",
        r"x_s(t)=\sum_{n=-\infty}^{\infty}x(nT)\delta(t-nT),\quad X_s(s)=\sum_{n=-\infty}^{\infty}x(nT)e^{-snT}",
        14,
    )
    f_z_def = formula_png("b051_z_def", r"X(z)=\sum_{n=-\infty}^{\infty}x(n)z^{-n}", 18)
    f_z_inv = formula_png("b051_z_inv", r"x(n)=Z^{-1}[X(z)]=\frac{1}{2\pi j}\oint_C X(z)z^{n-1}\,dz", 16)
    f_roc_abs = formula_png("b054_roc_abs", r"\sum_{n=-\infty}^{\infty}\left|x(n)z^{-n}\right|<\infty", 16)
    f_right = formula_png("b055_right", r"X(z)=\sum_{n=n_1}^{\infty}x(n)z^{-n},\quad |z|>R_{x1}", 15)
    f_left = formula_png("b056_left", r"X(z)=\sum_{n=-\infty}^{n_2}x(n)z^{-n},\quad |z|<R_{x2}", 15)
    f_bilateral = formula_png("b057_bilateral", r"R_{x1}<|z|<R_{x2}", 18)
    f_example_pair = formula_png("b058_pair", r"x_1(n)=a^n u(n),\qquad x_2(n)=-a^n u(-n-1)", 16)
    f_x1 = formula_png("b058_x1", r"X_1(z)=\sum_{n=0}^{\infty}a^n z^{-n}=\frac{1}{1-a z^{-1}}=\frac{z}{z-a},\quad |z|>|a|", 15)
    f_x2 = formula_png("b058_x2", r"X_2(z)=-\sum_{n=-\infty}^{-1}a^n z^{-n}=\frac{z}{z-a},\quad |z|<|a|", 15)
    f_inv_general = formula_png(
        "b063_inv_general",
        r"X(z)=\frac{b_mz^m+b_{m-1}z^{m-1}+\cdots+b_1z+b_0}{z^n+a_{n-1}z^{n-1}+\cdots+a_1z+a_0}\quad(m\leq n)",
        13,
    )
    f_pf = formula_png("b064_pf", r"\frac{F(z)}{z}=\frac{z}{(z+1)(z-2)}=\frac{A}{z+1}+\frac{B}{z-2},\quad A=\frac{1}{3},\ B=\frac{2}{3}", 14)
    f_pf_question = formula_png("b064_pf_question", r"F(z)=\frac{z^2}{(z+1)(z-2)}", 16)
    f_pf2 = formula_png("b064_pf2", r"F(z)=\frac{1}{3}\frac{z}{z+1}+\frac{2}{3}\frac{z}{z-2}", 16)
    f_pf_rocs = formula_png("b064_pf_rocs", r"|z|>2,\qquad |z|<1,\qquad 1<|z|<2", 14)
    f_roc1 = formula_png("b065_roc1", r"|z|>2:\quad f(n)=\left[\frac{1}{3}(-1)^n+\frac{2}{3}2^n\right]u(n)", 15)
    f_roc2 = formula_png("b065_roc2", r"|z|<1:\quad f(n)=\left[-\frac{1}{3}(-1)^n-\frac{2}{3}2^n\right]u(-n-1)", 15)
    f_roc3 = formula_png("b065_roc3", r"1<|z|<2:\quad f(n)=\frac{1}{3}(-1)^n u(n)-\frac{2}{3}2^n u(-n-1)", 15)
    f_linear = formula_png("b070_linear", r"Z[ax(n)+by(n)]=aX(z)+bY(z),\quad R_-<|z|<R_+", 15)
    f_shift = formula_png("b072_shift", r"Z[x(n-m)]=z^{-m}X(z),\qquad Z[x(n+m)]=z^{m}X(z)", 15)
    f_shift_right = formula_png(
        "b072_shift_right",
        r"Z[x(n-m)u(n)]=z^{-m}\left[X(z)+\sum_{k=-m}^{-1}x(k)z^{-k}\right]",
        14,
    )
    f_shift_left = formula_png(
        "b072_shift_left",
        r"Z[x(n+m)u(n)]=z^{m}\left[X(z)-\sum_{k=0}^{m-1}x(k)z^{-k}\right]",
        14,
    )
    f_diff_eq_q = formula_png("b073_diff_eq_q", r"y(n)-0.9y(n-1)=0.05u(n),\qquad y(-1)=0", 14)
    f_diff_eq_z1 = formula_png("b073_diff_eq_z1", r"Y(z)-0.9z^{-1}Y(z)=\frac{0.05z}{z-1}", 14)
    f_diff_eq_z2 = formula_png("b073_diff_eq_z2", r"Y(z)=\frac{0.05z^2}{(z-0.9)(z-1)}", 14)
    f_diff_eq_pf = formula_png("b073_diff_eq_pf", r"\frac{Y(z)}{z}=\frac{A}{z-0.9}+\frac{B}{z-1},\qquad A=-0.45,\quad B=0.5", 14)
    f_diff_eq_yz = formula_png("b073_diff_eq_yz", r"Y(z)=\frac{-0.45z}{z-0.9}+\frac{0.5z}{z-1}", 14)
    f_diff_eq_yn = formula_png("b073_diff_eq_yn", r"y(n)=\left[-0.45(0.9)^n+0.5\right]u(n)", 15)
    f_linear_given = formula_png("b070_linear_given", r"Z[x(n)]=X(z),\quad R_{x-}<|z|<R_{x+};\qquad Z[y(n)]=Y(z),\quad R_{y-}<|z|<R_{y+}", 13)
    f_linear_roc = formula_png("b070_linear_roc", r"R_+=\min(R_{x+},R_{y+}),\qquad R_-=\max(R_{x-},R_{y-})", 14)
    f_linear_ex = formula_png(
        "b071_linear_ex",
        r"Z[a^n u(n)-a^n u(n-1)]=\frac{z}{z-a}-\frac{a}{z-a}=1",
        14,
    )
    f_linear_ex_question = formula_png("b071_linear_ex_question", r"a^n u(n)-a^n u(n-1)", 15)
    f_linear_ex_roc = formula_png("b071_linear_ex_roc", r"|z|>|a|", 15)
    f_shift_given = formula_png("b072_shift_given", r"Z[x(n)]=X(z)", 15)
    f_unilateral_base = formula_png("b072_unilateral_base", r"Z[x(n)u(n)]=X(z)", 15)
    f_scale_unilateral_ex = formula_png("b074_scale_unilateral_ex", r"(-1)^n u(n)", 15)
    f_scale = formula_png("b074_scale", r"Z[a^n x(n)]=X\!\left(\frac{z}{a}\right),\qquad R_{x1}<\left|\frac{z}{a}\right|<R_{x2}", 14)
    f_scale_inv = formula_png("b074_scale_inv", r"Z[a^{-n}x(n)]=X(az),\qquad R_{x1}<|az|<R_{x2}", 14)
    f_scale_cos_question = formula_png("b075_scale_cos_question", r"Z[\cos(\omega_0 n)u(n)]\quad \Longrightarrow \quad Z[\beta^n\cos(\omega_0 n)u(n)]", 14)
    f_scale_cos_known = formula_png("b075_scale_cos_known", r"Z[\cos(\omega_0 n)u(n)]=\frac{z(z-\cos\omega_0)}{z^2-2z\cos\omega_0+1},\quad |z|>1", 13)
    f_scale_cos_beta = formula_png(
        "b075_scale_cos_beta",
        r"Z[\beta^n\cos(\omega_0 n)u(n)]=\frac{z^2-\beta z\cos\omega_0}{z^2-2\beta z\cos\omega_0+\beta^2},\quad |z|>|\beta|",
        13,
    )
    f_mul_n = formula_png("b076_muln", r"Z[nx(n)]=-z\frac{dX(z)}{dz}", 16)
    f_mul_nm = formula_png("b076_mulnm", r"Z[n^m x(n)]=\left[-z\frac{d}{dz}\right]^mX(z)", 15)
    f_mul_nu = formula_png("b076_nu", r"Z[nu(n)]=-z\frac{d}{dz}\left(\frac{z}{z-1}\right)=\frac{z}{(z-1)^2}", 14)
    f_mul_nu_question = formula_png("b076_nu_question", r"Z[u(n)]\quad \Longrightarrow \quad Z[nu(n)]", 14)
    f_initial = formula_png("b077_initial", r"x(0)=\lim_{z\to\infty}X(z)", 15)
    f_final = formula_png("b077_final", r"x(\infty)=\lim_{z\to1}(z-1)X(z)", 15)
    f_conv_z_full = formula_png(
        "b077_convz_full",
        r"Z[x(n)*h(n)]=X(z)H(z),\quad \max(R_{x1},R_{h1})<|z|<\min(R_{x2},R_{h2})",
        13,
    )
    f_conv_z = formula_png("b077_convz", r"Z[x_1(n)*x_2(n)]=X_1(z)X_2(z)", 16)
    f_conv_ex = formula_png(
        "b078_conv_ex",
        r"X(z)=\frac{z}{z-1},\quad H(z)=\frac{z-1}{z-a},\quad Y(z)=X(z)H(z)=\frac{z}{z-a},\quad |z|>|a|",
        13,
    )
    f_conv_ex_question = formula_png(
        "b078_conv_ex_question",
        r"x(n)=u(n),\qquad h(n)=a^n u(n)-a^{n-1}u(n-1),\qquad |a|<1",
        14,
    )
    f_conv_ex_roc = formula_png("b078_conv_ex_roc", r"|z|>|a|", 15)
    f_dtft_def = formula_png(
        "b079_dtft_def",
        r"DTFT[x(n)]=X(e^{j\omega})=X(z)|_{z=e^{j\omega}}=\sum_{n=-\infty}^{\infty}x(n)e^{-j n\omega}",
        15,
    )
    f_dtft_inv = formula_png("b080_dtft_inv", r"x(n)=\frac{1}{2\pi}\int_{-\pi}^{\pi}X(e^{j\omega})e^{j n\omega}\,d\omega", 16)
    f_dtft_period = formula_png("b082_dtft_period", r"X(e^{j(\omega+2\pi)})=X(e^{j\omega})", 16)
    f_dtft_assume = formula_png("b084_dtft_assume", r"DTFT[x(n)]=X(e^{j\omega})", 15)
    f_dtft_lin = formula_png("b084_dtft_lin", r"DTFT[a x(n)+b y(n)]=aX(e^{j\omega})+bY(e^{j\omega})", 14)
    f_dtft_lin_full = formula_png(
        "b084_dtft_lin_full",
        r"DTFT[ax_1(n)+bx_2(n)]=aX_1(e^{j\omega})+bX_2(e^{j\omega})",
        14,
    )
    f_dtft_shift = formula_png("b084_dtft_shift", r"DTFT[x(n-n_0)]=e^{-j\omega n_0}X(e^{j\omega})", 14)
    f_dtft_mod = formula_png("b084_dtft_mod", r"DTFT[x(n)e^{j\omega_0n}]=X(e^{j(\omega-\omega_0)})", 14)
    f_dtft_nx = formula_png("b085_dtft_nx", r"DTFT[nx(n)]=j\frac{d}{d\omega}X(e^{j\omega})", 14)
    f_dtft_rev = formula_png("b085_dtft_rev", r"DTFT[x(-n)]=X(e^{-j\omega})", 14)
    f_dtft_conj_def = formula_png(
        "b085_dtft_conj_def",
        r"x_e(n)=x_e^*(-n),\qquad x_o(n)=-x_o^*(-n)",
        14,
    )
    f_dtft_conj_expand = formula_png(
        "b085_dtft_conj_expand",
        r"x_e(n)=x_{er}(n)+jx_{ei}(n),\qquad x_e^*(-n)=x_{er}(-n)-jx_{ei}(-n)",
        13,
    )
    f_conj_parts = formula_png(
        "b085_conj_parts",
        r"x_e(n)=\frac{1}{2}[x(n)+x^*(-n)],\qquad x_o(n)=\frac{1}{2}[x(n)-x^*(-n)]",
        14,
    )
    f_dtft_real_imag = formula_png(
        "b086_real_imag",
        r"DTFT[x_r(n)]=X_e(e^{j\omega}),\qquad DTFT[jx_i(n)]=X_o(e^{j\omega})",
        14,
    )
    f_dtft_conj_parts = formula_png(
        "b086_conj_parts_ft",
        r"DTFT[x_e(n)]=\operatorname{Re}[X(e^{j\omega})],\qquad DTFT[x_o(n)]=j\operatorname{Im}[X(e^{j\omega})]",
        14,
    )
    f_dtft_ex_hr = formula_png("b087_ex_hr", r"H_R(e^{j\omega})=1+\cos\omega=1+\frac{1}{2}(e^{j\omega}+e^{-j\omega})", 14)
    f_dtft_ex_question = formula_png("b087_ex_question", r"H_R(e^{j\omega})=1+\cos\omega", 15)
    f_dtft_ex_he = formula_png("b087_ex_he", r"h_e(n)=\delta(n)+\frac{1}{2}\delta(n+1)+\frac{1}{2}\delta(n-1)", 14)
    f_dtft_ex_conditions = formula_png(
        "b087_ex_conditions",
        r"h(n)=0,\ n<0;\qquad h_o(-1)=-\frac{1}{2},\quad h_o(0)=0,\quad h_o(1)=\frac{1}{2}",
        13,
    )
    f_dtft_ex_result = formula_png("b087_ex_result", r"h(n)=\delta(n)+\delta(n-1),\qquad H(e^{j\omega})=1+e^{-j\omega}", 15)
    f_dtft_time_conv = formula_png("b088_time_conv", r"DTFT[x(n)*h(n)]=X(e^{j\omega})H(e^{j\omega})", 15)
    f_dtft_freq_conv = formula_png(
        "b088_freq_conv",
        r"DTFT[x(n)h(n)]=\frac{1}{2\pi}\int_{-\pi}^{\pi}X(e^{j\theta})H(e^{j(\omega-\theta)})\,d\theta",
        14,
    )
    f_dtft_parseval = formula_png(
        "b088_parseval",
        r"\sum_{n=-\infty}^{\infty}|x(n)|^2=\frac{1}{2\pi}\int_{-\pi}^{\pi}|X(e^{j\omega})|^2\,d\omega",
        14,
    )

    common_rows = [
        (formula_png("b062_seq_delta", r"\delta(n)", 13), formula_png("b062_t_delta", r"1", 13), "全平面"),
        (formula_png("b062_seq_u", r"u(n)", 13), formula_png("b062_t_u", r"\frac{z}{z-1}", 13), r"|z|>1"),
        (formula_png("b062_seq_au", r"a^n u(n)", 13), formula_png("b062_t_au", r"\frac{z}{z-a}", 13), r"|z|>|a|"),
        (formula_png("b062_seq_left", r"-a^n u(-n-1)", 13), formula_png("b062_t_left", r"\frac{z}{z-a}", 13), r"|z|<|a|"),
        (formula_png("b062_seq_nau", r"n a^n u(n)", 13), formula_png("b062_t_nau", r"\frac{a z}{(z-a)^2}", 13), r"|z|>|a|"),
        (formula_png("b062_seq_cos", r"\cos(\omega_0 n)u(n)", 12), formula_png("b062_t_cos", r"\frac{z(z-\cos\omega_0)}{z^2-2z\cos\omega_0+1}", 11), r"|z|>1"),
        (formula_png("b062_seq_sin", r"\sin(\omega_0 n)u(n)", 12), formula_png("b062_t_sin", r"\frac{z\sin\omega_0}{z^2-2z\cos\omega_0+1}", 11), r"|z|>1"),
    ]

    doc = BatchDoc(PDF_PATH)
    doc.section = "2. 离散时间傅里叶分析与Z变换"
    doc.start()
    doc.h1("02 离散时间傅里叶分析与Z变换")
    doc.p("本章从 z 变换开始，再讨论离散时间傅里叶变换 DTFT。z 变换的收敛域决定序列类型，DTFT 可看作 z 变换在单位圆上的取值。")
    doc.note("814 考点提示", "本章常考 z 变换收敛域、逆 z 变换、z 变换性质和 DTFT 性质。做题时一定同时写出变换式和收敛域。", compact=True)

    doc.h2("2.1 z 变换")
    doc.h3("2.1.1 定义与收敛域")
    doc.p("从抽样信号的拉普拉斯变换出发，引入 z 与 s 的指数映射，即可得到序列的 z 变换。也可以直接对离散序列定义双边 z 变换。")
    draw_formula(doc, formula_png("b050_z_s_map", r"z=e^{sT}", 16), max_h=24)
    draw_formula_rows(doc, [f_sampling], max_h=38, gap=9)
    draw_formula(doc, f_z_def, max_h=34)
    doc.p("使级数绝对收敛的 z 平面区域称为收敛域 ROC。不同 ROC 会对应不同的时间序列，因此不能只写 X(z) 而漏写 ROC。")
    draw_formula(doc, f_roc_abs, max_h=28)
    draw_formula_rows(doc, [f_right, f_left, f_bilateral], max_h=27, gap=8)
    doc.bullet([
        "有限长序列：ROC 通常为去掉可能的 0 或无穷远点后的全平面。",
        "右边序列：ROC 为某圆外区域。",
        "左边序列：ROC 为某圆内区域。",
        "双边序列：ROC 为圆环区域。",
    ])

    doc.h3("常见序列的 z 变换")
    table_rows = [(seq, zform, roc) for seq, zform, roc in common_rows]
    draw_formula_table(doc, ["序列", "z 变换", "收敛域"], table_rows, [150, 210, 150], row_h=38)

    doc.h3("例 1  右边序列与左边序列")
    doc.p("分别求下列两个序列的 z 变换及其收敛域：")
    draw_formula(doc, f_example_pair, max_h=28)
    draw_formula_rows(doc, [f_x1, f_x2], max_h=30, gap=8)
    doc.note("易混点", "两个序列得到相同的代数式，但 ROC 不同；ROC 不同，原序列也不同。", compact=True)

    doc.h3("2.1.2 逆 z 变换")
    doc.p("由 X(z) 求原序列 x(n) 称为 z 反变换。常用方法包括留数法、长除法和部分分式展开法。")
    draw_formula(doc, f_z_inv, max_h=32)
    doc.p("部分分式展开时，通常先把表达式除以 z 后展开成若干标准极点项，再根据 ROC 判断每一项对应右边序列还是左边序列。")
    draw_formula(doc, f_inv_general, max_h=34)
    doc.h3("例 2  根据 ROC 求原序列")
    doc.p("已知下式，当收敛域分别为下列三种情况时求 f(n)。")
    draw_formula(doc, f_pf_question, max_h=26)
    draw_formula(doc, f_pf_rocs, max_h=22)
    draw_formula_rows(doc, [f_pf, f_pf2], max_h=35, gap=8)
    draw_formula_rows(doc, [f_roc1, f_roc2, f_roc3], max_h=30, gap=8)
    doc.note("814 考点提示", "逆 z 变换题目若给多个 ROC，要分别判断每个极点项是右边序列还是左边序列。", compact=True)

    doc.h3("2.1.3 z 变换的基本性质")
    doc.p("本节性质在计算 z 变换、逆 z 变换和系统函数时反复使用。原 PPT 中强调：性质不仅要写变换式，还要同时关注收敛域。")
    draw_property(doc, "(1) 线性", [f_linear_given, f_linear], max_h=25)
    doc.p("相加后序列的 z 变换收敛域一般为两个收敛域的重叠部分，即")
    draw_formula(doc, f_linear_roc, max_h=24)
    doc.p("如果这些线性组合中某些零点和极点互相抵消，则收敛域可能回扩大，而不是缩小。")
    doc.h3("例 3  线性组合导致 ROC 扩大")
    doc.p("求下列序列的 z 变换。")
    draw_formula(doc, f_linear_ex_question, max_h=24)
    draw_formula(doc, f_linear_ex, max_h=30)
    doc.p("可以看出，线性叠加后序列的 z 变换收敛域可能扩大：由下式扩展到全 z 平面。")
    draw_formula(doc, f_linear_ex_roc, max_h=22)

    draw_property(doc, "(2) 时移特性（双边单边大不同）", f_shift_given, max_h=23)
    doc.p("1. 双边 z 变换：若序列的 z 变换如上式，则右移或左移的双边 z 变换为")
    draw_formula(doc, f_shift, max_h=27)
    draw_red_text(doc, "在这种情况下，序列位移不会使 z 变换收敛域发生变换。")
    doc.p("2. 单边 z 变换：若 x(n) 是双边序列，其单边 z 变换为")
    draw_formula(doc, f_unilateral_base, max_h=23)
    doc.p("右移后的单边 z 变换等于")
    draw_formula(doc, f_shift_right, max_h=32)
    draw_formula(doc, f_shift_left, max_h=32)
    doc.h3("例 4  单边 z 变换求系统响应")
    doc.p("已知差分方程表达式如下，边界条件为 y(-1)=0，用 z 变换求系统响应 y(n)。")
    draw_formula(doc, f_diff_eq_q, max_h=26)
    doc.p("对方程两端取 z 变换：")
    draw_formula_rows(doc, [f_diff_eq_z1, f_diff_eq_z2], max_h=30, gap=8)
    doc.p("求逆变换，先作部分分式展开：")
    draw_formula_rows(doc, [f_diff_eq_pf, f_diff_eq_yz, f_diff_eq_yn], max_h=31, gap=8)

    draw_property(doc, "(3) z 域尺度变换（序列指数加权）", [f_scale, f_scale_inv], max_h=28)
    doc.ensure(88)
    doc.p("例如，对于下列单边 z 变换，可由尺度变换直接令 z 变为 -z 得到。")
    draw_formula(doc, f_scale_unilateral_ex, max_h=22)
    doc.h3("例 5  指数加权余弦序列的 z 变换")
    doc.p("已知左式，求右式对应序列的 z 变换。")
    draw_formula(doc, f_scale_cos_question, max_h=24)
    draw_formula_rows(doc, [f_scale_cos_known, f_scale_cos_beta], max_h=34, gap=8)

    draw_property(doc, "(4) z 域微分", [f_mul_n, f_mul_nm], max_h=28)
    doc.p("例：已知单位阶跃序列的 z 变换，求斜边序列的 z 变换。")
    draw_formula(doc, f_mul_nu_question, max_h=24)
    draw_formula(doc, f_mul_nu, max_h=32)

    draw_property(doc, "(5) 初值定理", f_initial, max_h=24)
    doc.p("该定理通常要求 x(n) 为因果序列，并已知其 z 变换。")
    draw_property(doc, "(6) 终值定理", f_final, max_h=24)
    doc.p("终值定理要求 X(z) 在单位圆上只能有一个一阶极点，其他极点均在单位圆内。")
    draw_red_text(doc, "终值定理使用前必须检查极点位置。")
    draw_property(doc, "(7) 时域卷积定理", f_conv_z_full, max_h=28)
    doc.p("卷积后收敛域是 X(z) 与 H(z) 收敛域的重叠部分；若位于某一 z 变换收敛域的极点被另一 z 变换的零点抵消，则收敛域会扩大。")
    doc.h3("例 6  卷积中的零极点抵消")
    doc.p("求下列两序列的卷积。")
    draw_formula(doc, f_conv_ex_question, max_h=25)
    draw_formula(doc, f_conv_ex, max_h=34)
    doc.p("显然 X(z) 的极点 z=1 被 H(z) 的零点抵消，因此 Y(z) 的收敛域会比重叠部分大，为")
    draw_formula(doc, f_conv_ex_roc, max_h=22)

    doc.h2("2.2 离散时间傅里叶变换 DTFT")
    doc.h3("2.2.1 定义与收敛域")
    doc.p("当 z 取单位圆时，z 变换变为 DTFT。DTFT 存在的充分条件通常是序列绝对可和。")
    draw_formula(doc, formula_png("b079_z_unit", r"z=e^{j\omega}", 16), max_h=24)
    draw_dtft_mapping(doc)
    draw_formula(doc, f_dtft_def, max_h=36)
    draw_formula(doc, f_dtft_inv, max_h=32)
    doc.bullet([
        "DTFT 是频率变量 ω 的连续函数。",
        "频谱关于 ω 以 2π 为周期。",
        "若 z 变换 ROC 包含单位圆，则可由 z 变换在单位圆上取值得到 DTFT。",
    ])
    draw_formula(doc, f_dtft_period, max_h=28)

    doc.h3("2.2.2 DTFT 性质")
    doc.p("若序列的 DTFT 记为")
    draw_formula(doc, f_dtft_assume, max_h=24)
    doc.p("则常用性质如下。性质名称要和公式一起记，做题时先判断属于哪一类变换。")
    draw_property(doc, "(1) 线性", f_dtft_lin_full, max_h=25)
    draw_property(doc, "(2) 序列位移", f_dtft_shift, max_h=25)
    draw_property(doc, "(3) 频域位移", f_dtft_mod, max_h=25)
    draw_property(doc, "(4) 序列的线性加权", f_dtft_nx, max_h=26)
    draw_property(doc, "(5) 序列反褶", f_dtft_rev, max_h=25)
    draw_property(doc, "(6) 共轭对称性", f_dtft_conj_def, max_h=25)
    doc.p("满足左式的序列称为共轭对称序列；满足右式的序列称为共轭反对称序列。")
    draw_formula(doc, f_dtft_conj_expand, max_h=30)
    draw_red_text(doc, "共轭对称序列：实部是偶函数，虚部是奇函数。\n共轭反对称序列：实部是奇函数，虚部是偶函数。")
    doc.p("x(n) 的共轭（反）对称分量分别表示为：")
    draw_formula(doc, f_conj_parts, max_h=30)
    doc.p("x(n) 的实（虚）部和共轭（反）对称分量的傅里叶变换为：")
    draw_formula_rows(doc, [f_dtft_real_imag, f_dtft_conj_parts], max_h=30, gap=8)
    doc.h3("例 7  共轭对称性应用")
    doc.p("设 h(n) 为实因果序列，且满足下式，求 h(n) 及其频谱。")
    draw_formula(doc, f_dtft_ex_question, max_h=24)
    draw_formula_rows(doc, [f_dtft_ex_hr, f_dtft_ex_he], max_h=30, gap=8)
    doc.p("由 h(n) 为因果序列和实序列可知：")
    draw_formula(doc, f_dtft_ex_conditions, max_h=28)
    doc.p("结合 he(n) 与 ho(n) 的图形关系，可得")
    draw_dtft_conj_example_plots(doc)
    draw_formula(doc, f_dtft_ex_result, max_h=30)
    draw_property(doc, "(7) 时域卷积", f_dtft_time_conv, max_h=25)
    draw_property(doc, "(8) 频域卷积", f_dtft_freq_conv, max_h=30)
    draw_property(doc, "(9) 帕塞瓦尔定理", f_dtft_parseval, max_h=38)
    doc.note("814 考点提示", "DTFT 性质常和序列平移、调制、反褶及共轭对称结合考。遇到 n x(n) 时优先想到频域微分；遇到实序列、偶奇性时优先检查共轭对称关系。", compact=True)
    append_chapter_review(doc)

    doc.save()
    NOTE_PATH.write_text(
        """# DSP讲义重制_第三批_原PPT46-88页_z变换DTFT_校对记录

## 范围

- 原 PPT 页码：46-88
- 输出：`outputs/DSP讲义重制_第三批_原PPT46-88页_z变换DTFT_初稿.pdf`

## 处理说明

- 本批覆盖第二章开头、z 变换定义与收敛域、典型序列表、逆 z 变换、z 变换性质、DTFT 定义和 DTFT 性质。
- 源 PDF 的文字层为空，本批依据渲染页图人工重排，后续仍需逐页复核细节公式。
- 公式统一按 STIX/衬线数学字体渲染；所有除法以分数形式呈现。
- 去除原 PPT 水印和装饰背景，保留核心公式、例题和考点提示。
""",
        encoding="utf-8",
    )
    print(PDF_PATH)


if __name__ == "__main__":
    build_pdf()
