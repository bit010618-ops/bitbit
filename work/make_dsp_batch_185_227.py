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
    PAGE_H,
    PAGE_W,
    TEXT,
    discrete_axis_label_geometry,
    draw_auto_math_block,
    draw_auto_math_text,
    formula_png,
    normalize_display_formula_height,
    register_fonts,
    wrap,
)
from make_dsp_batch_016_024 import BatchDoc, draw_formula
from make_dsp_batch_046_088 import draw_red_text


PDF_PATH = OUT_DIR / "DSP讲义重制_第七批_原PPT185-227页_频率采样卷积与谱分析_内容版.pdf"
NOTE_PATH = OUT_DIR / "DSP讲义重制_第七批_原PPT185-227页_频率采样卷积与谱分析_校对记录.md"


def f(name, expr, size=14, color="#111111"):
    return formula_png(f"b185_{name}", expr, size, color=color)


def img_size(path):
    im = Image.open(path)
    return im.size


def draw_formula_center(doc, path, max_w=None, max_h=34, gap=10):
    draw_formula(doc, path, max_w=max_w, max_h=max_h, gap=gap)


def draw_label_formula(doc, label, path, max_h=30, gap=9):
    max_h = normalize_display_formula_height(max_h)
    doc.ensure(max_h + 20)
    c = doc.c
    c.setFont("CNB", 9.8)
    c.setFillColor(BLUE_DARK)
    c.drawString(MARGIN_X, doc.y - 16, label)
    iw, ih = img_size(path)
    scale = min((CONTENT_W - 112) / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(path)), MARGIN_X + 110, doc.y - dh - 2, dw, dh, mask="auto")
    doc.y -= max(max_h, dh + 4) + gap
    c.setFillColor(TEXT)


def draw_formula_list(doc, items, max_h=31):
    for item in items:
        if len(item) == 3:
            label, path, row_h = item
        else:
            label, path = item
            row_h = max_h
        draw_label_formula(doc, label, path, max_h=row_h)


def draw_blue_note(doc, title, lines, red_title=False):
    wrapped = []
    total = 0
    for line in lines:
        ws = wrap(line, CONTENT_W - 24, "CN", 9.1)
        wrapped.append(ws)
        total += len(ws)
    h = 30 + 14 * total + 10
    doc.ensure(h + 10)
    c = doc.c
    y = doc.y - h
    c.setStrokeColor(colors.HexColor("#A5D4FF"))
    c.setFillColor(colors.HexColor("#F3FAFF"))
    c.roundRect(MARGIN_X, y, CONTENT_W, h, 4, stroke=1, fill=1)
    title_color = colors.HexColor("#D71920") if red_title else BLUE_DARK
    draw_auto_math_text(
        c, MARGIN_X + 12, y + h - 20, title,
        font="CNB", size=9.8, color=title_color,
    )
    yy = y + h - 39
    for ws in wrapped:
        for line in ws:
            draw_auto_math_block(
                c, MARGIN_X + 12, yy + 9.1, line, CONTENT_W - 24,
                font="CN", size=9.1, leading=14, color=TEXT,
            )
            yy -= 14
    doc.y = y - 12


def draw_two_col(doc, left_title, left_lines, right_title, right_lines):
    col_gap = 18
    col_w = (CONTENT_W - col_gap) / 2
    def measure(lines):
        return sum(len(wrap(line, col_w - 18, "CN", 8.8)) for line in lines)
    h = 30 + max(measure(left_lines), measure(right_lines)) * 13 + 12
    doc.ensure(h + 12)
    c = doc.c
    for x, title, lines in [
        (MARGIN_X, left_title, left_lines),
        (MARGIN_X + col_w + col_gap, right_title, right_lines),
    ]:
        y = doc.y - h
        c.setStrokeColor(colors.HexColor("#D8E8F6"))
        c.setFillColor(colors.HexColor("#F8FBFE"))
        c.roundRect(x, y, col_w, h, 4, stroke=1, fill=1)
        draw_auto_math_text(
            c, x + 10, y + h - 19, title,
            font="CNB", size=9.8, color=BLUE_DARK,
        )
        yy = y + h - 38
        for line in lines:
            for part in wrap(line, col_w - 18, "CN", 8.8):
                draw_auto_math_block(
                    c, x + 10, yy + 8.8, part, col_w - 18,
                    font="CN", size=8.8, leading=13, color=TEXT,
                )
                yy -= 13
    doc.y -= h + 12


def draw_pipeline(doc, labels):
    doc.ensure(70)
    c = doc.c
    w, h, gap = 76, 32, 19
    x = MARGIN_X + 12
    y = doc.y - 50
    for i, label in enumerate(labels):
        c.setStrokeColor(BLUE)
        c.setLineWidth(1.2)
        c.setFillColor(colors.white)
        c.roundRect(x, y, w, h, 4, stroke=1, fill=1)
        draw_auto_math_text(
            c, x + w / 2, y + 11, label,
            font="CNB", size=8.8, color=BLUE_DARK, align="center",
        )
        if i < len(labels) - 1:
            x2 = x + w
            c.setStrokeColor(BLUE)
            c.line(x2 + 3, y + h / 2, x2 + gap - 4, y + h / 2)
            c.line(x2 + gap - 4, y + h / 2, x2 + gap - 10, y + h / 2 + 4)
            c.line(x2 + gap - 4, y + h / 2, x2 + gap - 10, y + h / 2 - 4)
        x += w + gap
    doc.y -= 72
    c.setFillColor(TEXT)


def stem_plot_axis_geometry():
    return {"vertical_arrow_headroom": 12.0}


def draw_stem_plot(
    doc,
    title,
    samples,
    n_min,
    n_max,
    y_max=None,
    width=250,
    height=130,
    x_label="n",
    x_tick_labels=None,
    sample_value_labels=None,
    title_position="below",
):
    y_max = y_max or max(abs(v) for v in samples.values())
    doc.ensure(height + 28)
    c = doc.c
    x0 = MARGIN_X + (CONTENT_W - width) / 2
    y0 = doc.y - height + 20
    mid = y0 + 36
    left = x0 + 24
    right = x0 + width - 24
    top = y0 + height - 25
    bottom = y0 + 16
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.9)
    c.line(left, mid, right, mid)
    c.line(right, mid, right - 6, mid + 4)
    c.line(right, mid, right - 6, mid - 4)
    zero_x = left + (0 - n_min) / (n_max - n_min) * (right - left)
    c.line(zero_x, bottom, zero_x, top)
    c.line(zero_x, top, zero_x - 3, top - 6)
    c.line(zero_x, top, zero_x + 3, top - 6)
    c.setFont("CN", 7.6)
    c.drawString(right + 4, mid - 2, x_label)
    label_geometry = discrete_axis_label_geometry()
    for n in range(n_min, n_max + 1):
        x = left + (n - n_min) / (n_max - n_min) * (right - left)
        c.line(x, mid - 3, x, mid + 3)
        should_label = n == 0 or (x_tick_labels is not None and n in x_tick_labels) or (
            x_tick_labels is None and (n in samples or n in (-1, 1, n_max))
        )
        if should_label:
            if n == 0:
                offset = label_geometry["origin_tick"]
                c.drawRightString(x + offset["x_offset"], mid + offset["y_offset"], "0")
            elif x_tick_labels is not None and n in x_tick_labels:
                tick_path = formula_png(f"b185_x_tick_{n - n_min}", x_tick_labels[n], 11)
                tick_w, tick_h = img_size(tick_path)
                tick_scale = min(45 / tick_w, 14 / tick_h)
                draw_w, draw_h = tick_w * tick_scale, tick_h * tick_scale
                c.drawImage(
                    ImageReader(str(tick_path)),
                    x - draw_w / 2,
                    mid - 20,
                    draw_w,
                    draw_h,
                    mask="auto",
                )
            else:
                offset = label_geometry["regular_tick"]
                c.drawCentredString(x + offset["x_offset"], mid + offset["y_offset"], str(n))
    scale = (
        top - mid - stem_plot_axis_geometry()["vertical_arrow_headroom"]
    ) / max(y_max, 1)
    for n, val in samples.items():
        x = left + (n - n_min) / (n_max - n_min) * (right - left)
        y = mid + val * scale
        c.line(x, mid, x, y)
        c.circle(x, y, 3.0, stroke=1, fill=1)
        if sample_value_labels is not None and n in sample_value_labels:
            value_path = formula_png(f"b185_sample_value_{n - n_min}", sample_value_labels[n], 11)
            value_w, value_h = img_size(value_path)
            value_scale = min(28 / value_w, 14 / value_h)
            draw_w, draw_h = value_w * value_scale, value_h * value_scale
            c.drawImage(
                ImageReader(str(value_path)),
                x - draw_w / 2,
                y + 6,
                draw_w,
                draw_h,
                mask="auto",
            )
        else:
            c.drawCentredString(x, y + 7 if val >= 0 else y - 14, f"{val:g}")
    title_x = zero_x + 24 if title_position == "axis_top" else (left + right) / 2
    title_y = top - 4 if title_position == "axis_top" else y0 + 2
    draw_auto_math_text(
        c, title_x, title_y, title,
        font="CNB", size=8.6, color=TEXT, align="center",
    )
    doc.y -= height + 15


def draw_small_table(doc, headers, rows, col_widths=None, font_size=8.7):
    col_widths = col_widths or [CONTENT_W / len(headers)] * len(headers)
    row_h = 24
    h = row_h * (len(rows) + 1)
    doc.ensure(h + 12)
    c = doc.c
    x0 = MARGIN_X
    y = doc.y - row_h
    c.setStrokeColor(colors.HexColor("#C9DDEC"))
    c.setFillColor(colors.HexColor("#F3F8FC"))
    c.rect(x0, y, CONTENT_W, row_h, stroke=1, fill=1)
    x = x0
    for head, cw in zip(headers, col_widths):
        draw_auto_math_text(
            c, x + cw / 2, y + 8, head,
            font="CNB", size=font_size, color=TEXT, align="center",
        )
        c.line(x, y, x, y - row_h * len(rows))
        x += cw
    c.line(x0 + CONTENT_W, y, x0 + CONTENT_W, y - row_h * len(rows))
    yy = y - row_h
    for row in rows:
        x = x0
        c.setFillColor(colors.white)
        c.rect(x0, yy, CONTENT_W, row_h, stroke=1, fill=0)
        c.setFillColor(TEXT)
        for cell, cw in zip(row, col_widths):
            draw_auto_math_text(
                c, x + cw / 2, yy + 8, cell,
                font="CN", size=font_size, color=TEXT, align="center",
            )
            x += cw
        yy -= row_h
    doc.y -= h + 12


def draw_bullet_list(doc, items, font_size=9.2, gap=5):
    c = doc.c
    for item in items:
        lines = wrap(item, CONTENT_W - 22, "CN", font_size)
        h = len(lines) * 14 + gap
        doc.ensure(h + 4)
        c.setFillColor(BLUE)
        c.circle(MARGIN_X + 5, doc.y - 9, 2.2, stroke=0, fill=1)
        c.setFont("CN", font_size)
        c.setFillColor(TEXT)
        yy = doc.y - 13
        for line in lines:
            c.drawString(MARGIN_X + 18, yy, line)
            yy -= 14
        doc.y -= h


def draw_chapter_map(doc):
    doc.ensure(270)
    c = doc.c
    top = doc.y
    c.setFont("CNB", 13)
    c.setFillColor(BLUE_DARK)
    c.drawCentredString(PAGE_W / 2, top - 10, "第三章知识导图")
    groups = [
        ("DFS 与 DFT 基础", ["DFS 定义、性质", "DFT 定义、性质", "循环移位", "圆周共轭对称", "常用变换对", "各变换关系"]),
        ("频率采样", ["频率采样定理", "频域内插", "时域周期延拓", "无混叠条件"]),
        ("卷积与系统输出", ["循环卷积定义与定理", "线性卷积关系", "DFT 求线性卷积", "重叠相加法", "重叠保留法"]),
        ("频谱分析", ["频谱混叠", "频谱泄露", "截断效应", "栅栏效应", "问题与措施"]),
    ]
    box_w = (CONTENT_W - 24) / 2
    box_h = 100
    for idx, (title, items) in enumerate(groups):
        x = MARGIN_X + (idx % 2) * (box_w + 24)
        y = top - 42 - (idx // 2) * (box_h + 14)
        c.setStrokeColor(colors.HexColor("#BDD9EE"))
        c.setFillColor(colors.HexColor("#F8FBFE"))
        c.roundRect(x, y - box_h, box_w, box_h, 5, stroke=1, fill=1)
        c.setFont("CNB", 10)
        c.setFillColor(BLUE_DARK)
        c.drawString(x + 12, y - 20, title)
        c.setFont("CN", 8.7)
        c.setFillColor(TEXT)
        yy = y - 34
        for it in items:
            c.circle(x + 14, yy + 3, 1.8, stroke=0, fill=1)
            c.drawString(x + 23, yy, it)
            yy -= 12
    doc.y = top - 270
    c.setFillColor(TEXT)


def draw_frequency_summary(doc):
    draw_two_col(
        doc,
        "三类误差",
        [
            "时域抽样 -> 频域混叠：抽样频率不足导致频谱重叠。",
            "时域截断 -> 频谱泄露：窗谱主瓣展宽并带来旁瓣干扰。",
            "频域抽样(DFT) -> 栅栏效应：采样点之间的频谱不可见。",
        ],
        "改善方法",
        [
            "混叠：提高抽样率或采样前抗混叠滤波。",
            "截断：选择合适窗函数并增加截断长度。",
            "栅栏：尾部补零可看到更多谱线，但提高分辨率要增加记录长度。",
        ],
    )


def build():
    register_fonts()
    doc = BatchDoc(PDF_PATH)
    doc.section = "3. 离散傅里叶变换"
    doc.header()

    doc.h2("3.4 频率采样定理")
    doc.p("当 z 变换的收敛域包含单位圆时，可以在单位圆上对频谱作等间隔采样。频率采样会在时域产生周期延拓，这是本节的核心。")
    draw_formula_list(
        doc,
        [
            ("频域采样", f("freq_sample", r"X(k)=X(e^{j\omega})|_{\omega=\frac{2\pi}{N}k},\quad k=0,1,\cdots,N-1", 13.5), 34),
            ("周期延拓", f("time_periodic", r"\tilde{x}_N(n)=\sum_{r=-\infty}^{\infty}x(n+rN)", 14.5), 34),
            ("截取主值", f("xN", r"x_N(n)=\tilde{x}_N(n)R_N(n)", 14), 28),
        ],
    )
    draw_blue_note(
        doc,
        "结论",
        [
            "时域采样会产生频域周期延拓；频域采样会产生时域周期延拓。",
            "若原序列有限长 M，采样点数 N>=M 时无时域混叠；N<M 时会产生时域混叠。",
        ],
        red_title=True,
    )
    doc.h2("频域内插")
    doc.p("由 N 个频域样本可以构造频域内插表达式，这一形式常用于频率采样结构的数字滤波器设计。")
    draw_formula_center(
        doc,
        f("interp", r"X(z)=\frac{1}{N}\sum_{k=0}^{N-1}X(k)\frac{1-z^{-N}}{1-W_N^{-k}z^{-1}}", 14.5),
        max_h=38,
    )
    doc.h2("例  频率采样求 IDFT")
    doc.p("设 x(n)=R_6(n)，在单位圆上取 4 个等间隔样本。由于 N=4<M=6，会发生时域混叠，主值序列为：")
    draw_formula_center(doc, f("freq_ex", r"x_4(n)=\{2,2,1,1\}", 15), max_h=28)

    doc.h2("3.5 用 DFT 计算线性卷积")
    doc.p("DFT 可直接计算圆周卷积。系统输出需要线性卷积，因此要先明确线性卷积、圆周卷积和周期延拓之间的关系。")
    draw_formula_list(
        doc,
        [
            ("L 点圆周卷积", f("circ_conv", r"y_c(n)=\left[\sum_{m=0}^{L-1}x_2(m)x_1((n-m))_L\right]R_L(n)", 12.5), 36),
            ("DFT 卷积定理", f("dft_conv", r"DFT[x_1(n)\ast_L x_2(n)] = X_1(k)X_2(k)", 13.5), 30),
            ("无混叠条件", f("no_alias", r"L\geq N_1+N_2-1", 16), 28),
        ],
    )
    draw_pipeline(doc, ["x(n)补零", "L点DFT", "相乘", "L点IDFT", "y(n)"])
    doc.p("当 L 不小于线性卷积长度时，圆周卷积结果等于线性卷积；否则线性卷积会按 L 点周期延拓后在主值区间内叠加。")

    doc.h2("例  求圆周卷积与线性卷积")
    doc.p("设 x_1(n)=R_5(n)，x_2(n)=n+1(0<=n<=2)。线性卷积和不同点数圆周卷积结果如下。")
    draw_small_table(
        doc,
        ["卷积类型", "结果"],
        [
            ["线性卷积", "{1,3,6,6,6,5,3}"],
            ["5 点圆周卷积", "{6,6,6,6,6}"],
            ["6 点圆周卷积", "{4,3,6,6,6,5}"],
            ["7 点圆周卷积", "{1,3,6,6,6,5,3}"],
        ],
        col_widths=[110, CONTENT_W - 110],
    )
    draw_blue_note(doc, "814 考点提示", ["求圆周卷积时，通常先求线性卷积，再按圆周长度折叠叠加。"], red_title=True)

    doc.h2("3.5.3 重叠相加法")
    doc.p("长序列可分段计算。每段先与 h(n) 做线性卷积，再按分段位置平移，最后把重叠区域相加。")
    draw_formula_center(
        doc,
        f("ola", r"h(n)*\sum_i x_i(n-iM)=\sum_i [h(n)*x_i(n)]\delta(n-iM)", 13),
        max_h=32,
    )
    draw_blue_note(
        doc,
        "FFT 实现步骤",
        [
            "1. 将输入分成长度 M 的若干段。",
            "2. 取 L=M+N-1，分别补零后用 DFT/FFT 计算每段线性卷积。",
            "3. 将各段结果按 M 点间隔平移并重叠相加。",
            "若使用 FFT，L 通常取 2 的整数次幂。",
        ],
    )
    doc.h2("例  重叠相加法验证")
    doc.p("x(n)=(n+1)R_8(n)，h(n)=R_3(n)。直接线性卷积和分段验证结果一致。")
    draw_formula_center(doc, f("ola_ex", r"y(n)=\{1,3,6,9,12,15,18,21,15,8\}", 13.5), max_h=28)
    doc.p("若 3000 点序列与 60 点滤波器用 128 点 DFT/IDFT 实现，每段有效输出点数为 128-60+1=69。")
    draw_formula_center(doc, f("ola_count", r"\frac{3000}{69}\approx 43.48\Rightarrow 44,\quad DFT=45,\quad IDFT=44", 13), max_h=30)

    doc.h2("3.5.4 重叠保留法")
    doc.p("重叠保留法每段保留上一段的 N-1 个点，与新输入点一起做圆周卷积；每段结果丢掉前 N-1 点，只保留后 M 点并首尾连接。")
    draw_blue_note(
        doc,
        "计算流程",
        [
            "设 h(n) 长度为 N，每段新输入长度为 M，则循环卷积长度 L0=M+N-1。",
            "第一段前面补 N-1 个 0；后续每段与前段重叠 N-1 点。",
            "每段做 L 点圆周卷积后，舍弃前 N-1 点，保留后 M 点。",
        ],
    )
    doc.h2("例  重叠保留法相同区间")
    doc.p("x(n) 的范围为 0<=n<=7，h(n) 的范围为 0<=n<=19，20 点循环卷积是线性卷积以 20 为周期延拓后的主值序列。")
    doc.p("线性卷积范围为 [0,26]；[0,6] 出现混叠；[7,19] 与线性卷积相同。")
    draw_formula_center(doc, f("ols_same", r"y_L(n):[0,26],\quad [0,6],\quad [7,19]", 13), max_h=28)
    doc.h2("例  重叠保留法段数")
    doc.p("h(n) 长度 M=31，x(n) 长度 N_1=19000，每段 512 点。")
    draw_formula_list(
        doc,
        [
            ("总输出点数", f("ols_count1", r"19000+31-1=19030", 14), 24),
            ("每段有效点", f("ols_count2", r"512-30=482", 14), 24),
            ("段数", f("ols_count3", r"\frac{19030}{482}\approx 39.48\Rightarrow 40", 14), 30),
        ],
    )
    doc.h2("例  重叠保留法验证")
    doc.p("x(n)=(n+1)R_8(n)，h(n)=R_3(n)，每段长度为 6，设 M=4、N=3、L0=M+N-1。")
    draw_formula_center(doc, f("ols_verify", r"y(n)=\{1,3,6,9\mid 12,15,18,21\mid 15,8\}", 13.5), max_h=28)
    doc.p("流程上可用 IDFT 求循环卷积；本题直接算循环卷积更方便验证。")
    doc.h2("例  分段求系统输出")
    doc.p("x(n)=13-n, 0<=n<=12，h(n)={2,-1,1}；将 x(n) 每段分为 7 点，每段重复 2 点。")
    draw_small_table(
        doc,
        ["分段", "序列", "局部结果"],
        [
            ["x0(n)", "{0,0,13,12,11,10,9}", "{1,9,26,11,23,21,19}"],
            ["x1(n)", "{10,9,8,7,6,5,4}", "{21,12,17,15,13,11,9}"],
            ["x2(n)", "{5,4,3,2,1,0,0}", "{10,3,7,5,3,1,1}"],
        ],
        col_widths=[70, 235, CONTENT_W - 305],
        font_size=8.2,
    )
    draw_formula_center(doc, f("ols_y", r"y(n)=\{26,11,23,21,19,17,15,13,11,9,7,5,3,1,1\}", 12), max_h=28)
    doc.h2("例  FIR 滤波分段参数")
    doc.p("FIR 长度 N=50，每段 100 点，做 128 点循环卷积。")
    draw_formula_list(
        doc,
        [
            ("重叠点", f("fir_v", r"V=49", 16), 22),
            ("有效点", f("fir_b", r"B=128-49-28=51", 13.5), 28),
            ("保留区间", f("fir_pick", r"y_m(n):\ n=49\sim 99", 13.5), 28),
        ],
    )

    doc.h2("3.5.5 求解 LTI 系统输出方法小结")
    draw_formula_list(
        doc,
        [
            ("时域直接求解", f("lti_time", r"y_1(n)=h(n)*x(n)=\sum_{m=0}^{N-1}h(m)x(n-m)", 13.5), 34),
            ("频域解析法", f("lti_freq", r"y_1(n)=IDFT[Y(e^{j\omega})]=IDFT[X(e^{j\omega})H(e^{j\omega})]", 12.5), 30),
        ],
    )
    draw_pipeline(doc, ["x(n)补零", "L点DFT", "X(k)H(k)", "L点IDFT", "y(n)"])

    doc.h2("3.6 用 DFT 进行频谱分析")
    doc.p("连续信号需要先抽样成序列；序列过长时需要截断；DFT 只能看到有限个频域样值。这三个过程分别会带来三类误差。")
    draw_frequency_summary(doc)
    doc.h2("3.6.1 频谱混叠")
    doc.p("若采样不满足奈奎斯特定理，频域会发生混叠，离散序列频谱在 π 附近重叠，无法分析出原频谱信息。")
    draw_formula_list(
        doc,
        [
            ("产生条件", f("alias_cond", r"f_s<2f_h", 18), 24),
            ("避免条件", f("alias_fix", r"f_s\geq 2f_h", 18), 24),
            ("预滤波", f("alias_filter", r"f>\frac{f_s}{2}", 15), 26),
        ],
    )
    doc.h2("频率分辨率")
    doc.p("频率分辨率指区分相距最近的两个频率分量的能力。DFT 等间隔取样时，相邻两点的模拟频率差记为 F。")
    doc.p("例：要求谱分辨率不超过 10 Hz，最高频率为 2.5 kHz。")
    draw_formula_list(
        doc,
        [
            ("采样约束", f("res1", r"\frac{f_s}{N}\leq 10,\quad f_s\geq 2f_c=5\mathrm{kHz}", 13.5), 32),
            ("记录时间", f("res2", r"T_p=\frac{N}{f_s}\geq 0.1,\quad T_{p\min}=0.1", 13.5), 32),
            ("采样间隔", f("res3", r"T_{\max}=\frac{1}{2f_c}=\frac{1}{5000},\quad N_{\min}=500", 13.5), 32),
            ("分辨率加倍", f("res4", r"F\leq 5\mathrm{Hz}\Rightarrow T_{p\min}=0.2,\quad N_{\min}=1000", 13.5), 32),
        ],
    )
    draw_red_text(doc, "注意：若使用 FFT，N_min=1024。")

    doc.h2("3.6.2 截断效应")
    doc.p("非时限序列必须截断。截断相当于将 x(n) 乘窗函数 w(n)，得到 y(n)=x(n)w(n)。")
    draw_formula_list(
        doc,
        [
            ("矩形窗", f("win1", r"w(n)=R_N(n),\quad x(n)=\cos(\omega_0 n)", 13.5), 28),
            ("窗频谱", f("win2", r"W(e^{j\omega})=\frac{\sin(\frac{\omega N}{2})}{\sin(\frac{\omega}{2})}e^{-j\frac{N-1}{2}\omega}", 13), 34),
            ("幅度", f("win3", r"|W(e^{j\omega})|=\left|\frac{\sin(\frac{\omega N}{2})}{\sin(\frac{\omega}{2})}\right|", 13.5), 32),
        ],
    )
    draw_stem_plot(
        doc,
        r"X(e^{j\omega})",
        {-1: 3.14, 1: 3.14},
        -2,
        2,
        y_max=3.5,
        width=310,
        height=130,
        x_label="ω",
        x_tick_labels={-1: r"-\omega_0", 1: r"\omega_0"},
        sample_value_labels={-1: r"\pi", 1: r"\pi"},
        title_position="axis_top",
    )
    draw_blue_note(
        doc,
        "截断后的两方面影响",
        [
            "1. 频谱泄露：窗谱主瓣使原谱线展宽，截断长度越长，主瓣越窄，泄露越小；泄露会降低频率分辨率。",
            "2. 谱间干扰：矩形窗旁瓣不小，可能造成强信号旁瓣淹没弱信号主瓣。",
        ],
        red_title=True,
    )
    draw_blue_note(
        doc,
        "应对措施",
        [
            "加大窗宽以减小主瓣宽度和泄露。",
            "使用缓变型窗函数减小旁瓣幅度，例如海明窗。",
        ],
    )

    doc.h2("3.6.3 栅栏效应")
    doc.p("N 点 DFT 是 DTFT 在 [0,2pi] 上的 N 点等间隔采样。采样点之间的频谱不可见，如同从栅栏缝隙中观察频谱，这就是栅栏效应。")
    draw_blue_note(
        doc,
        "应对栅栏效应",
        [
            "在序列尾部补零，可以看到更多谱线，但不能提高频率分辨率。",
            "若采样频率不变，增加采样长度，也就是增加 DFT 点数。",
        ],
        red_title=True,
    )
    doc.h2("814 真题关注")
    draw_bullet_list(doc, [
        "2007：频谱泄露产生的主要原因是什么？可以用什么方法改善？",
        "2016：栅栏效应是什么？简述减小方法。",
        "2019：简述栅栏效应的原因和解决方法。",
        "2020：什么是栅栏效应？",
        "2021：什么是频谱泄露，怎么抑制？",
    ])
    doc.h2("频谱分析综合例题")
    doc.p("利用 DFT 分析连续时间信号会引起三类误差：频谱混叠、截断效应和栅栏现象。")
    draw_frequency_summary(doc)

    doc.h2("第三章小结")
    draw_chapter_map(doc)
    doc.h2("思考题")
    doc.p("已知 x_1(n)={1,1,1}, x_2(n)={1,1,1,0,0,0,1}，计算线性卷积和 7 点圆周卷积，并判断何时二者相等。")
    draw_formula_center(doc, f("think", r"x_1(n)*x_2(n)=\{2,3,3,2,1,0,1\},\quad N\geq 9", 13.5), max_h=28)
    doc.h2("第三章课后习题")
    draw_bullet_list(doc, [
        "3-3 画序列图像并求循环卷积。",
        "3-13 Z 变换单位圆上等间隔采样求 IDFT。",
        "3-14 循环卷积和线性卷积的关系。",
        "3-17 频率采样。",
        "3-18、3-19 谱分析。",
        "3-21 使用 FFT 的重叠保留法。",
        "3-22 证明频域循环卷积定理。",
        "3-24 时域卷积定理。",
        "3-25 循环卷积和线性卷积的关系。",
    ])
    doc.save()

    NOTE_PATH.write_text(
        "第七批校对记录\n"
        "- 覆盖原 PPT 185-227 页，第三章后半：频率采样、DFT 计算线性卷积、重叠相加/重叠保留、频谱分析、第三章小结和课后习题。\n"
        "- 原 PPT 红字重点、真题提示、课后习题均已保留；水印和装饰性封面背景未进入重排讲义。\n"
        "- 原 PPT 214 页频域解析公式写为 IDFT[Y(e^{jw})]，已忠于源内容保留，建议最终人工复核是否应表述为反 DTFT/频域反变换。\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    build()
