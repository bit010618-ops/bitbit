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
    TEXT,
    formula_png,
    piecewise_png,
    register_fonts,
    wrap,
)
from make_dsp_batch_016_024 import BatchDoc, draw_formula
from make_dsp_batch_046_088 import draw_red_text
from make_dsp_batch_089_112 import draw_formula_left


PDF_PATH = OUT_DIR / "DSP讲义重制_第六批_原PPT141-184页_DFS_DFT与变换关系_内容版.pdf"
NOTE_PATH = OUT_DIR / "DSP讲义重制_第六批_原PPT141-184页_DFS_DFT与变换关系_校对记录.md"


def f(name, expr, size=14, color="#111111"):
    return formula_png(f"b141_{name}", expr, size, color=color)


def img_size(path):
    im = Image.open(path)
    return im.size


def draw_formula_center(doc, path, max_w=None, max_h=34, gap=10):
    draw_formula(doc, path, max_w=max_w, max_h=max_h, gap=gap)


def draw_formula_row(doc, paths, weights=None, max_h=28, gap=10):
    weights = weights or [1] * len(paths)
    total_weight = sum(weights)
    widths = [CONTENT_W * w / total_weight for w in weights]
    doc.ensure(max_h + gap)
    c = doc.c
    x = MARGIN_X
    y_min = doc.y
    for path, box_w in zip(paths, widths):
        iw, ih = img_size(path)
        scale = min((box_w - 10) / iw, max_h / ih)
        dw, dh = iw * scale, ih * scale
        c.drawImage(ImageReader(str(path)), x + (box_w - dw) / 2, doc.y - dh, dw, dh, mask="auto")
        y_min = min(y_min, doc.y - dh)
        x += box_w
    doc.y = y_min - gap


def draw_label_formula(doc, label, path, max_h=28, gap=8):
    doc.ensure(max_h + 20)
    c = doc.c
    c.setFont("CNB", 9.8)
    c.setFillColor(BLUE_DARK)
    c.drawString(MARGIN_X, doc.y - 16, label)
    iw, ih = img_size(path)
    scale = min((CONTENT_W - 108) / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    x = MARGIN_X + 105
    c.drawImage(ImageReader(str(path)), x, doc.y - dh - 2, dw, dh, mask="auto")
    doc.y -= max(max_h, dh + 4) + gap
    c.setFillColor(TEXT)


def draw_small_tag(doc, text, red=False):
    doc.ensure(22)
    c = doc.c
    c.setFillColor(colors.HexColor("#D71920") if red else BLUE_DARK)
    c.setFont("CNB", 10)
    c.drawString(MARGIN_X, doc.y - 14, text)
    doc.y -= 22
    c.setFillColor(TEXT)


def draw_section_box(doc, title, lines, red_title=False):
    line_count = 0
    wrapped = []
    for line in lines:
        ws = wrap(line, CONTENT_W - 24, "CN", 9.1)
        wrapped.append(ws)
        line_count += len(ws)
    h = 30 + line_count * 14 + 10
    doc.ensure(h + 10)
    c = doc.c
    x = MARGIN_X
    y = doc.y - h
    c.setStrokeColor(colors.HexColor("#A5D4FF"))
    c.setFillColor(colors.HexColor("#F3FAFF"))
    c.roundRect(x, y, CONTENT_W, h, 4, stroke=1, fill=1)
    c.setFont("CNB", 9.8)
    c.setFillColor(colors.HexColor("#D71920") if red_title else BLUE_DARK)
    c.drawString(x + 12, y + h - 20, title)
    c.setFont("CN", 9.1)
    c.setFillColor(TEXT)
    yy = y + h - 39
    for ws in wrapped:
        for line in ws:
            c.drawString(x + 12, yy, line)
            yy -= 14
    doc.y = y - 12


def draw_formula_list(doc, items, max_h=30):
    for item in items:
        if len(item) == 3:
            label, path, row_h = item
        else:
            label, path = item
            row_h = max_h
        draw_label_formula(doc, label, path, max_h=row_h)


def _axis(c, x, y, w, h, x_label):
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.line(x, y, x + w, y)
    c.line(x + w, y, x + w - 6, y + 3)
    c.line(x + w, y, x + w - 6, y - 3)
    c.line(x + w * 0.45, y - 4, x + w * 0.45, y + h)
    c.setFillColor(TEXT)
    c.setFont("CN", 7.2)
    c.drawString(x + w + 3, y - 3, x_label)


def draw_time_frequency_cases(doc):
    """Source page 145: four time/frequency periodicity cases."""
    card_gap = 16
    card_w = (CONTENT_W - card_gap) / 2
    card_h = 105
    total_h = card_h * 2 + 16
    doc.ensure(total_h + 8)
    c = doc.c
    top = doc.y
    titles = [
        "(a) 时域周期连续（频域非周期离散）",
        "(b) 时域非周期连续（频域非周期连续）",
        "(c) 时域非周期离散（频域周期连续）",
        "(d) 时域周期离散（频域周期离散）",
    ]
    for index, title in enumerate(titles):
        row, col = divmod(index, 2)
        x = MARGIN_X + col * (card_w + card_gap)
        y = top - row * (card_h + 8) - card_h
        c.setStrokeColor(BLUE)
        c.setLineWidth(1)
        c.rect(x, y, card_w, card_h, stroke=1, fill=0)
        c.setFillColor(TEXT)
        c.setFont("CNB", 7.6)
        c.drawString(x + 6, y + card_h - 14, title)
        left_x, right_x = x + 8, x + card_w / 2 + 5
        base_y = y + 24
        plot_w = card_w / 2 - 18
        _axis(c, left_x, base_y, plot_w, 46, "t" if index < 2 else "n")
        _axis(c, right_x, base_y, plot_w, 46, "f" if index < 2 else "ω")
        c.setFont("CN", 7)
        c.drawString(left_x + 4, y + card_h - 28, "x(t)" if index < 2 else "x(nT_s)")
        c.drawString(right_x + 4, y + card_h - 28, "|X|" if index < 2 else "|X(e^{jω})|")

        if index in (0, 3):
            for shift in (-34, 0, 34):
                cx = left_x + plot_w * 0.45 + shift
                if index == 0:
                    c.line(cx - 17, base_y, cx, base_y + 28)
                    c.line(cx, base_y + 28, cx + 17, base_y)
                else:
                    for j in range(-3, 4):
                        px = cx + j * 5
                        amp = max(3, 26 - abs(j) * 7)
                        c.line(px, base_y, px, base_y + amp)
        else:
            cx = left_x + plot_w * 0.45
            if index == 1:
                c.line(cx - 22, base_y, cx, base_y + 30)
                c.line(cx, base_y + 30, cx + 22, base_y)
            else:
                for j in range(-5, 6):
                    px = cx + j * 6
                    amp = max(2, 28 - abs(j) * 5)
                    c.line(px, base_y, px, base_y + amp)

        if index in (0, 3):
            for j in range(-4, 5):
                px = right_x + plot_w * 0.45 + j * 9
                amp = 34 / (1 + abs(j))
                c.line(px, base_y, px, base_y + amp)
                c.circle(px, base_y + amp, 1.2, stroke=1, fill=1)
        else:
            periods = (-plot_w * 0.42, plot_w * 0.45) if index == 2 else (0,)
            for offset in periods:
                last = None
                for step in range(70):
                    u = (step - 35) / 11
                    val = abs(math.sin(math.pi * u) / (math.pi * u)) if abs(u) > 1e-6 else 1
                    px = right_x + plot_w * 0.45 + offset + step - 35
                    py = base_y + 4 + 35 * val
                    if last:
                        c.line(last[0], last[1], px, py)
                    last = (px, py)
    doc.y = top - total_h - 10


def draw_dfs_relation_map(doc):
    """Source page 148: DTFT/DFS relation with time/frequency periodicity."""
    h = 178
    doc.ensure(h + 8)
    c = doc.c
    top = doc.y
    left_x = MARGIN_X + 42
    right_x = MARGIN_X + CONTENT_W - 245
    mid_x = MARGIN_X + CONTENT_W / 2
    row_y = (top - 52, top - 137)

    c.setFont("CNB", 8.4)
    c.setFillColor(colors.HexColor("#7A245C"))
    c.drawString(left_x - 34, row_y[0] + 44, "时域离散")
    c.drawString(left_x - 34, row_y[1] + 44, "时域周期")
    c.drawString(right_x - 15, row_y[0] + 44, "频域周期")
    c.drawString(right_x - 15, row_y[1] + 44, "频域离散")

    for idx, y in enumerate(row_y):
        _axis(c, left_x, y, 145, 42, "n")
        count = 9 if idx == 0 else 15
        for j in range(count):
            px = left_x + 58 + (j - (4 if idx == 0 else 7)) * 9
            amp = max(4, 29 - j * 3) if idx == 0 else 9 + 17 * abs(math.sin(j * math.pi / 7))
            c.setStrokeColor(colors.HexColor("#00A3B4"))
            c.line(px, y, px, y + amp)
            c.circle(px, y + amp, 1.2, stroke=1, fill=1)

        _axis(c, right_x, y, 165, 42, "ω" if idx == 0 else "k")
        if idx == 0:
            last = None
            for step in range(160):
                val = 9 + 22 * (0.55 + 0.45 * math.cos((step - 80) * math.pi / 48)) ** 2
                px, py = right_x + step, y + val
                c.setStrokeColor(colors.blue)
                if last:
                    c.line(last[0], last[1], px, py)
                last = (px, py)
        else:
            for j in range(15):
                px = right_x + 15 + j * 10
                amp = 10 + 20 * (0.55 + 0.45 * math.cos((j - 7) * math.pi / 7)) ** 2
                c.setStrokeColor(colors.magenta)
                c.line(px, y, px, y + amp)
                c.circle(px, y + amp, 1.2, stroke=1, fill=1)

    c.setStrokeColor(colors.red)
    c.setFillColor(colors.red)
    for y, upper, lower in ((row_y[0] + 12, "DTFT", "IDTFT"), (row_y[1] + 12, "DFS", "IDFS")):
        c.line(mid_x - 42, y + 10, mid_x + 42, y + 10)
        c.line(mid_x + 42, y + 10, mid_x + 34, y + 14)
        c.line(mid_x + 42, y + 10, mid_x + 34, y + 6)
        c.line(mid_x + 42, y - 8, mid_x - 42, y - 8)
        c.line(mid_x - 42, y - 8, mid_x - 34, y - 4)
        c.line(mid_x - 42, y - 8, mid_x - 34, y - 12)
        c.setFont("CNB", 8.2)
        c.drawCentredString(mid_x, y + 14, upper)
        c.drawCentredString(mid_x, y - 20, lower)

    c.setStrokeColor(colors.HexColor("#D2A000"))
    c.setFillColor(colors.HexColor("#FFF6C8"))
    c.rect(right_x + 108, row_y[1] + 35, 95, 36, stroke=1, fill=1)
    c.setFillColor(TEXT)
    c.setFont("CN", 7.5)
    c.drawCentredString(right_x + 155, row_y[1] + 57, "一周期采样 N 点")
    c.drawCentredString(right_x + 155, row_y[1] + 44, "ω/2π = k/N")
    doc.y = top - h - 8


def draw_transform_review(doc):
    doc.h2("3 傅里叶变换回顾")
    doc.p("进入 DFS/DFT 前，先把连续时间与离散时间傅里叶表示放在同一页对照。这里保留原 PPT 的三组定义，后续 DFT 的采样关系都从这些式子来。")
    draw_formula_list(
        doc,
        [
            ("傅里叶级数", f("fs1", r"x(t)=\sum_{k=-\infty}^{\infty}a_k e^{jk\Omega_0 t}", 13)),
            ("系数", f("fs2", r"a_k=\frac{1}{T}\int_T x(t)e^{-jk\Omega_0 t}\,dt", 13)),
            ("傅里叶反变换", f("ft1", r"x(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}X(j\Omega)e^{j\Omega t}\,d\Omega", 13)),
            ("傅里叶变换", f("ft2", r"X(j\Omega)=\int_{-\infty}^{\infty}x(t)e^{-j\Omega t}\,dt", 13)),
            ("DTFT 反变换", f("dtft1", r"x(n)=\frac{1}{2\pi}\int_{-\pi}^{\pi}X(e^{j\omega})e^{j\omega n}\,d\omega", 13)),
            ("DTFT", f("dtft2", r"X(e^{j\omega})=\sum_{n=-\infty}^{\infty}x(n)e^{-j\omega n}", 13)),
        ],
        max_h=26,
    )
    draw_section_box(
        doc,
        "时间域与频域的四种对应",
        [
            "时间连续且周期：频域离散、非周期。",
            "时间连续且非周期：频域连续、非周期。",
            "时间离散且非周期：频域连续、周期。",
            "时间离散且周期：频域离散、周期。",
        ],
    )
    draw_time_frequency_cases(doc)


def draw_dfs_section(doc):
    doc.h2("3.1 离散傅里叶级数 DFS")
    doc.p("对周期序列的一周期求和即可得到 DFS。原课件两页分别给出指数形式和旋转因子形式，两种记号都保留。")
    draw_label_formula(doc, "正变换", f("dfs_forward", r"\tilde{X}(k)=DFS[\tilde{x}(n)]=\sum_{n=0}^{N-1}\tilde{x}(n)e^{-j\frac{2\pi}{N}kn},\quad k=0,1,\cdots,N-1", 14.5), max_h=38)
    draw_label_formula(doc, "反变换", f("dfs_inverse", r"\tilde{x}(n)=IDFS[\tilde{X}(k)]=\frac{1}{N}\sum_{k=0}^{N-1}\tilde{X}(k)e^{j\frac{2\pi}{N}kn},\quad n=0,1,\cdots,N-1", 14.5), max_h=40)
    draw_label_formula(doc, "旋转因子", f("dfs_wn", r"W_N=e^{-j\frac{2\pi}{N}}", 15), max_h=24)
    draw_formula_row(
        doc,
        [
            f("dfs_wn_f", r"\tilde{X}(k)=\sum_{n=0}^{N-1}\tilde{x}(n)W_N^{kn}", 14),
            f("dfs_wn_i", r"\tilde{x}(n)=\frac{1}{N}\sum_{k=0}^{N-1}\tilde{X}(k)W_N^{-kn}", 14),
        ],
        max_h=36,
    )
    draw_section_box(
        doc,
        "DTFT 与 DFS 的视觉关系",
        [
            "非周期离散序列 x(n) 的 DTFT 是频域连续且以 2π 为周期的 X(e^{jω})。",
            "把 x(n) 以 N 为周期延拓得到周期序列后，频域只需在一周期内取 N 个等间隔样本；采样关系为 ω/(2π)=k/N。",
            "讲义重排时用结构图保留原页含义：时间域从非周期到周期，频域从连续周期谱到离散 DFS 样本。",
        ],
    )
    draw_dfs_relation_map(doc)
    doc.h2("例 1  求 R_4(n) 周期延拓后的 DFS")
    doc.p("把实序列 x(n)=R_4(n) 以 N=8 周期延拓，求一周期内的 DFS 系数。")
    draw_formula_center(doc, f("dfs_ex_sum", r"\tilde{X}(k)=\sum_{n=0}^{7}R_4(n)W_8^{kn}=\sum_{n=0}^{3}W_8^{kn}=1+W_8^k+W_8^{2k}+W_8^{3k}", 12.5), max_h=32)
    doc.bullet([
        "X(0)=4，X(2)=X(4)=X(6)=0。",
        "X(1)=1-j(√2+1)，X(3)=1-j(√2-1)。",
        "X(5)=1+j(√2-1)，X(7)=1+j(√2+1)。",
    ])
    doc.h2("3.1.2 DFS 性质")
    draw_red_text(doc, "因为 DFS 可由 z 变换解释，故 DFS 许多性质与 z 变换相似。")
    draw_formula_center(doc, f("dfs_z_note", r"z=e^{j\frac{2\pi}{N}k}", 14), max_h=24, gap=8)
    draw_formula_list(
        doc,
        [
            ("线性", f("dfs_prop_lin", r"DFS[a\tilde{x}_1(n)+b\tilde{x}_2(n)]=a\tilde{X}_1(k)+b\tilde{X}_2(k)", 12.2)),
            ("时域移位", f("dfs_prop_tshift", r"DFS[\tilde{x}(n+m)]=W_N^{-mk}\tilde{X}(k)", 12.2)),
            ("频域移位", f("dfs_prop_fshift", r"DFS[W_N^{mn}\tilde{x}(n)]=\tilde{X}(k+m)", 12.2)),
            ("周期卷积和", f("dfs_prop_conv_a", r"\tilde{y}(n)=\sum_{m=0}^{N-1}\tilde{x}_1(m)\tilde{x}_2(n-m)", 15.5), 38),
            ("", f("dfs_prop_conv_b", r"=\sum_{m=0}^{N-1}\tilde{x}_2(m)\tilde{x}_1(n-m)", 15.5), 38),
        ],
        max_h=38,
    )


def draw_dft_definition_examples(doc):
    doc.h2("3.2 离散傅里叶变换 DFT")
    doc.p("DFT 是有限长序列的一段主值序列变换。这里的 k、n 取值范围是原 PPT 红字强调的内容，讲义中保留为重点。")
    draw_label_formula(doc, "正变换", f("dft_f", r"X(k)=DFT[x(n)]_N=\sum_{n=0}^{N-1}x(n)W_N^{kn},\quad k=0,1,\cdots,N-1", 14), max_h=38)
    draw_label_formula(doc, "反变换", f("dft_i", r"x(n)=IDFT[X(k)]_N=\frac{1}{N}\sum_{k=0}^{N-1}X(k)W_N^{-kn},\quad n=0,1,\cdots,N-1", 14), max_h=40)
    doc.h2("例 2  求有限长序列的 N 点 DFT")
    doc.p("N 为偶数，求下列长度为 N 的有限长序列的 N 点 DFT。")
    draw_formula_center(doc, f("dft_ex2_q1", r"x(n)=\delta(n)+\delta(n-n_0),\quad 0\leq n_0\leq N-1", 13), max_h=24)
    draw_formula_center(doc, piecewise_png("b141_even_piece", r"x(n)=", r"1,\ n=0,2,\cdots,N-2", r"0,\ n=1,3,\cdots,N-1", fontsize=15), max_h=40)
    draw_formula_center(doc, f("dft_ex2_direct", r"X(k)=\sum_{n=0}^{N-1}[\delta(n)+\delta(n-n_0)]W_N^{kn}=W_N^{0k}+W_N^{n_0k}=1+W_N^{n_0k}", 12), max_h=30)
    draw_formula_center(doc, f("dft_ex2_z", r"X(z)=1+z^{-n_0},\qquad X(k)=X(z)|_{z=e^{j\frac{2\pi}{N}k}}=1+e^{-j\frac{2\pi}{N}kn_0}", 12), max_h=34)
    draw_formula_center(doc, f("dft_ex2_even", r"X(k)=\sum_{r=0}^{N/2-1}W_N^{2rk}=\frac{1-W_N^{kN}}{1-W_N^{2k}}", 13), max_h=28)
    draw_formula_center(doc, piecewise_png("b141_even_result", r"X(k)=", r"\frac{N}{2},\ k=0,\frac{N}{2}", r"0,\ k\ne0,\frac{N}{2}", fontsize=16), max_h=42)
    doc.h2("例 3  已知 DFT 求反变换")
    draw_formula_row(doc, [f("idft_delta", r"X(k)=\delta(k)", 14), f("idft_rect", r"X(k)=R_N(k)", 14)], max_h=23)
    draw_formula_center(doc, f("idft_delta_sol", r"x(n)=\frac{1}{N}\sum_{k=0}^{N-1}\delta(k)W_N^{-kn}=\frac{1}{N},\quad n\in[0,N-1]\Rightarrow x(n)=\frac{1}{N}R_N(n)", 11.8), max_h=34)
    draw_formula_center(doc, f("idft_rect_sol", r"x(n)=\frac{1}{N}\sum_{k=0}^{N-1}R_N(k)W_N^{-kn}=\frac{1}{N}\frac{1-W_N^{-Nn}}{1-W_N^{-n}}\Rightarrow x(n)=\delta(n)R_N(n)", 11.8), max_h=36)


def draw_circular_shift(doc):
    doc.h2("3.2.2 循环（圆周）移位")
    draw_formula_center(doc, f("circ_def", r"x_m(n)=x((n+m))_N R_N(n)", 15), max_h=24)
    doc.bullet([
        "先作周期延拓，得到以 N 为周期的周期序列。",
        "再在周期序列上进行移位。",
        "最后截取一个主值区间，得到循环移位后的有限长序列。",
    ])
    doc.h2("例 4  循环移位")
    doc.p("已知 x(n)={1,2,3,4}，长度不足 8 点时先补零到 N 点。下列序列中，下划线项表示 n=0。")
    rows = [
        f("circ_r1", r"x((n+2))_8R_8(n)=\{\underline{3},4,0,0,0,0,1,2\}", 12.5),
        f("circ_r2", r"x((n-2))_8R_8(n)=\{\underline{0},0,1,2,3,4,0,0\}", 12.5),
        f("circ_r3", r"x((-n+2))_8R_8(n)=\{\underline{3},2,1,0,0,0,0,4\}", 12.5),
        f("circ_r4", r"x((-n-2))_8R_8(n)=\{\underline{0},0,0,4,3,2,1,0\}", 12.5),
    ]
    for row in rows:
        draw_formula_left(doc, row, max_h=25, gap=8)


def draw_dft_properties(doc):
    doc.h2("3.2.3 DFT 的基本性质")
    draw_formula_list(
        doc,
        [
            ("线性性质", f("dft_lin", r"y(n)=ax_1(n)+bx_2(n)\Rightarrow Y(k)=aX_1(k)+bX_2(k)", 12.5)),
            ("时域移位", f("dft_tshift", r"DFT[x((n+m))_N R_N(n)]=W_N^{-km}X(k)", 12.5)),
            ("频域移位", f("dft_fshift", r"DFT[W_N^{mn}x(n)]=X((k+m))_N R_N(k)", 12.5)),
        ],
        max_h=27,
    )
    draw_red_text(doc, "牢记下面两个等式：")
    draw_formula_center(doc, f("dft_zw_note", r"z=e^{j\omega},\qquad \omega=\frac{2\pi}{N}k", 14), max_h=24, gap=8)
    doc.h2("例 5  频域乘子对应循环移位")
    doc.p("若 X(k) 是序列 x(n) 的 4 点 DFT，且 x(n)={1, 3/4, 1/2, 1/4}，求 y(n)。")
    draw_formula_center(doc, f("ex_freqshift_given", r"Y(k)=W_4^{3k}X(k)", 14), max_h=22, gap=8)
    draw_formula_center(doc, f("ex_freqshift_derive", r"Y(k)=W_4^{3k}X(k)=e^{-j\frac{2\pi}{4}k3}X(k)\Rightarrow y(n)=x((n-3))_4R_4(n)=x((n+1))_4R_4(n)", 11.5), max_h=36)
    draw_formula_center(doc, f("ex_freqshift_ans", r"y(n)=\{\underline{\frac{3}{4}},\frac{1}{2},\frac{1}{4},1\}", 13), max_h=24)
    draw_red_text(doc, "拓展：若频域再乘以二阶旋转因子，则时域对应另一个循环移位结果。")
    draw_formula_center(doc, f("ex_freqshift_extend", r"Y(k)=W_2^k X(k)\Rightarrow y(n)=\{\frac{1}{2},\frac{1}{4},1,\frac{3}{4}\}", 13), max_h=26, gap=8)
    doc.h2("共轭对称")
    draw_formula_list(
        doc,
        [
            ("共轭对称", f("conj_e", r"x_e(n)=x_e^*(-n),\qquad x_e(n)=\frac{x(n)+x^*(-n)}{2}", 12.5)),
            ("共轭反对称", f("conj_o", r"x_o(n)=-x_o^*(-n),\qquad x_o(n)=\frac{x(n)-x^*(-n)}{2}", 12.5)),
            ("圆周共轭对称", f("conj_ep", r"x_{ep}(n)=x_{ep}^*(N-n),\qquad x_{ep}(n)=\frac{x(n)+x^*(N-n)}{2}", 12.2)),
            ("圆周共轭反对称", f("conj_op", r"x_{op}(n)=-x_{op}^*(N-n),\qquad x_{op}(n)=\frac{x(n)-x^*(N-n)}{2}", 12.2)),
        ],
        max_h=28,
    )
    draw_section_box(
        doc,
        "共轭对称对应关系",
        [
            "序列的实部对应频域的圆周共轭对称分量，虚部对应频域的圆周共轭反对称分量。",
            "序列的圆周共轭对称分量对应频域实部，圆周共轭反对称分量对应频域虚部。",
        ],
    )
    draw_red_text(doc, "特别地，若 x(n) 为实序列，则 DFT 结果具有圆周共轭对称性。")
    draw_formula_center(doc, f("real_conj_note", r"X(k)=X^*(N-k),\qquad |X(k)|=|X(N-k)|,\qquad \theta(k)=-\theta(N-k)", 12.8), max_h=26, gap=8)
    doc.h2("例 6  共轭对称求实部对应序列")
    doc.p("已知有限长序列 x(n)={1,2,3,4}，其 6 点 DFT 为 X(k)。序列 y(n) 的 6 点 DFT 为 Y(k)，且 Y(k)=Re[X(k)]，求 y(n)")
    draw_formula_center(doc, f("conj_ex1", r"y(n)=x_{ep}(n)=\frac{x(n)+x^*(N-n)}{2}=\{\underline{1},1,\frac{3}{2},4,\frac{3}{2},1\}", 12), max_h=32)
    draw_formula_center(doc, f("conj_ex2", r"x_e(n)=\frac{x(n)+x^*(-n)}{2}=\{\underline{2},\frac{3}{2},1,1,1,\frac{3}{2},2\},\quad y(n)=x_e((n))_6R_6(n)", 11.2), max_h=34)
    doc.h2("一次 DFT/IDFT 处理两个实序列")
    draw_formula_center(doc, f("two_real_dft", r"y(n)=x_1(n)+jx_2(n),\quad Y(k)=X_1(k)+jX_2(k)", 13), max_h=24)
    draw_formula_row(
        doc,
        [
            f("two_real_x1", r"X_1(k)=\frac{1}{2}[Y(k)+Y^*(N-k)]", 13),
            f("two_real_x2", r"X_2(k)=\frac{1}{2j}[Y(k)-Y^*(N-k)]", 13),
        ],
        max_h=28,
    )
    draw_formula_center(doc, f("two_real_idft", r"Y(k)=X_1(k)+jX_2(k)\Rightarrow y(n)=IDFT[Y(k)]=x_1(n)+jx_2(n)", 12.5), max_h=28)
    doc.p("因此，第一个实序列取 y(n) 的实部，第二个实序列取 y(n) 的虚部。")


def draw_common_pairs_and_relations(doc):
    doc.h2("3.2.4 常用 N 点 DFT 对")
    pairs = [
        f("pair1", r"\delta((n))_N R_N(n)\ \longleftrightarrow\ R_N(k)", 12.5),
        f("pair2", r"\delta((n-m))_N R_N(n)\ \longleftrightarrow\ e^{-j\frac{2\pi}{N}km}R_N(k)", 12.5),
        f("pair3", r"R_N(n)\ \longleftrightarrow\ N\delta((k))_N R_N(k)", 12.5),
        f("pair4", r"e^{j\frac{2\pi}{N}nm}R_N(n)\ \longleftrightarrow\ N\delta((k-m))_N R_N(k)", 12.5),
    ]
    for path in pairs:
        draw_formula_left(doc, path, max_h=24, gap=8)
    draw_red_text(doc, "助记：第三个式子时域为直流，说明频域上所有能量 N 都集中在 k=0 这条直流谱线上。")
    doc.h2("例 7  由常用变换对求 DFT")
    doc.p("求 x(n)=cos(3πn/5)sin(4πn/5) 的 10 点 DFT。")
    draw_formula_center(doc, f("cos_sin_expand", r"x(n)=\frac{1}{4j}\left(e^{j\frac{2\pi}{10}7n}+e^{j\frac{2\pi}{10}n}-e^{-j\frac{2\pi}{10}n}-e^{-j\frac{2\pi}{10}7n}\right)", 11.5), max_h=34)
    draw_formula_center(doc, f("cos_sin_ans", r"X(k)=\frac{5}{2j}\left[\delta(k-7)+\delta(k-1)-\delta(k-9)-\delta(k-3)\right],\quad k\in[0,9]", 12), max_h=32)
    doc.h2("例 8  已知 8 点 DFT 反求 x(n)")
    draw_formula_center(doc, f("inv8_q", r"X(k)=1+2\sin(\frac{\pi k}{4})+3\cos(\frac{\pi k}{2})+4\sin(\frac{3\pi k}{4})", 13), max_h=28)
    draw_formula_center(doc, f("inv8_expand", r"X(k)=1-j[e^{j\frac{2\pi k}{8}}-e^{-j\frac{2\pi k}{8}}]+1.5[e^{j\frac{4\pi k}{8}}+e^{-j\frac{4\pi k}{8}}]-2j[e^{j\frac{6\pi k}{8}}-e^{-j\frac{6\pi k}{8}}]", 10.8), max_h=34)
    draw_formula_center(doc, f("inv8_ans", r"x(n)=[\underline{1},j,1.5,2j,0,-2j,1.5,-j]", 13), max_h=24)
    doc.h2("3.3 各种变换的关系")
    draw_red_text(doc, "DFS 和 DFT 的关系：DFT 由 DFS 导出。")
    doc.bullet([
        "对 x(n), 0<=n<=M-1，做 N 点 DFT(N>=M)。先作 N 点周期延拓得到周期序列，再在任意 N 周期内做 DFS，可得到与 DFT 主值相同的结果。",
        "DFT 的处理可理解为先周期延拓，再做对应处理。",
        "DFT 运算相当于周期延拓后取一个主值区间进行 DFS 运算，只是 k 有范围限制。",
    ])
    draw_red_text(doc, "DFT 和 DTFT、Z 变换的关系")
    draw_formula_list(
        doc,
        [
            ("DFT", f("rel_dft", r"X(k)=\sum_{n=0}^{N-1}x(n)e^{-j\frac{2\pi}{N}kn}", 17)),
            ("DTFT", f("rel_dtft", r"X(e^{j\omega})=\sum_{n=0}^{N-1}x(n)e^{-j\omega n}", 17)),
            ("Z 变换", f("rel_z", r"X(z)=\sum_{n=0}^{N-1}x(n)z^{-n}", 17)),
        ],
        max_h=40,
    )
    draw_formula_center(doc, f("rel_sample", r"X(k)=X(e^{j\omega})|_{\omega=\frac{2\pi k}{N}}=X(z)|_{z=e^{j\frac{2\pi k}{N}}}", 14), max_h=34)
    doc.p("序列的 DFT 是 DTFT 从 0 到 2π 以 2π/N 为间隔的等间隔采样，也是 z 变换单位圆上的 N 个抽样值。")
    doc.h2("例 9  R_5(n) 的 DTFT 与 DFT 采样")
    draw_formula_center(doc, f("r5_dtft", r"X(e^{j\omega})=\sum_{n=0}^{4}e^{-j\omega n}=\frac{1-e^{-j5\omega}}{1-e^{-j\omega}}=e^{-j2\omega}\frac{\sin(5\omega/2)}{\sin(\omega/2)}", 11.5), max_h=36)
    draw_formula_center(doc, piecewise_png("b141_r5_n5", r"X_5(k)=", r"5,\ k=0", r"0,\ k=1,2,3,4", fontsize=16), max_h=42)
    draw_formula_center(doc, f("r5_n10", r"X_{10}(k)=e^{-j\frac{2\pi k}{5}}\frac{\sin(\pi k/2)}{\sin(\pi k/10)},\quad 0\leq k\leq 9", 13), max_h=28)


def draw_end_pages(doc):
    doc.h2("本段知识地图")
    draw_section_box(
        doc,
        "离散傅里叶变换",
        [
            "DFS：定义、性质；严谨理解是对离散周期序列的一周期表示。",
            "DFT：定义、线性、循环移位、圆周共轭对称、常用变换对；DFT 是 DFS 取主值区间得到的主值序列。",
            "各种变换关系：根据自定义式的不同记忆，核心是 DFT 等间隔采样 DTFT，也等价于 z 变换单位圆采样。",
        ],
    )
    doc.h2("课后习题")
    doc.bullet([
        "3-1 求序列 DFT。",
        "3-2 求 X(k)。其中修改(2)为下列分段式。",
    ])
    draw_formula_center(doc, piecewise_png("b141_hw_piece", r"X(k)=", r"-\frac{N}{2}je^{j\theta},\ k=m", r"\frac{N}{2}je^{-j\theta},\ k=N-m", fontsize=15), max_h=42)
    doc.bullet([
        "其余 k 时 X(k)=0。",
        "3-15 实序列的 DFT 及 DFT 的性质。",
        "3-16 利用 DFT 的性质求 DFT。",
        "3-23 DFT 和 DTFT 的关系。",
    ])


def build():
    register_fonts()
    doc = BatchDoc(PDF_PATH)
    doc.section = "3. 离散傅里叶变换"
    doc.start()
    doc.h1("第三章 离散傅里叶变换")
    doc.h2("本章内容")
    doc.bullet([
        "离散傅里叶级数 DFS。",
        "离散傅里叶变换 DFT。",
        "各种变换的关系、频率采样、用 DFT 进行线性卷积、用 DFT 进行频谱分析。",
    ])
    draw_transform_review(doc)
    draw_dfs_section(doc)
    draw_dft_definition_examples(doc)
    draw_circular_shift(doc)
    draw_dft_properties(doc)
    draw_common_pairs_and_relations(doc)
    draw_end_pages(doc)
    doc.save()

    NOTE_PATH.write_text(
        "\n".join(
            [
                "# 第六批校对记录",
                "",
                "- 范围：原 PPT 141-184 页。",
                "- 已保留：第三章目录、FS/FT/DTFT 回顾、DFS/DFT 定义、性质名称、红色重点、例题步骤、常用变换对、DFT/DTFT/Z 变换关系、课后习题。",
                "- 排版规则：课后题只放在所属章节末尾，不放在下一章章前。",
                "- 去除：PPT 水印、装饰网络背景、重复页眉装饰。",
                "- 公式处理：所有主要公式均通过数学渲染生成，不保留源代码式文本；比值使用分数形式。",
                "- 待渲染抽检：共轭对称页、常用 DFT 对例题页、R_5(n) 采样关系页。",
            ]
        ),
        encoding="utf-8",
    )
    print(PDF_PATH)


if __name__ == "__main__":
    build()





