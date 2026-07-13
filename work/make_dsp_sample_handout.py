from pathlib import Path
from math import sin, cos, pi

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True)
PDF_PATH = OUT_DIR / "DSP讲义重制_样章_前15页.pdf"
NOTE_PATH = OUT_DIR / "DSP讲义重制_样章_校对记录.md"

PAGE_W, PAGE_H = A4
MARGIN_X = 52
TOP = 770
BOTTOM = 58
BLUE = colors.HexColor("#0875D1")
BLUE_DARK = colors.HexColor("#075B9C")
BLUE_LIGHT = colors.HexColor("#EAF5FF")
LINE = colors.HexColor("#CADCEB")
TEXT = colors.HexColor("#1F2933")
MUTED = colors.HexColor("#5E6B75")
PALE = colors.HexColor("#F6F9FC")


def register_fonts():
    candidates = [
        ("CN", r"C:\Windows\Fonts\msyh.ttc"),
        ("CNB", r"C:\Windows\Fonts\msyhbd.ttc"),
        ("CNL", r"C:\Windows\Fonts\msyhl.ttc"),
    ]
    fallback = r"C:\Windows\Fonts\simhei.ttf"
    for name, path in candidates:
        try:
            pdfmetrics.registerFont(TTFont(name, path))
        except Exception:
            pdfmetrics.registerFont(TTFont(name, fallback))


def sw(font, size, text):
    return pdfmetrics.stringWidth(text, font, size)


def wrap(text, width, font="CN", size=10.4):
    out = []
    for para in text.split("\n"):
        if not para:
            out.append("")
            continue
        line = ""
        for ch in para:
            if sw(font, size, line + ch) <= width:
                line += ch
            else:
                if line:
                    out.append(line)
                line = ch
        if line:
            out.append(line)
    return out


class Doc:
    def __init__(self, path):
        self.c = canvas.Canvas(str(path), pagesize=A4)
        self.page = 0
        self.section = ""

    def header(self, title=None):
        self.page += 1
        c = self.c
        c.setFillColor(BLUE_DARK)
        c.rect(0, PAGE_H - 35, PAGE_W, 35, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("CN", 9.5)
        c.drawString(MARGIN_X, PAGE_H - 22, "DSP 讲义重制样章")
        c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 22, self.section or "数字信号处理基础")
        c.setStrokeColor(LINE)
        c.setLineWidth(0.7)
        c.line(MARGIN_X, 46, PAGE_W - MARGIN_X, 46)
        c.setFillColor(MUTED)
        c.setFont("CN", 8.5)
        c.drawString(MARGIN_X, 30, "根据原 PPT 前 15 页重排；原始水印不进入重制版")
        c.drawRightString(PAGE_W - MARGIN_X, 30, f"{self.page}")
        if title:
            self.title(title)

    def new_page(self, section="", title=None):
        if self.page:
            self.c.showPage()
        self.section = section
        self.header(title)
        return TOP

    def save(self):
        self.c.save()

    def title(self, text, y=TOP):
        c = self.c
        c.setFillColor(BLUE)
        c.setFont("CNB", 22)
        c.drawString(MARGIN_X, y, text)
        c.setStrokeColor(BLUE)
        c.setLineWidth(2.2)
        c.line(MARGIN_X, y - 10, MARGIN_X + 72, y - 10)

    def h2(self, text, y):
        c = self.c
        c.setFillColor(BLUE)
        c.roundRect(MARGIN_X, y - 20, 6, 20, 2, stroke=0, fill=1)
        c.setFillColor(TEXT)
        c.setFont("CNB", 14.6)
        c.drawString(MARGIN_X + 14, y - 15, text)
        return y - 34

    def h3(self, text, y):
        c = self.c
        c.setFillColor(BLUE_DARK)
        c.setFont("CNB", 11.8)
        c.drawString(MARGIN_X, y, text)
        return y - 18

    def p(self, text, y, width=None, size=10.2, color=TEXT, leading=16, first_indent=0):
        width = width or (PAGE_W - 2 * MARGIN_X)
        c = self.c
        c.setFillColor(color)
        c.setFont("CN", size)
        lines = wrap(text, width - first_indent if first_indent else width, "CN", size)
        for idx, line in enumerate(lines):
            c.drawString(MARGIN_X + (first_indent if idx == 0 else 0), y, line)
            y -= leading
        return y - 4

    def bullet(self, items, y, width=None, size=9.9, leading=15.5):
        width = width or (PAGE_W - 2 * MARGIN_X - 18)
        c = self.c
        c.setFont("CN", size)
        for item in items:
            c.setFillColor(BLUE)
            c.circle(MARGIN_X + 3.5, y + 3.5, 2.3, stroke=0, fill=1)
            c.setFillColor(TEXT)
            first = True
            for line in wrap(item, width, "CN", size):
                c.drawString(MARGIN_X + 16, y, line)
                y -= leading
                first = False
            if first:
                y -= leading
            y -= 2
        return y - 3

    def note(self, title, body, y, width=None):
        width = width or (PAGE_W - 2 * MARGIN_X)
        c = self.c
        lines = wrap(body, width - 30, "CN", 9.2)
        h = 31 + 14 * len(lines)
        c.setFillColor(BLUE_LIGHT)
        c.roundRect(MARGIN_X, y - h + 8, width, h, 4, stroke=0, fill=1)
        c.setStrokeColor(colors.HexColor("#9DCBF2"))
        c.roundRect(MARGIN_X, y - h + 8, width, h, 4, stroke=1, fill=0)
        c.setFillColor(BLUE_DARK)
        c.setFont("CNB", 9.6)
        c.drawString(MARGIN_X + 14, y - 14, title)
        c.setFillColor(TEXT)
        c.setFont("CN", 9.2)
        yy = y - 31
        for line in lines:
            c.drawString(MARGIN_X + 14, yy, line)
            yy -= 14
        return y - h - 8


def draw_cover(doc):
    c = doc.c
    doc.page += 1
    c.setFillColor(colors.white)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(BLUE_DARK)
    c.rect(0, PAGE_H - 165, PAGE_W, 165, stroke=0, fill=1)
    c.setFillColor(BLUE)
    c.rect(0, PAGE_H - 178, PAGE_W, 13, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("CNB", 25)
    c.drawString(MARGIN_X, PAGE_H - 76, "数字信号处理")
    c.setFont("CNB", 18)
    c.drawString(MARGIN_X, PAGE_H - 111, "A4 讲义重制样章")
    c.setFont("CN", 10.5)
    c.drawString(MARGIN_X, PAGE_H - 139, "样章范围：原课件前 15 页")

    y = PAGE_H - 238
    c.setFillColor(TEXT)
    c.setFont("CNB", 16)
    c.drawString(MARGIN_X, y, "第一章  数字信号处理概述与离散时域基础")
    y -= 32
    c.setFont("CN", 10.6)
    intro = (
        "本样章按照“教材讲义风”重新组织原 PPT 内容：保留知识主体和例题顺序，"
        "将横版投影片改为 A4 纵向阅读版，并去除原课件水印。版式采用清爽标题层级、"
        "表格归纳、流程图和少量考点提示，便于打印、批注和系统复习。"
    )
    for line in wrap(intro, PAGE_W - 2 * MARGIN_X, "CN", 10.6):
        c.drawString(MARGIN_X, y, line)
        y -= 18

    y -= 18
    c.setFillColor(PALE)
    c.roundRect(MARGIN_X, y - 150, PAGE_W - 2 * MARGIN_X, 150, 5, stroke=0, fill=1)
    c.setFillColor(BLUE_DARK)
    c.setFont("CNB", 12.4)
    c.drawString(MARGIN_X + 18, y - 26, "样章包含")
    c.setFillColor(TEXT)
    c.setFont("CN", 10.1)
    items = [
        "信号分类：模拟信号、时域离散信号、数字信号。",
        "模拟信号数字处理流程：预滤波、A/D、数字处理、D/A、平滑滤波。",
        "离散序列的表示：集合、函数表达式、图形表示。",
        "常用序列与复指数序列周期，序列的移位、翻转、抽取与插值。",
    ]
    yy = y - 52
    for item in items:
        c.setFillColor(BLUE)
        c.circle(MARGIN_X + 24, yy + 4, 2.2, stroke=0, fill=1)
        c.setFillColor(TEXT)
        c.drawString(MARGIN_X + 38, yy, item)
        yy -= 23

    c.setFillColor(MUTED)
    c.setFont("CN", 8.8)
    c.drawString(MARGIN_X, 30, "说明：这是排版样章，用于确认讲义风格；完整章节将按确认后的规范批量制作。")


def draw_table(c, x, y, col_w, row_h, headers, rows):
    total_w = sum(col_w)
    c.setFillColor(BLUE_DARK)
    c.roundRect(x, y - row_h, total_w, row_h, 4, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("CNB", 9.7)
    xx = x
    for i, h in enumerate(headers):
        c.drawCentredString(xx + col_w[i] / 2, y - 17, h)
        xx += col_w[i]
    y0 = y - row_h
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.setFont("CN", 9.2)
    for r, row in enumerate(rows):
        c.setFillColor(colors.white if r % 2 == 0 else PALE)
        c.rect(x, y0 - row_h, total_w, row_h, stroke=0, fill=1)
        c.setFillColor(TEXT)
        xx = x
        for i, text in enumerate(row):
            lines = wrap(text, col_w[i] - 14, "CN", 9.2)[:2]
            yy = y0 - 16
            for line in lines:
                c.drawString(xx + 7, yy, line)
                yy -= 12
            xx += col_w[i]
        y0 -= row_h
    c.setStrokeColor(LINE)
    xx = x
    c.rect(x, y - row_h * (len(rows) + 1), total_w, row_h * (len(rows) + 1), stroke=1, fill=0)
    for w in col_w[:-1]:
        xx += w
        c.line(xx, y, xx, y - row_h * (len(rows) + 1))
    return y - row_h * (len(rows) + 1) - 20


def draw_flow(c, x, y):
    labels = ["x_a(t)", "预滤波", "A/D 转换", "DSP", "D/A 转换", "平滑滤波", "y_a(t)"]
    widths = [54, 62, 68, 54, 68, 62, 54]
    gap = 13
    h = 32
    xx = x
    c.setFont("CNB", 8.8)
    for i, lab in enumerate(labels):
        c.setFillColor(colors.white)
        c.roundRect(xx, y - h, widths[i], h, 4, stroke=1, fill=1)
        c.setStrokeColor(BLUE)
        c.setFillColor(BLUE_DARK)
        c.drawCentredString(xx + widths[i] / 2, y - 20, lab)
        if i < len(labels) - 1:
            x1 = xx + widths[i] + 3
            x2 = xx + widths[i] + gap - 3
            c.setStrokeColor(BLUE)
            c.line(x1, y - h / 2, x2, y - h / 2)
            c.line(x2, y - h / 2, x2 - 4, y - h / 2 + 3)
            c.line(x2, y - h / 2, x2 - 4, y - h / 2 - 3)
        xx += widths[i] + gap
    return y - h - 16


def draw_stem(c, x, y, w, h, values, n_min=None, n_max=None, title=""):
    if n_min is None:
        n_min = min(values)
    if n_max is None:
        n_max = max(values)
    v_min = min(0, min(values.values()))
    v_max = max(1, max(values.values()))
    c.setStrokeColor(LINE)
    c.setFillColor(PALE)
    c.roundRect(x, y - h, w, h, 4, stroke=1, fill=1)
    left, right = x + 25, x + w - 14
    top, bottom = y - 20, y - h + 27
    y0 = bottom + (0 - v_min) / (v_max - v_min or 1) * (top - bottom)
    c.setStrokeColor(colors.HexColor("#91A8B8"))
    c.line(left, y0, right, y0)
    c.line(left, bottom, left, top)
    c.setFont("CN", 7.6)
    c.setFillColor(MUTED)
    c.drawString(left - 17, top - 4, "x[n]")
    c.drawRightString(right, y0 - 12, "n")
    count = n_max - n_min
    for n, v in values.items():
        px = left + (n - n_min) / (count or 1) * (right - left)
        py = bottom + (v - v_min) / (v_max - v_min or 1) * (top - bottom)
        c.setStrokeColor(BLUE)
        c.setLineWidth(1.1)
        c.line(px, y0, px, py)
        c.setFillColor(BLUE)
        c.circle(px, py, 2.2, stroke=0, fill=1)
        c.setFillColor(TEXT)
        c.drawCentredString(px, bottom - 12, str(n))
    if title:
        c.setFillColor(BLUE_DARK)
        c.setFont("CNB", 8.4)
        c.drawString(x + 11, y - 12, title)


def page_overview(doc):
    y = doc.new_page("概述", "0. 样章结构")
    y -= 40
    y = doc.h2("讲义化处理原则", y)
    y = doc.bullet(
        [
            "由 PPT 横屏演示稿改为 A4 纵向阅读稿，压缩空白，保留原知识顺序。",
            "将原有大字号标题、散点文字和水印统一改为讲义标题、正文、表格与图示。",
            "例题按普通小节呈现，不使用醒目的大边框；必要提示只服务于真题高频考点。",
            "明显符号和表述问题在正文中直接规范化，不在页面里放“校对备注”。",
        ],
        y,
    )
    y -= 4
    y = doc.h2("本样章知识路线", y)
    c = doc.c
    steps = [
        ("信号类型", "连续/离散/数字"),
        ("处理流程", "A/D - DSP - D/A"),
        ("序列表示", "集合/公式/图形"),
        ("常用序列", "δ[n], u[n], R_N[n]"),
        ("周期判断", "e^{jωn}"),
        ("序列运算", "移位/翻转/抽取/插值"),
    ]
    x, yy = MARGIN_X, y - 14
    box_w, box_h, gap = 76, 48, 8
    for title, sub in steps:
        c.setFillColor(BLUE_LIGHT)
        c.roundRect(x, yy - box_h, box_w, box_h, 4, stroke=0, fill=1)
        c.setStrokeColor(colors.HexColor("#ABD2F2"))
        c.roundRect(x, yy - box_h, box_w, box_h, 4, stroke=1, fill=0)
        c.setFillColor(BLUE_DARK)
        c.setFont("CNB", 9.5)
        c.drawCentredString(x + box_w / 2, yy - 18, title)
        c.setFillColor(MUTED)
        c.setFont("CN", 7.8)
        c.drawCentredString(x + box_w / 2, yy - 34, sub)
        x += box_w + gap
    y = yy - box_h - 35
    y = doc.note(
        "真题导向",
        "华理 814 真题中，采样、傅里叶/频率映射、滤波器和系统性质出现频率较高。本样章只在与前 15 页内容直接相关处加入采样与频率周期性的提示。",
        y,
    )


def page_signal_types(doc):
    y = doc.new_page("1. 信号与数字处理方法", "1.1 信号的分类")
    y -= 40
    y = doc.p("数字信号处理的对象可以从“时间变量是否连续”和“幅值是否连续”两个角度分类。理解这一点，是后续学习采样、量化和离散系统分析的入口。", y)
    y -= 6
    c = doc.c
    y = draw_table(
        c,
        MARGIN_X,
        y,
        [102, 132, 132, 125],
        42,
        ["类型", "时间变量", "幅值", "典型说明"],
        [
            ["模拟信号", "连续", "连续", "工程传感器输出、语音电压等"],
            ["时域离散信号", "离散", "可连续取值", "由采样得到，尚未量化"],
            ["数字信号", "离散", "离散", "采样后再量化、编码得到"],
        ],
    )
    y = doc.h2("关键关系", y)
    y = doc.bullet(
        [
            "数字信号一定是时域离散的，但时域离散信号不一定是数字信号。",
            "采样只让时间变量离散化；量化和编码才让幅值以数字形式表示。",
            "后续公式中常把离散序列写成 x[n]，用 n 表示整数序号，用 T 表示采样间隔。",
        ],
        y,
    )


def page_dsp_flow(doc):
    y = doc.new_page("1. 信号与数字处理方法", "1.2 模拟信号的数字处理")
    y -= 40
    y = doc.p("在实际系统中，许多输入和输出仍然是模拟量。数字信号处理方法的基本思想，是先把模拟信号转换成数字序列，在数字域完成处理，再按需要恢复为模拟信号。", y)
    y -= 10
    y = draw_flow(doc.c, MARGIN_X, y)
    y = doc.h2("各环节含义", y)
    y = doc.bullet(
        [
            "预滤波：限制输入带宽，降低混叠风险。",
            "A/D 转换：通常包括采样、量化、编码三个步骤。",
            "数字信号处理：在离散时间/数字域完成滤波、频谱分析、调制解调等运算。",
            "D/A 转换与平滑滤波：将数字序列转换成连续时间信号，并抑制重构后的阶梯和高频分量。",
        ],
        y,
    )
    y -= 2
    y = doc.note(
        "814 考法提示",
        "采样类题目常把采样频率、最高频率、混叠和理想重构放在一起考。复习时要同时记住 f_s >= 2f_m 的条件，以及数字频率 Ω = ωT 的映射关系。",
        y,
    )


def page_discrete_signal(doc):
    y = doc.new_page("2. 时域离散信号", "2.1 时域离散信号的表示")
    y -= 40
    y = doc.h2("由采样得到离散序列", y)
    y = doc.p("设连续时间模拟信号为 x_a(t)，以采样间隔 T 等间隔取样，得到的时域离散信号可写为", y)
    c = doc.c
    c.setFillColor(PALE)
    c.roundRect(MARGIN_X, y - 40, PAGE_W - 2 * MARGIN_X, 40, 4, stroke=0, fill=1)
    c.setFillColor(BLUE_DARK)
    c.setFont("CNB", 13)
    c.drawCentredString(PAGE_W / 2, y - 25, "x[n] = x_a(t)|_{t=nT} = x_a(nT),      n 为任意整数")
    y -= 62
    y = doc.p("这里 n 是整数序号，T 是相邻两次采样之间的时间间隔。原课件中常写作 x(n)，本讲义统一采用更常见的离散时间记号 x[n]，含义不变。", y)
    y = doc.h2("三种表示方法", y)
    y = doc.bullet(
        [
            "集合表示：用 {x[n]} 或列出若干样值，通常用下划线或标注说明 n=0 的位置。",
            "函数表示：给出 x[n] 关于 n 的表达式，例如 x[n]=n+1。",
            "图形表示：用离散竖线图表示每个整数 n 上的样值。",
        ],
        y,
    )
    draw_stem(c, MARGIN_X + 52, y - 10, 350, 125, {-1: 1, 0: 2, 1: 1, 2: 3}, -2, 3, "例：{1, 2, 1, 3}，其中 n=0 对应第二项")


def page_common_sequences(doc):
    y = doc.new_page("2. 时域离散信号", "2.2 常用离散序列")
    y -= 40
    y = draw_table(
        doc.c,
        MARGIN_X,
        y,
        [108, 160, 223],
        46,
        ["序列", "定义", "说明"],
        [
            ["单位脉冲 δ[n]", "δ[n]=1, n=0；δ[n]=0, n≠0", "离散系统中最基本的测试序列。"],
            ["单位阶跃 u[n]", "u[n]=1, n≥0；u[n]=0, n<0", "常用于表示因果序列。"],
            ["矩形序列 R_N[n]", "R_N[n]=1, 0≤n≤N-1；其他为 0", "长度为 N 的有限长序列。"],
            ["实指数序列", "x[n]=a^n u[n]", "a 的大小决定衰减或增长。"],
            ["正弦序列", "x[n]=sin(ωn)", "离散频率以 2π 为周期。"],
            ["复指数序列", "x[n]=C e^{jωn}", "判断周期性时要特别注意 ω/2π 是否为有理数。"],
        ],
    )
    y = doc.h2("学习重点", y)
    y = doc.p("这些序列既是离散系统分析的基本积木，也是卷积、差分方程、频域变换中的常用输入。后续讨论系统响应时，单位脉冲响应 h[n] 将起到核心作用。", y)


def page_complex_period(doc):
    y = doc.new_page("2. 时域离散信号", "2.3 复指数序列的周期")
    y -= 40
    y = doc.p("考虑复指数序列 e^{jωn}。若存在正整数 N，使得对所有整数 n 都有 e^{jω(n+N)}=e^{jωn}，则称该序列为周期序列，最小的正整数 N 称为基波周期。", y)
    c = doc.c
    c.setFillColor(PALE)
    c.roundRect(MARGIN_X, y - 84, PAGE_W - 2 * MARGIN_X, 84, 4, stroke=0, fill=1)
    c.setFillColor(TEXT)
    c.setFont("CNB", 12)
    c.drawString(MARGIN_X + 18, y - 24, "e^{jω(n+N)} = e^{jωn}  <=>  e^{jωN}=1")
    c.drawString(MARGIN_X + 18, y - 52, "ωN = 2πk,  k 为整数  <=>  2π/ω 为有理数")
    y -= 108
    y = doc.h2("判定规则", y)
    y = doc.bullet(
        [
            "若 2π/ω 为无理数，则 e^{jωn} 不是周期序列。",
            "若 2π/ω 为整数，则该整数就是周期。",
            "若 2π/ω = A/B，其中 A、B 互素，则最小周期为 A。",
        ],
        y,
    )
    y = doc.h3("例 1  求下列序列的周期", y)
    y = doc.bullet(
        [
            "e^{j5n}：2π/5 为无理数，因此不是周期序列。",
            "e^{j2πn/12}：2π/(2π/12)=12，最小周期 N=12。",
            "e^{j8πn/31}：2π/(8π/31)=31/4，最小周期 N=31。",
        ],
        y,
    )
    y = doc.note(
        "考点连接",
        "离散时间频率以 2π 为周期，ω 与 ω+2πm 对应同一个序列。这个性质会在 DTFT、DFT 和采样频谱题中反复出现。",
        y,
    )


def page_oscillation_ops(doc):
    y = doc.new_page("2. 时域离散信号", "2.3-2.4 振荡速率与序列运算")
    y -= 40
    y = doc.h2("离散正弦序列的振荡速率", y)
    y = doc.p("连续时间正弦信号的频率越大，振荡越快；但在离散时间中，频率以 2π 为周期。通常只需关注 0 到 π 的频率范围，超过 π 后会与低频序列发生等价或折叠关系。", y)
    c = doc.c
    x0, y0 = MARGIN_X + 12, y - 20
    labels = ["ω=0", "ω=π/4", "ω=π/2", "ω=π"]
    for i, om in enumerate([0, pi / 4, pi / 2, pi]):
        vals = {n: cos(om * n) for n in range(0, 9)}
        draw_stem(c, x0 + i * 118, y0, 104, 92, vals, 0, 8, labels[i])
    y = y0 - 115
    y = doc.h2("序列的基本运算", y)
    y = doc.bullet(
        [
            "相加：c[n]=a[n]+b[n]，要求在同一 n 上逐点相加。",
            "相乘：c[n]=a[n]b[n]，要求在同一 n 上逐点相乘。",
            "移位：x[n-n0] 表示原序列右移 n0 个单位；x[n+n0] 表示原序列左移 n0 个单位。",
        ],
        y,
    )


def page_transform_exercise(doc):
    y = doc.new_page("2. 时域离散信号", "2.4 序列的变换")
    y -= 40
    y = doc.h2("翻转、抽取与插值", y)
    y = doc.bullet(
        [
            "翻转：x[-n] 是 x[n] 关于 n=0 的镜像。",
            "抽取：x[Mn] 只保留原序列中序号能被 M 对应取到的样值，常表现为时间轴压缩。",
            "插值：x[n/M] 可理解为在相邻样值之间插入 M-1 个零，再按新的整数序号表示。",
        ],
        y,
    )
    y = doc.p("处理复合变换时，建议先看括号内的新自变量，例如 x[1-2n]；再列出使 1-2n 落入原序列非零区间的整数 n。这样比直接凭直觉平移、翻转更稳。", y)
    y = doc.h3("例 2  画出 x[1-2n] 的图像", y)
    c = doc.c
    c.setFillColor(PALE)
    c.roundRect(MARGIN_X, y - 102, PAGE_W - 2 * MARGIN_X, 102, 4, stroke=0, fill=1)
    c.setFillColor(TEXT)
    c.setFont("CNB", 11.5)
    c.drawString(MARGIN_X + 18, y - 25, "已知")
    c.setFont("CN", 10.8)
    c.drawString(MARGIN_X + 60, y - 25, "x[n] = 3n+1,  -1≤n≤1")
    c.drawString(MARGIN_X + 60, y - 49, "x[n] = 1,      2≤n≤3")
    c.drawString(MARGIN_X + 60, y - 73, "x[n] = 0,      其他 n")
    y -= 125
    y = doc.note(
        "解题入口",
        "先令 m=1-2n，再筛选 m 属于 {-1,0,1,2,3} 时对应的整数 n，并据此作出 x(1-2n) 的离散图。",
        y,
    )


def write_notes():
    NOTE_PATH.write_text(
        """# DSP讲义重制_样章_校对记录

## 样章范围

- 原始文件：`C:\\Users\\HP\\Desktop\\DPS课件\\DSP课件.pdf`
- 范围：前 15 页 PPT 内容
- 参考文件：`C:\\Users\\HP\\Desktop\\讲义、做题本\\华理814真题.pdf`
- 输出：`outputs/DSP讲义重制_样章_前15页.pdf`

## 已按样章规范处理

- 横版 PPT 改为 A4 纵向讲义，不采用简单二合一拼页。
- 去除原 PPT 页面水印，正文、图示、表格均重新排版。
- 统一采用较常见的离散序列记号 `x[n]`，并注明与原课件 `x(n)` 含义一致。
- 将 A/D 过程补全为采样、量化、编码，将 D/A 后的平滑滤波表述得更清楚。
- 例题不做大边框；按普通小节和练习题呈现。
- 只在采样、频率周期性等华理 814 高频相关处加入轻量“考法提示”。

## 需要用户确认

- 当前样章是风格与密度确认稿，例 2 只保留题面和解题入口；如果你希望样章也补全答案，我可以在定稿版加入。
- 若确认本样章风格，后续可按同一规范处理全部章节，并单独维护完整校对记录。
""",
        encoding="utf-8",
    )


def main():
    register_fonts()
    doc = Doc(PDF_PATH)
    draw_cover(doc)
    page_overview(doc)
    page_signal_types(doc)
    page_dsp_flow(doc)
    page_discrete_signal(doc)
    page_common_sequences(doc)
    page_complex_period(doc)
    page_oscillation_ops(doc)
    page_transform_exercise(doc)
    doc.save()
    write_notes()
    print(PDF_PATH)
    print(NOTE_PATH)


if __name__ == "__main__":
    main()
