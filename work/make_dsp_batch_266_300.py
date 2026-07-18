from pathlib import Path
import sys
import os

HERE = Path(__file__).resolve().parents[1]
ORIG = Path(r"C:\Users\HP\Documents\Codex\2026-07-01\zh")
ORIG_WORK = ORIG / "work"
sys.path.insert(0, str(ORIG_WORK))

MPL_DIR = HERE / "work" / "mplcache"
MPL_DIR.mkdir(parents=True, exist_ok=True)
os.environ["MPLCONFIGDIR"] = str(MPL_DIR)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

from make_dsp_sample_handout_v2 import (
    BLUE,
    BLUE_DARK,
    CONTENT_W,
    MARGIN_X,
    MUTED,
    TEXT,
    Doc,
    PAGE_H,
    PAGE_W,
    register_fonts,
    normalize_display_formula_height,
    wrap,
)


OUT_DIR = HERE / "outputs"
WORK_DIR = HERE / "work"
FIG_DIR = WORK_DIR / "figures" / "batch_266_300"
FORMULA_DIR = WORK_DIR / "formula_cache"
for d in [OUT_DIR, FIG_DIR, FORMULA_DIR]:
    d.mkdir(parents=True, exist_ok=True)

PDF_PATH = OUT_DIR / "DSP讲义重制_第九批_原PPT266-300页_IIR滤波器设计_内容版.pdf"
NOTE_PATH = OUT_DIR / "DSP讲义重制_第九批_原PPT266-300页_IIR滤波器设计_校对记录.md"
SRC_DIR = ORIG_WORK / "pdfs" / "source_pages_261_300"


plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["font.family"] = "STIXGeneral"


def formula_png(name, expr, fontsize=13, color="#111111"):
    path = FORMULA_DIR / f"b266_{name}.png"
    fig = plt.figure(figsize=(0.01, 0.01), dpi=300)
    fig.patch.set_alpha(0)
    fig.text(0, 0, f"${expr}$", fontsize=fontsize, color=color)
    fig.savefig(path, dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    return path


def img_size(path):
    return Image.open(path).size


def draw_formula(doc, path, max_w=None, max_h=36, gap=11, center=True):
    max_h = normalize_display_formula_height(max_h)
    doc.ensure(max_h + gap)
    iw, ih = img_size(path)
    max_w = max_w or CONTENT_W * 0.88
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    x = MARGIN_X + (CONTENT_W - dw) / 2 if center else MARGIN_X
    doc.c.drawImage(ImageReader(str(path)), x, doc.y - dh, dw, dh, mask="auto")
    doc.y -= dh + gap


def crop_source(page, crop, suffix="main"):
    src = SRC_DIR / f"src-{page}.png"
    out = FIG_DIR / f"src-{page}_{suffix}.png"
    if not out.exists():
        Image.open(src).crop(crop).save(out)
    return out


def draw_source_crop(doc, page, title=None, crop=(45, 140, 1625, 1015), max_h=235, gap=12, suffix="main"):
    reserve = max_h + gap + (28 if title else 0)
    doc.ensure(reserve)
    if title:
        doc.h3(title)
    path = crop_source(page, crop, suffix)
    iw, ih = img_size(path)
    scale = min(CONTENT_W / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    x = MARGIN_X + (CONTENT_W - dw) / 2
    doc.c.drawImage(ImageReader(str(path)), x, doc.y - dh, dw, dh, mask="auto")
    doc.y -= dh + gap


def draw_note(doc, title, lines):
    wrapped = []
    total = 0
    for line in lines:
        parts = wrap(line, CONTENT_W - 24, "CN", 9.1)
        wrapped.append(parts)
        total += len(parts)
    h = 30 + total * 14 + 10
    doc.ensure(h + 12)
    c = doc.c
    y = doc.y - h
    c.setStrokeColor(colors.HexColor("#A5D4FF"))
    c.setFillColor(colors.HexColor("#F3FAFF"))
    c.roundRect(MARGIN_X, y, CONTENT_W, h, 4, stroke=1, fill=1)
    c.setFont("CNB", 9.8)
    c.setFillColor(BLUE_DARK)
    c.drawString(MARGIN_X + 12, y + h - 20, title)
    c.setFont("CN", 9.1)
    c.setFillColor(TEXT)
    yy = y + h - 39
    for parts in wrapped:
        for line in parts:
            c.drawString(MARGIN_X + 12, yy, line)
            yy -= 14
    doc.y = y - 12


def chapter_overview(doc):
    doc.h1("第五章 IIR系统的网络结构与滤波器设计", "原PPT 266-300 页内容重制")
    doc.p("本批进入第五章。原 PPT 的封面页和目录页转换为本章标题与讲义目录；后续知识页按 5.1 信号流图、5.2 IIR 基本网络结构、5.3 模拟滤波器设计与巴特沃斯低通滤波器展开。")
    doc.bullet([
        "5.1 信号流图：数字滤波器、幅频/相频响应、滤波器分类、结构表示方法。",
        "5.2 IIR 基本网络结构：直接 I 型、直接 II 型、级联型、并联型。",
        "5.3 模拟滤波器设计：典型低通/高通/带通/带阻特性，巴特沃斯低通滤波器设计方法。",
    ])


def build():
    register_fonts()
    doc = Doc(PDF_PATH)
    doc.section = "第五章 IIR滤波器设计"
    doc.start()
    chapter_overview(doc)

    doc.h2("5.1 信号流图与数字滤波器")
    doc.p("数字滤波器是输入、输出均为数字信号，并通过数值运算改变输入信号频率成分比例的系统。对于 LTI 系统，滤波既可以从时域卷积理解，也可以从频域乘积理解。")
    draw_formula(doc, formula_png("lti_filter", r"y(n)=\sum_{m=-\infty}^{\infty}x(m)h(n-m)=F^{-1}\{X(e^{j\omega})H(e^{j\omega})\}", 14), max_h=38)
    draw_source_crop(doc, 269, "幅频响应选择频率成分", crop=(55, 205, 1530, 760), max_h=175)
    draw_note(doc, "相频响应", [
        "幅频响应决定不同频率分量通过或被抑制的程度；相频响应决定不同频率分量通过滤波器后的移位情况。",
        "若滤波器具有线性相位，则输入信号各频率分量的移位具有一致性，是后续 FIR 设计中的重要目标。",
    ])
    draw_source_crop(doc, 270, "数字滤波器分类", crop=(40, 160, 1600, 900), max_h=230)
    draw_source_crop(doc, 271, "结构表示方法与基本运算单元", crop=(55, 200, 1500, 980), max_h=220)
    draw_source_crop(doc, 272, "二阶数字滤波器方框图与信号流图", crop=(55, 170, 1560, 1000), max_h=245)

    doc.h2("5.2 IIR 基本网络结构")
    doc.p("IIR 滤波器的单位脉冲响应无限长，系统函数在有限 z 平面上存在极点，结构上有从输出到输入的反馈。稳定 IIR 滤波器的全部极点应位于单位圆内。")
    draw_source_crop(doc, 273, "IIR 滤波器特点", crop=(55, 160, 1520, 840), max_h=205)
    draw_formula(doc, formula_png("iir_general", r"y(n)=\sum_{i=1}^{N}a_i y(n-i)+\sum_{i=0}^{M}b_i x(n-i)", 14), max_h=36)
    draw_formula(doc, formula_png("iir_hz_general", r"H(z)=\frac{\sum_{i=0}^{M}b_i z^{-i}}{1-\sum_{i=1}^{N}a_i z^{-i}}", 15), max_h=46)
    draw_source_crop(doc, 274, "三类基本网络结构", crop=(45, 155, 1600, 900), max_h=220)

    doc.h2("5.2.2 直接 I 型 IIR 滤波器")
    doc.p("直接 I 型按差分方程直接展开：横向延时链实现零点，反馈延时链实现极点。它需要的延时单元数为 N+M，且系数变化会显著影响零极点位置。")
    draw_source_crop(doc, 275, "直接 I 型结构图", crop=(40, 145, 1605, 960), max_h=250)
    draw_source_crop(doc, 276, "二阶直接 I 型推导", crop=(50, 145, 1605, 1010), max_h=245)
    draw_source_crop(doc, 277, "直接 I 型结构特点", crop=(40, 160, 1605, 990), max_h=255)

    doc.h2("5.2.3 直接 II 型 IIR 滤波器")
    doc.p("直接 II 型通过变量替换合并前后两个延时网络，所需延时单元最少，因此也称典范型。实现时仍要注意反馈部分系数符号。")
    draw_source_crop(doc, 278, "直接 II 型合并过程", crop=(40, 135, 1615, 1010), max_h=260)
    draw_source_crop(doc, 279, "例：有理式归一化为 z 的负幂", crop=(40, 150, 1570, 980), max_h=240)
    draw_source_crop(doc, 280, "直接 I 型与直接 II 型结构流图", crop=(55, 180, 1570, 880), max_h=220)
    draw_source_crop(doc, 281, "例：两个系统函数的实现要求", crop=(45, 160, 1540, 760), max_h=175)

    doc.h2("5.2.4 级联型 IIR 数字滤波器")
    doc.p("级联型将系统函数分解为若干一阶或二阶子系统的乘积。每个子系统分别实现后再串联，便于按零极点成对控制滤波器特性。")
    draw_source_crop(doc, 282, "级联型分解形式", crop=(40, 150, 1605, 965), max_h=250)
    draw_source_crop(doc, 283, "级联型例题结构", crop=(40, 155, 1605, 1000), max_h=250)

    doc.h2("5.2.5 并联型 IIR 数字滤波器")
    doc.p("并联型将系统函数分解为若干部分分式之和，各分支分别实现后相加。它适合由部分分式展开得到的实现结构。")
    draw_source_crop(doc, 284, "并联型结构图", crop=(45, 155, 1605, 980), max_h=245)
    draw_source_crop(doc, 285, "并联型例题分解", crop=(40, 150, 1605, 975), max_h=250)
    draw_source_crop(doc, 286, "并联型系统函数表达", crop=(45, 150, 1580, 935), max_h=230)
    draw_source_crop(doc, 287, "并联型结构实现", crop=(45, 155, 1585, 950), max_h=235)
    draw_source_crop(doc, 288, "IIR 基本结构小结", crop=(40, 150, 1605, 1015), max_h=255)

    doc.h2("5.3 模拟滤波器设计")
    doc.p("IIR 数字滤波器常由模拟滤波器设计出发，通过变换得到数字滤波器。因此本节先给出模拟滤波器设计的一般思路和典型模拟滤波器特性。")
    draw_source_crop(doc, 289, "模拟滤波器设计到数字滤波器", crop=(45, 145, 1605, 1005), max_h=250)
    draw_source_crop(doc, 290, "模拟低通与高通滤波器指标", crop=(45, 150, 1605, 980), max_h=240)
    draw_source_crop(doc, 291, "模拟带通与带阻滤波器指标", crop=(45, 150, 1605, 980), max_h=240)

    doc.h2("5.3.1 模拟低通滤波器设计指标")
    doc.p("模拟低通滤波器设计以通带截止频率、阻带截止频率、通带最大衰减和阻带最小衰减为核心指标。常用分贝指标表达通带/阻带约束。")
    draw_source_crop(doc, 292, "设计指标与衰减定义", crop=(45, 145, 1605, 970), max_h=245)
    draw_source_crop(doc, 293, "3 dB 截止频率示意", crop=(45, 150, 1605, 990), max_h=245)
    draw_source_crop(doc, 294, "由指标确定模拟滤波器", crop=(45, 150, 1605, 960), max_h=235)

    doc.h2("5.3.2 巴特沃斯低通滤波器")
    doc.p("巴特沃斯低通滤波器具有单调下降的幅频响应。设计时先根据阶数确定极点分布，再构造系统函数，并由表格或公式确定多项式。")
    draw_source_crop(doc, 295, "巴特沃斯低通幅度平方函数", crop=(45, 145, 1605, 970), max_h=245)
    draw_source_crop(doc, 296, "极点分布与系统函数", crop=(45, 145, 1605, 985), max_h=250)
    draw_source_crop(doc, 297, "归一化低通系统函数", crop=(45, 150, 1605, 980), max_h=250)
    draw_source_crop(doc, 298, "巴特沃斯多项式表 1", crop=(50, 140, 1605, 1000), max_h=260)
    draw_source_crop(doc, 299, "巴特沃斯多项式表 2", crop=(50, 140, 1605, 1000), max_h=260)
    draw_source_crop(doc, 300, "巴特沃斯多项式表 3", crop=(50, 140, 1605, 1000), max_h=260)
    draw_note(doc, "查表使用", [
        "巴特沃斯低通滤波器按阶数 N 选择对应多项式 B(p)。若设计给出非归一化截止频率，应先完成频率归一化，再由表中多项式恢复实际系统函数。",
        "表格中的因式分解形式便于后续级联实现；展开式适合直接计算系数。",
    ])

    doc.save()

    NOTE_PATH.write_text(
        "# 第九批校对记录\n\n"
        "- 范围：原 PPT 266-300 页，第五章开头至巴特沃斯低通滤波器设计方法。\n"
        "- 266-267：章节封面与目录已转为讲义标题和目录，不直接保留横板装饰页。\n"
        "- 268-272：数字滤波器定义、幅频/相频响应、分类、结构表示方法和二阶例题均已带入。\n"
        "- 273-288：IIR 特点、直接 I 型、直接 II 型、级联型、并联型及对应例题均已保留；复杂结构图按源页主体裁切嵌入，避免重绘改变拓扑。\n"
        "- 289-300：模拟滤波器设计流程、典型模拟滤波器指标、低通设计指标和巴特沃斯多项式表均已保留。\n"
        "- 当前取舍：本批先采用源页主体裁切图保真，背景水印暂按用户已认可的取舍保留；后续精排可逐页改成更细的图文重排。\n",
        encoding="utf-8",
    )
    print(PDF_PATH)
    print(NOTE_PATH)


if __name__ == "__main__":
    build()



