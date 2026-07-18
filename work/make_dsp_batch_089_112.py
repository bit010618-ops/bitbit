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
    piecewise_png,
    register_fonts,
    normalize_display_formula_height,
    wrap,
)
from make_dsp_batch_016_024 import BatchDoc, draw_formula
from make_dsp_batch_046_088 import draw_property, draw_red_text


PDF_PATH = OUT_DIR / "DSP讲义重制_第四批_原PPT89-114页_频域分析与系统函数_内容版.pdf"
NOTE_PATH = OUT_DIR / "DSP讲义重制_第四批_原PPT89-114页_频域分析与系统函数_校对记录.md"


def f(name, expr, size=14, color="#111111"):
    return formula_png(f"b089_{name}", expr, size, color=color)


def draw_formula_left(doc, image_path, max_w=None, max_h=28, gap=8, indent=0):
    max_h = normalize_display_formula_height(max_h)
    doc.ensure(max_h + gap)
    c = doc.c
    im = Image.open(image_path)
    iw, ih = im.size
    max_w = max_w or CONTENT_W * 0.9
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    x = MARGIN_X + indent
    y = doc.y - dh
    c.drawImage(ImageReader(str(image_path)), x, y, dw, dh, mask="auto")
    doc.y -= dh + gap


def draw_formula_rows(doc, rows, max_h=28, gap=7, left=False, indent=0):
    for row in rows:
        if left:
            draw_formula_left(doc, row, max_h=max_h, gap=gap, indent=indent)
        else:
            draw_formula(doc, row, max_h=max_h, gap=gap)


def paragraph_red_inline(doc, pre, red, post):
    lines_pre = wrap(pre, CONTENT_W, "CN", 9.6)
    doc.ensure(42)
    c = doc.c
    c.setFont("CN", 9.6)
    c.setFillColor(TEXT)
    for line in lines_pre[:-1]:
        c.drawString(MARGIN_X, doc.y, line)
        doc.y -= 15
    line = lines_pre[-1] if lines_pre else ""
    x = MARGIN_X
    c.drawString(x, doc.y, line)
    x += c.stringWidth(line, "CN", 9.6)
    c.setFont("CNB", 9.6)
    c.setFillColor(colors.HexColor("#D71920"))
    c.drawString(x, doc.y, red)
    x += c.stringWidth(red, "CNB", 9.6)
    c.setFont("CN", 9.6)
    c.setFillColor(TEXT)
    c.drawString(x, doc.y, post)
    doc.y -= 20


def draw_chapter_contents(doc):
    doc.ensure(125)
    c = doc.c
    items = [
        ("01", "Z 变换"),
        ("02", "离散时间傅里叶变换"),
        ("03", "模拟频率与数字频率换算"),
        ("04", "系统函数 H(z)"),
        ("05", "拉氏变换与 Z 变换的比较"),
        ("06", "滤波器的设计"),
    ]
    x0 = MARGIN_X
    y0 = doc.y
    box_w = (CONTENT_W - 24) / 2
    box_h = 28
    for i, (num, text) in enumerate(items):
        col = i % 2
        row = i // 2
        x = x0 + col * (box_w + 24)
        y = y0 - row * 41
        c.setFillColor(BLUE)
        c.roundRect(x, y - box_h, 44, box_h, 3, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("CNB", 11)
        c.drawCentredString(x + 22, y - 18, num)
        c.setStrokeColor(BLUE)
        c.setFillColor(colors.white)
        c.roundRect(x + 44, y - box_h, box_w - 44, box_h, 3, stroke=1, fill=0)
        c.setFillColor(BLUE_DARK)
        c.setFont("CNB", 10.2)
        c.drawString(x + 56, y - 18, text)
    doc.y -= 126


def impulse_spectrum_axis_geometry():
    return {
        "axis_height": 56.0,
        "sample_height": 42.0,
    }


def draw_impulse_spectrum(doc, points, title_path=None, max_x_label=None):
    doc.ensure(105)
    c = doc.c
    x = MARGIN_X + 80
    y = doc.y - 66
    w = CONTENT_W - 160
    left, right = x, x + w
    c.setStrokeColor(colors.black)
    c.setFillColor(colors.black)
    c.setLineWidth(1.0)
    c.line(left, y, right, y)
    c.line(right, y, right - 7, y + 4)
    c.line(right, y, right - 7, y - 4)
    geometry = impulse_spectrum_axis_geometry()
    axis_top = y + geometry["axis_height"]
    c.line(left, y - 18, left, axis_top)
    c.line(left, axis_top, left - 4, axis_top - 8)
    c.line(left, axis_top, left + 4, axis_top - 8)
    axis_title = formula_png("b4_impulse_axis_title", r"X(e^{j\omega})", 10)
    axis_image = Image.open(axis_title)
    axis_scale = min(70 / axis_image.width, 13 / axis_image.height)
    axis_w, axis_h = axis_image.width * axis_scale, axis_image.height * axis_scale
    c.drawImage(
        ImageReader(str(axis_title)),
        left + 5,
        y + 45,
        axis_w,
        axis_h,
        mask="auto",
    )
    c.setFont("CN", 8.5)
    c.drawString(right + 4, y - 3, "ω")
    if title_path:
        im = Image.open(title_path)
        scale = min(120 / im.width, 18 / im.height)
        dw, dh = im.width * scale, im.height * scale
        c.drawImage(ImageReader(str(title_path)), x + (w - dw) / 2, doc.y - 8, dw, dh, mask="auto")
    for pos, label_path, height_label in points:
        px = left + pos * w
        top = y + geometry["sample_height"]
        c.line(px, y, px, top)
        c.circle(px, top, 3.1, stroke=1, fill=1)
        im = Image.open(label_path)
        scale = min(56 / im.width, 15 / im.height)
        dw, dh = im.width * scale, im.height * scale
        c.drawImage(ImageReader(str(label_path)), px - dw / 2, y - 18, dw, dh, mask="auto")
        if height_label:
            c.setFont("CN", 8.5)
            c.drawCentredString(px, top + 7, height_label)
    if max_x_label:
        im = Image.open(max_x_label)
        scale = min(60 / im.width, 14 / im.height)
        dw, dh = im.width * scale, im.height * scale
        c.drawImage(ImageReader(str(max_x_label)), right - dw / 2, y - 18, dw, dh, mask="auto")
    doc.y -= 108


def draw_unit_circle_case(doc, poles, roc_label, caption):
    doc.ensure(116)
    c = doc.c
    x = MARGIN_X + 160
    y = doc.y - 50
    r = 38
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    c.circle(x, y, r, stroke=1, fill=0)
    c.line(x - 70, y, x + 70, y)
    c.line(x + 70, y, x + 64, y + 3)
    c.line(x + 70, y, x + 64, y - 3)
    c.line(x, y - 55, x, y + 55)
    c.line(x, y + 55, x - 3, y + 49)
    c.line(x, y + 55, x + 3, y + 49)
    c.setFont("CN", 8)
    c.drawString(x + 73, y - 3, "Re z")
    c.drawString(x + 4, y + 57, "Im z")
    for px, py, label in poles:
        c.setFont("CNB", 12)
        c.drawCentredString(x + px * r, y + py * r - 4, "×")
        c.setFont("CN", 8.2)
        c.drawString(x + px * r + 5, y + py * r + 5, label)
    c.setFillColor(TEXT)
    c.setFont("CNB", 9.4)
    c.drawString(MARGIN_X + 285, doc.y - 30, caption)
    draw_formula_left(doc, roc_label, max_w=210, max_h=22, gap=6, indent=285)
    doc.y -= 36


def build_pdf():
    register_fonts()

    # Sampling and frequency-domain relation.
    xs_def = f("xs_def", r"x_s(t)=x(t)\delta_T(t)=\sum_{n=-\infty}^{\infty}x(nT)\delta(t-nT)", 14)
    ft_product = f("ft_product", r"FT[f_1(t)f_2(t)]=\frac{1}{2\pi}F_1(\Omega)*F_2(\Omega)", 14)
    x_defs = f("x_defs", r"X(j\Omega)=FT[x(t)],\quad X_s(j\Omega)=FT[x_s(t)],\quad P(j\Omega)=FT[\delta_T(t)]", 13)
    ft_periodic = f("ft_periodic", r"FT[f(t)]=2\pi\sum_{n=-\infty}^{\infty}F_n\delta(\Omega-n\Omega_s)", 13)
    p_spectrum = f("p_spectrum", r"P(j\Omega)=\frac{2\pi}{T}\sum_{k=-\infty}^{\infty}\delta(\Omega-k\Omega_s)", 13)
    xs_spectrum = f("xs_spectrum", r"X_s(j\Omega)=\frac{1}{T}\sum_{k=-\infty}^{\infty}X(j\Omega-jk\Omega_s)", 14, color="#D71920")
    sampling_condition = f("sampling_condition", r"\Omega_s\geq 2\Omega_m", 16, color="#D71920")
    x_discrete = f("x_discrete", r"x(n)=x_a(t)|_{t=nT}=x_a(nT)", 15)
    omega_s = f("omega_s", r"\frac{2\pi}{T}=\Omega_s=2\pi F_s", 15)
    xs_dtft = f("xs_dtft", r"X_s(j\Omega)=\int_{-\infty}^{\infty}x_s(t)e^{-j\Omega t}dt=\sum_{n=-\infty}^{\infty}x_a(nT)e^{-jn\Omega T}", 13)
    xc = f("xc_cos", r"x_c(t)=\cos 100\pi t", 15)
    fs100 = f("fs100", r"f_s=100\mathrm{Hz}\Rightarrow x_c[n]=\cos(\pi n)", 14)
    spec100 = f("spec100", r"X_s(e^{j\omega})=2\pi\delta(\omega-\pi)", 14)
    fs150 = f("fs150", r"f_s=150\mathrm{Hz}\Rightarrow x_c[n]=\cos\left(\frac{2\pi}{3}n\right)", 14)
    spec150 = f("spec150", r"X_s(e^{j\omega})=\pi\delta\left(\omega-\frac{2\pi}{3}\right)+\pi\delta\left(\omega-\frac{4\pi}{3}\right)", 13)

    # System function and difference-equation solution.
    h_def = f("h_def", r"H(z)=\frac{Y(z)}{X(z)}", 18)
    h_impulse = f("h_impulse", r"H(z)=\sum_{n=0}^{\infty}h(n)z^{-n}", 16)
    bilateral_shift = f("bilateral_shift", r"Z[x(n\pm m)]=z^{\pm m}X(z)", 15)
    uni_shift_r = f("uni_shift_r", r"Z[x(n-m)u(n)]=z^{-m}\left[X(z)+\sum_{k=-m}^{-1}x(k)z^{-k}\right]", 13)
    uni_shift_l = f("uni_shift_l", r"Z[x(n+m)u(n)]=z^{m}\left[X(z)-\sum_{k=0}^{m-1}x(k)z^{-k}\right]", 13)
    diff_general = f("diff_general", r"\sum_{k=0}^{N}a_k y(n-k)=\sum_{r=0}^{M}b_r x(n-r)", 14)
    diff_unilateral = f(
        "diff_unilateral",
        r"\sum_{k=0}^{N}a_kz^{-k}\!\left[Y(z)+\sum_{l=-k}^{-1}y(l)z^{-l}\right]=\sum_{r=0}^{M}b_rz^{-r}\!\left[X(z)+\sum_{m=-r}^{-1}x(m)z^{-m}\right]",
        10,
    )
    ex1_q = f("ex1_q", r"y(n)-y(n-1)-2y(n-2)=x(n)+2x(n-2),\quad y(-1)=2,\quad y(-2)=-\frac{1}{2},\quad x(n)=u(n)", 11)
    ex1_z = f("ex1_z", r"Y(z)-z^{-1}[Y(z)+y(-1)z]-2z^{-2}[Y(z)+y(-1)z+y(-2)z^2]=X(z)+2z^{-2}X(z)", 11)
    ex1_decomp = f("ex1_decomp", r"Y(z)=Y_{zi}(z)+Y_{zs}(z)=\frac{(1+2z^{-1})y(-1)+2y(-2)}{1-z^{-1}-2z^{-2}}+\frac{1+2z^{-2}}{1-z^{-1}-2z^{-2}}X(z)", 10)
    ex1_x = f("ex1_x", r"X(z)=\frac{z}{z-1}", 14)
    ex1_yzi_pf = f("ex1_yzi_pf", r"\frac{Y_{zi}(z)}{z}=\frac{z+4}{(z-2)(z+1)}=\frac{2}{z-2}-\frac{1}{z+1}", 13)
    ex1_yzi = f("ex1_yzi", r"y_{zi}(n)=[2\cdot 2^n-(-1)^n]u(n)", 14)
    ex1_yzs_pf = f("ex1_yzs_pf", r"\frac{Y_{zs}(z)}{z}=\frac{z^2+2}{(z-2)(z+1)(z-1)}=\frac{2}{z-2}+\frac{\frac{1}{2}}{z+1}-\frac{\frac{3}{2}}{z-1}", 11)
    ex1_yzs = f("ex1_yzs", r"y_{zs}(n)=\left[2\cdot 2^n+\frac{1}{2}(-1)^n-\frac{3}{2}\right]u(n)", 13)
    ex1_y = f("ex1_y", r"y(n)=\left[4\cdot 2^n-\frac{1}{2}(-1)^n-\frac{3}{2}\right]u(n)", 14)
    ex2_q = f("ex2_q", r"x(n)=\left(-\frac{1}{2}\right)^nu(n),\quad y_{zs}(n)=\left[\frac{3}{2}\left(\frac{1}{2}\right)^n+4\left(-\frac{1}{3}\right)^n-\frac{9}{2}\left(-\frac{1}{2}\right)^n\right]u(n)", 11)
    ex2_hz = f("ex2_hz", r"H(z)=\frac{Y_{zs}(z)}{X(z)}=\frac{z^2+2z}{(z-\frac{1}{2})(z+\frac{1}{3})}", 13)
    ex2_pf = f("ex2_pf", r"\frac{H(z)}{z}=\frac{z+2}{(z-\frac{1}{2})(z+\frac{1}{3})}=\frac{3}{z-\frac{1}{2}}-\frac{2}{z+\frac{1}{3}}", 12)
    ex2_hn = f("ex2_hn", r"h(n)=\left[3\left(\frac{1}{2}\right)^n-2\left(-\frac{1}{3}\right)^n\right]u(n)", 14)
    ex2_diff = f("ex2_diff", r"y(n)-\frac{1}{6}y(n-1)-\frac{1}{6}y(n-2)=x(n)+2x(n-1)", 14)

    # Causality/stability.
    causal_td = f("causal_td", r"h(n)=0,\quad n<0", 15)
    stable_td = f("stable_td", r"\sum_{n=-\infty}^{\infty}|h(n)|\leq M", 15)
    causal_stable_td = f("causal_stable_td", r"h(n)=0,\ n<0,\qquad \sum_{n=0}^{\infty}|h(n)|\leq M", 14)
    ex_u_piece = piecewise_png("b089_ex_u_piece", r"h(n)=u(n)=", r"1,\ n\geq0", r"0,\ n<0", fontsize=16)
    ex_u_sum = f("ex_u_sum", r"\sum_{n=-\infty}^{\infty}|h(n)|=\infty", 15)
    ex_u_hz = f("ex_u_hz", r"H(z)=\frac{z}{z-1},\qquad ROC:|z|>1", 14)
    ex_h2_q = f("ex_h2_q", r"H(z)=\frac{1}{1-\frac{1}{2}z^{-1}}+\frac{1}{1-2z^{-1}}=\frac{z}{z-\frac{1}{2}}+\frac{z}{z-2}", 12)
    ex_h2_case1 = f("ex_h2_case1", r"|z|>2:\quad h(n)=\left[\left(\frac{1}{2}\right)^n+2^n\right]u(n)", 13)
    ex_h2_case2 = f("ex_h2_case2", r"\frac{1}{2}<|z|<2:\quad h(n)=\left(\frac{1}{2}\right)^nu(n)-2^nu(-n-1)", 13)
    ex_h2_case3 = f("ex_h2_case3", r"|z|<\frac{1}{2}:\quad h(n)=-\left[\left(\frac{1}{2}\right)^n+2^n\right]u(-n-1)", 13)
    ex3_q = f("ex3_q", r"y(n)+0.2y(n-1)-0.24y(n-2)=x(n)+x(n-1)", 13)
    ex3_transform = f("ex3_transform", r"Y(z)+0.2z^{-1}Y(z)-0.24z^{-2}Y(z)=X(z)+z^{-1}X(z)", 12)
    ex3_hz = f("ex3_hz", r"H(z)=\frac{Y(z)}{X(z)}=\frac{1+z^{-1}}{1+0.2z^{-1}-0.24z^{-2}}=\frac{z(z+1)}{(z+0.6)(z-0.4)}", 12)
    ex3_poles = f("ex3_poles", r"z_1=-0.6,\qquad z_2=0.4,\qquad ROC:|z|>0.6", 13)
    ex3_pf = f("ex3_pf", r"\frac{H(z)}{z}=\frac{z+1}{(z+0.6)(z-0.4)}=\frac{-0.4}{z+0.6}+\frac{1.4}{z-0.4}", 12)
    ex3_hn = f("ex3_hn", r"h(n)=-0.4(-0.6)^nu(n)+1.4(0.4)^nu(n)", 14)
    freq_resp = f("freq_resp", r"H(e^{j\omega})=\sum_{n=-\infty}^{\infty}h(n)e^{-j\omega n}=H(z)|_{z=e^{j\omega}}", 13)
    freq_polar = f("freq_polar", r"H(e^{j\omega})=|H(e^{j\omega})|e^{j\theta(\omega)}", 14)
    freq_amp = f("freq_amp", r"|H(e^{j\omega})|=\sqrt{R^2+X^2}", 14)
    freq_phase = f("freq_phase", r"\theta(\omega)=\arctan\frac{X}{R}", 14)
    ratio_q = f("ratio_q", r"H(e^{j\omega})=\frac{R_1+jX_1}{R_2+jX_2}", 14)
    ratio_amp = f("ratio_amp", r"|H(e^{j\omega})|=\frac{\sqrt{R_1^2+X_1^2}}{\sqrt{R_2^2+X_2^2}}", 17)
    ratio_phase = f("ratio_phase", r"\theta(\omega)=\arctan\frac{X_1}{R_1}-\arctan\frac{X_2}{R_2}", 14)
    first_order_q = f("first_order_q", r"H(e^{j\omega})=\frac{1}{1-ae^{-j\omega}}", 14)
    first_order_amp = f("first_order_amp", r"|H(e^{j\omega})|=\frac{1}{\sqrt{1+a^2-2a\cos\omega}}", 17)
    first_order_phase = f("first_order_phase", r"\theta(\omega)=-\arctan\frac{a\sin\omega}{1-a\cos\omega}", 14)
    steady_input = f("steady_input", r"x(n)=e^{j\omega_0n}", 14)
    steady_conv = f("steady_conv", r"y(n)=e^{j\omega_0n}H(e^{j\omega_0})", 14)
    steady_output = f("steady_output", r"y(n)=|H(e^{j\omega_0})|e^{j[\omega_0n+\theta(\omega_0)]}", 14)
    steady_sine = f("steady_sine", r"y(n)=A|H(e^{j\omega_0})|\cos[\omega_0n+\varphi+\theta(\omega_0)]", 14, "#D71920")

    pi_label = f("label_pi", r"\pi", 11)
    twopi3_label = f("label_2pi3", r"\frac{2\pi}{3}", 11)
    fourpi3_label = f("label_4pi3", r"\frac{4\pi}{3}", 11)
    twopi_label = f("label_2pi", r"2\pi", 11)

    doc = BatchDoc(PDF_PATH)
    doc.section = "第二章 离散频域分析与Z变换"
    doc.start()

    # Chapter review and homework are carried by the previous batch tail page.

    doc.h2("2.3 模拟频率与数字频率换算")
    doc.h3("2.3.1 理想抽样信号的频谱")
    doc.p("把连续时间信号与周期冲激串相乘，就得到理想抽样信号。源 PPT 的核心是：时域相乘对应频域卷积。")
    draw_formula_rows(doc, [xs_def, ft_product, x_defs], max_h=30)
    doc.p("周期冲激串的傅里叶变换仍为冲激串，因此抽样信号频谱可以看作原模拟频谱在频域的周期延拓。")
    draw_formula_rows(doc, [ft_periodic, p_spectrum, xs_spectrum], max_h=30)
    draw_red_text(doc, "理想抽样信号的频谱是原模拟信号频谱以抽样角频率为周期的延拓。若要避免混叠，必须满足抽样角频率不小于信号最高角频率的两倍。")
    draw_formula(doc, sampling_condition, max_h=28)

    doc.h3("2.3.2 离散时间傅里叶变换与模拟傅里叶变换")
    doc.p("若连续信号按间隔 T 抽样，离散序列与连续时间信号之间满足如下关系。")
    draw_formula_rows(doc, [x_discrete, omega_s, xs_dtft], max_h=34)
    doc.p("上式说明，离散时间频率变量与模拟角频率之间通过抽样周期联系。做题时先把模拟频率换成数字频率，再判断是否发生混叠。")
    doc.h3("例 2  不同抽样频率下的离散频谱")
    draw_formula(doc, xc, max_h=24)
    doc.p("当抽样频率为 100 Hz 时：")
    draw_formula_rows(doc, [fs100, spec100], max_h=25)
    draw_impulse_spectrum(doc, [(0.52, pi_label, "2π")], title_path=f("title_fs100", r"f_s=100\mathrm{Hz}", 11), max_x_label=twopi_label)
    doc.p("当抽样频率为 150 Hz 时：")
    draw_formula_rows(doc, [fs150, spec150], max_h=29)
    draw_impulse_spectrum(
        doc,
        [(0.34, twopi3_label, "π"), (0.67, fourpi3_label, "π")],
        title_path=f("title_fs150", r"f_s=150\mathrm{Hz}", 11),
        max_x_label=twopi_label,
    )

    doc.h2("2.4 系统函数 H(z)")
    doc.h3("2.4.1 系统函数定义")
    doc.p("在零初始状态下，系统输入与输出的 Z 变换之比称为系统函数，也称传递函数。")
    draw_formula(doc, h_def, max_h=30)
    doc.p("若系统对单位冲激的响应为 h(n)，则系统函数就是 h(n) 的 Z 变换。")
    draw_formula(doc, h_impulse, max_h=30)
    doc.bullet([
        "系统函数刻画系统在复频域中的性质。",
        "同一个代数式必须结合 ROC 才能判断因果性和稳定性。",
        "差分方程、系统函数、单位冲激响应三者可以互相转换。",
    ])

    doc.h3("2.4.2 用 Z 变换求解差分方程")
    doc.p("求解差分方程前先复习时移性质。双边 Z 变换的时移不会改变 ROC；单边 Z 变换的时移会多出初值项。")
    draw_formula_rows(doc, [bilateral_shift, uni_shift_r, uni_shift_l], max_h=31)
    draw_red_text(doc, "利用单边 z 变换求解差分方程时，初始条件会自然进入方程；如果题目只要求零状态响应，常可用双边形式。")
    doc.p("对一般线性常系数差分方程，源 PPT 给出的单边 Z 变换流程如下。")
    draw_formula_rows(doc, [diff_general, diff_unilateral], max_h=38)
    doc.note("初值项位置", "左端求和中的附加项来自系统初始状态；若输入 x(n) 为因果序列，右端附加项常为 0。", compact=True)

    doc.h3("例 1  用单边 Z 变换求零输入、零状态与全响应")
    draw_formula(doc, ex1_q, max_h=31)
    doc.p("对方程两端作单边 Z 变换，得到：")
    draw_formula(doc, ex1_z, max_h=32)
    doc.p("整理后可分解为零输入响应和零状态响应两部分：")
    draw_formula_rows(doc, [ex1_decomp, ex1_x], max_h=34)
    doc.p("零输入部分：")
    draw_formula_rows(doc, [ex1_yzi_pf, ex1_yzi], max_h=30)
    doc.p("零状态部分：")
    draw_formula_rows(doc, [ex1_yzs_pf, ex1_yzs, ex1_y], max_h=31)

    doc.h3("例 2  已知零状态响应求系统函数、冲激响应和差分方程")
    draw_formula(doc, ex2_q, max_h=36)
    doc.p("先由已知输入和零状态响应求系统函数，再作部分分式展开求 h(n)。")
    draw_formula_rows(doc, [ex2_hz, ex2_pf, ex2_hn], max_h=31)
    doc.p("把系统函数写成 z^{-1} 的有理式后，可直接读出差分方程。")
    draw_formula(doc, ex2_diff, max_h=30)

    doc.h2("2.4.3 因果稳定性判断")
    doc.h3("1. 时域判断")
    doc.p("对 LSI 系统，因果性看冲激响应是否只在非负时间存在；稳定性看冲激响应是否绝对可和。")
    draw_formula_rows(doc, [causal_td, stable_td, causal_stable_td], max_h=28)
    doc.h3("2. 频域判断（由 H(z) 的极点和收敛域判断）")
    doc.bullet([
        "因果：ROC 在最外层极点的外边，即大圆圆外。",
        "稳定：ROC 包含单位圆。",
        "临界稳定：有极点在单位圆上，实际处理中按不稳定看待。",
        "因果稳定：ROC 同时包含单位圆和单位圆外的整个平面。",
        "非因果系统也可能稳定，因果和稳定没有必然联系。",
    ])
    draw_red_text(doc, "注意：因果和稳定没有必然联系，非因果也可稳定。")
    draw_red_text(doc, "所有极点全部位于单位圆内，只能作为因果稳定系统的充分条件；极点在单位圆内不能单独推出系统因果稳定。")
    doc.p("总结：系统因果稳定当且仅当所有极点位于单位圆内，并且系统本身是因果系统。")

    doc.h3("例 1  已知 LTI 系统的冲激响应")
    draw_formula(doc, ex_u_piece, max_h=30)
    doc.p("从时域看，h(n) 为因果序列，因此系统因果；但绝对值求和发散，因此不稳定。")
    draw_formula(doc, ex_u_sum, max_h=26)
    doc.p("从 z 域看，系统函数和 ROC 如下。ROC 为圆外，所以因果；极点在单位圆上且 ROC 不包含单位圆，因此不稳定。")
    draw_formula(doc, ex_u_hz, max_h=28)

    doc.h3("例 2  不同 ROC 下的因果性、稳定性与反变换")
    draw_formula(doc, ex_h2_q, max_h=31)
    doc.p("由系统函数可知两个极点分别位于 1/2 和 2。三种 ROC 对应三种不同序列。")
    draw_formula_rows(doc, [ex_h2_case1, ex_h2_case2, ex_h2_case3], max_h=30)
    doc.bullet([
        "第一种 ROC 在大圆圆外：因果；不包含单位圆，不稳定。",
        "第二种 ROC 在小圆圆外、大圆圆内：非因果；包含单位圆，稳定。",
        "第三种 ROC 在小圆圆内：非因果；不包含单位圆，不稳定。",
    ])

    doc.h3("例 3  由差分方程判断稳定性并求单位取样响应")
    doc.p("已知因果 LSI 系统的差分方程，求系统函数和系统 ROC，判断稳定性，并求单位取样响应。")
    draw_formula(doc, ex3_q, max_h=26)
    doc.p("对方程两端取 Z 变换并整理：")
    draw_formula_rows(doc, [ex3_transform, ex3_hz, ex3_poles], max_h=30)
    paragraph_red_inline(doc, "由题目已知系统为", "因果系统", "，所以 ROC 在大圆圆外；因此 ROC 包含单位圆，系统稳定。")
    doc.p("继续作部分分式展开，得到单位取样响应：")
    draw_formula_rows(doc, [ex3_pf, ex3_hn], max_h=31)
    doc.p(
        "814 考点提示：这类题常把“因果”作为题干条件给出。只知道极点在单位圆内还不够，必须结合因果条件或 ROC，才能判断系统是否因果稳定。",
        size=8.8,
        leading=12.4,
    )

    doc.h2("2.4.4 系统的频率响应")
    doc.p("LTI 系统的频率响应是单位脉冲响应 h(n) 的 DTFT；从 z 域看，也就是系统函数在单位圆上的取值。")
    draw_formula_rows(doc, [freq_resp, freq_polar], max_h=26)
    doc.bullet([
        "幅频响应决定频率成分的去留。",
        "相频响应决定频率成分的移位。",
    ])
    doc.p("若频率响应的实部为 R，虚部为 X，则可用下式求幅度和相位。")
    draw_formula_rows(doc, [freq_amp, freq_phase], max_h=25)
    doc.h3("例  幅频响应和相频响应")
    draw_formula(doc, ratio_q, max_h=26, gap=5)
    draw_formula(doc, ratio_amp, max_h=40, gap=5)
    draw_formula(doc, ratio_phase, max_h=30, gap=8)
    doc.h3("例  一阶系统的幅相响应")
    draw_formula(doc, first_order_q, max_h=26, gap=5)
    draw_formula(doc, first_order_amp, max_h=40, gap=5)
    draw_formula(doc, first_order_phase, max_h=30, gap=8)

    doc.h2("2.4.4 系统的频率响应：正弦稳态")
    doc.p("若输入为固定频率的复指数序列，输出仍保持同一频率，只改变幅度和相位。")
    doc.y += 2
    draw_formula_rows(doc,[steady_input,steady_conv,steady_output],max_h=25,gap=1)
    draw_red_text(doc,"正弦稳态响应：幅度乘以幅频响应，相位加上相频响应。")
    draw_formula(doc,steady_sine,max_h=27,gap=2)

    doc.save()
    NOTE_PATH.write_text(
        """# 第四批 89-112 页校对记录

## 范围

- 源 PPT 页码：89-114
- 输出：`outputs/DSP讲义重制_第四批_原PPT89-114页_频域分析与系统函数_内容版.pdf`

## 本批遵循的规则

- 保留源 PPT 的章节导图、课后习题、章节目录、抽样频谱推导、系统函数定义、单边/双边 Z 变换时移差异、差分方程例题、因果稳定性红字结论、三道例题、系统频率响应定义和幅相响应例题。
- 公式均以数学公式图片嵌入，不在正文中留下源代码式题干。
- 红色重点改为红色加粗正文或红色公式，不删除。
- 装饰性网络背景、水印、Logo 不进入重制讲义。

## 明确修正

- 例 2 第三种 ROC 的反变换中，源页存在多余右括号，已按数学表达修正为一个完整等式。
""",
        encoding="utf-8",
    )
    print(PDF_PATH)


if __name__ == "__main__":
    build_pdf()
