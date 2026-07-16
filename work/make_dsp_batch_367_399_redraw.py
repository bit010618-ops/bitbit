from pathlib import Path
import sys, math
from reportlab.lib import colors

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'work'
sys.path.insert(0,str(WORK))

from make_dsp_batch_266_300_redraw import (
    BLUE, BLUE_DARK, CONTENT_W, MARGIN_X, TEXT, Doc, register_fonts,
    RED, PALE_BLUE, YELLOW, draw_math_at, draw_formula_block,
    draw_note, arrow, dot, wrap, draw_centered_multiline_text
)
from make_dsp_sample_handout_v2 import draw_auto_math_block, draw_auto_math_text, piecewise_png

OUT_DIR=ROOT/'outputs'
PDF_PATH=OUT_DIR/'DSP讲义重制_第十二批_原PPT367-399页_FIR滤波器设计_手绘复刻版.pdf'
NOTE_PATH=OUT_DIR/'DSP讲义重制_第十二批_原PPT367-399页_FIR滤波器设计_手绘复刻版_校对记录.md'
BLACK=colors.HexColor('#111111')
GREEN=colors.HexColor('#0A8F3A')
LIGHT_RED=colors.HexColor('#FFF1F1')
GRID=colors.HexColor('#B8B8B8')


def red_line(doc, text, size=9.5, leading=15):
    lines=wrap(text, CONTENT_W, 'CN', size)
    doc.ensure(len(lines)*leading+4)
    bottom=draw_auto_math_block(
        doc.c,MARGIN_X,doc.y+size,text,CONTENT_W,
        font='CNB',size=size,leading=leading,color=RED,
    )
    doc.y=bottom-size-3


def red_filter_relation(doc, result, left, operator, right, name):
    """Draw Chinese explanation text with real math-rendered omega subscripts."""
    doc.ensure(20)
    c = doc.c
    c.setFont('CNB', 9.6)
    c.setFillColor(RED)
    x = MARGIN_X
    y = doc.y

    prefix = f'{result} = {left}('
    c.drawString(x, y, prefix)
    x += c.stringWidth(prefix, 'CNB', 9.6)
    width, _ = draw_math_at(
        c, r'\omega_2', x, y + 3, max_w=24, max_h=13,
        fontsize=12, color='#E00000', name=f'{name}_omega2',
    )
    x += width

    middle = f') {operator} {right}('
    c.drawString(x, y, middle)
    x += c.stringWidth(middle, 'CNB', 9.6)
    width, _ = draw_math_at(
        c, r'\omega_1', x, y + 3, max_w=24, max_h=13,
        fontsize=12, color='#E00000', name=f'{name}_omega1',
    )
    x += width
    c.drawString(x, y, ')。')
    doc.y -= 18


def label_line(doc, label, text, red=False):
    doc.ensure(18)
    c=doc.c
    c.setFont('CNB',9.6); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X, doc.y, label)
    c.setFont('CN',9.4); c.setFillColor(RED if red else TEXT); c.drawString(MARGIN_X+72, doc.y, text)
    doc.y-=17


def draw_piecewise2(doc, name, lhs, row1, row2, height=62, fontsize=17):
    path = piecewise_png(name, lhs, row1, row2, fontsize=fontsize)
    doc.formula_box(path, height=height)


def mini_axis(c, x, y, w, h, title='', marks=None, bars=None, red=False):
    marks=marks or []
    bars=bars or []
    col=RED if red else BLACK
    c.setStrokeColor(col); c.setFillColor(col); c.setLineWidth(1.0)
    arrow(c,x,y,x+w,y,col,1.0)
    arrow(c,x,y-h*0.45,x,y+h*0.55,col,1.0)
    c.setFont('CN',7.4); c.setFillColor(col)
    c.drawString(x+w+3,y-4,'ω')
    if title:
        draw_auto_math_text(
            c, x+10, y+h*0.55+11, title, font='CN', size=7.4,
            color=col, math_size=9.5, math_height=13,
        )
    for pos,lab in marks:
        xx=x+w*pos
        c.line(xx,y-3,xx,y+3)
        draw_auto_math_text(
            c, xx, y-12, lab, font='CN', size=7.4,
            color=col, align='center', math_size=9.5, math_height=13,
        )
    for a,b,lev in bars:
        xa=x+w*a; xb=x+w*b; yy=y+h*lev
        c.setStrokeColor(RED); c.setLineWidth(1.2)
        c.line(xa,yy,xb,yy); c.line(xa,y,xa,yy); c.line(xb,y,xb,yy)


def linear_phase_classification_example(doc):
    doc.h3('例：由 h(n) 判断线性相位类型与可实现滤波器')
    doc.p('已知两组 FIR 单位脉冲响应，判断它们的振幅特性和相位特性，并说明可设计的滤波器类型。')
    draw_formula_block(doc,r'\text{(1) }N=6:\ \{5,1.5,3,2,1.5,5\};\qquad '
                           r'\text{(2) }N=7:\ \{3,2,1,0,-1,-2,-3\}',
                       'lp_class_source_sequences',fontsize=12.5,max_h=42)
    doc.bullet(['第一组为偶对称序列，群延迟 τ=(N-1)/2=5/2；按 N 的奇偶与对称性判为偶对称、N 偶数的线性相位 FIR。',
                '第二组为奇对称序列，群延迟 τ=(N-1)/2=3；H(ω) 在 ω=0、π 处为零，可设计带通滤波器。'])
    red_line(doc,'判断顺序：先看 N 奇偶，再看 h(n) 对称或反对称，最后查四类线性相位表。',size=9.1)


def ideal_impulse_responses(doc):
    doc.h3('四类理想滤波器的无限长冲激响应')
    rows=[
        ('低通',r'h_d(n)=\frac{\sin[\omega_c(n-\tau)]}{\pi(n-\tau)}'),
        ('高通',r'h_d(n)=\frac{\sin[\pi(n-\tau)]-\sin[\omega_c(n-\tau)]}{\pi(n-\tau)}'),
        ('带通',r'h_d(n)=\frac{\sin[\omega_2(n-\tau)]-\sin[\omega_1(n-\tau)]}{\pi(n-\tau)}'),
        ('带阻',r'h_d(n)=\frac{\sin[\pi(n-\tau)]-\sin[\omega_2(n-\tau)]+\sin[\omega_1(n-\tau)]}{\pi(n-\tau)}'),
    ]
    for i,(name,expr) in enumerate(rows):
        doc.ensure(42)
        doc.c.setFillColor(BLUE_DARK); doc.c.setFont('CNB',9.8)
        doc.c.drawString(MARGIN_X,doc.y-4,name)
        draw_math_at(doc.c,expr,MARGIN_X+85,doc.y+6,CONTENT_W-95,28,11.5,name=f'ideal_h_{i}')
        doc.y-=40
    red_line(doc,'理想响应均为无限长序列；实际 FIR 必须再用窗函数截断，且 τ=(N-1)/2。',size=9.1)


def ideal_filters(doc):
    h=260
    doc.ensure(h+8)
    c=doc.c; top=doc.y
    c.setFont('CNB',10.5); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-4,'四类理想频率响应与冲激响应')
    y=top-58; w=175; gap=72; h0=45
    x1=MARGIN_X+20; x2=MARGIN_X+20; x3=MARGIN_X+300; x4=MARGIN_X+300
    c.setFont('CNB',8.8); c.setFillColor(TEXT)
    items=[('低通',x1,y,[(0,'0'),(.45,'ωc'),(.78,'π')],[(0,.45,.68)]),('高通',x3,y,[(0,'0'),(.42,'ωc'),(.78,'π')],[(.42,.78,.68)]),('带通',x2,y-88,[(0,'0'),(.28,'ω1'),(.55,'ω2'),(.82,'π')],[(.28,.55,.68)]),('带阻',x4,y-88,[(0,'0'),(.28,'ω1'),(.55,'ω2'),(.82,'π')],[(0,.28,.68),(.55,.82,.68)])]
    for name,x,yy,marks,bars in items:
        c.drawString(x,yy+h0+24,name)
        mini_axis(c,x,yy,w,h0,r'|H_d(e^{jω})|',marks,bars,red=True)
    doc.y=top-h


def window_flow(doc):
    h=145
    doc.ensure(h+8)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-8,'窗函数法的基本思想')
    y=top-55; x=MARGIN_X+25
    boxes=[('无限长\n理想响应',80),('窗函数\nw(n)',76),('有限长\nh(n)',76)]
    for i,(txt,bw) in enumerate(boxes):
        bx=x+i*150
        c.setStrokeColor(BLUE); c.setLineWidth(1.1); c.roundRect(bx,y-20,bw,40,3,stroke=1,fill=0)
        draw_centered_multiline_text(c,bx+bw/2,y,txt,'CNB',9.2,leading=15,color=TEXT)
        if i<2: arrow(c,bx+bw,y,bx+135,y,BLUE,1.2)
    draw_math_at(c,r'h(n)=h_d(n)w(n)',x+300,y-30,180,24,13,name='win_h')
    draw_math_at(c,r'H(e^{j\omega})=H_d(e^{j\omega})*W(e^{j\omega})',x+245,y-67,250,24,12,name='win_freq')
    doc.y=top-h


def _window_effect_layout():
    return {'offsets': [10, 191, 372], 'width': 116, 'label_allowance': 11}


def window_effect(doc):
    h=190
    doc.ensure(h+6)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-5,'截断与窗函数的影响')
    layout=_window_effect_layout()
    xs=[MARGIN_X+offset for offset in layout['offsets']]
    labs=['理想低通','矩形窗后','实际低通']
    for i,x in enumerate(xs):
        y=top-75
        c.setFont('CN',8.2); c.setFillColor(TEXT); c.drawCentredString(x+65,y+60,labs[i])
        mini_axis(c,x,y,layout['width'],42,'',[(0,'0'),(.35,'ωc'),(.8,'π')],[],red=False)
        if i==0:
            c.setStrokeColor(RED); c.line(x,y+28,x+44,y+28); c.line(x+44,y+28,x+44,y); c.line(x+44,y,x+100,y)
        elif i==1:
            c.setStrokeColor(RED)
            pts=[(0,28),(12,27),(24,23),(35,11),(45,4),(55,11),(68,8),(82,5),(100,3)]
            for (a,b),(c1,d1) in zip(pts,pts[1:]): c.line(x+a,y+b,x+c1,y+d1)
        else:
            c.setStrokeColor(RED)
            pts=[(0,29),(32,28),(43,22),(52,10),(62,4),(76,7),(95,3)]
            for (a,b),(c1,d1) in zip(pts,pts[1:]): c.line(x+a,y+b,x+c1,y+d1)
    c.setFont('CNB',8.4); c.setFillColor(RED)
    c.drawString(MARGIN_X, top-145, '出现的过冲和波纹称为 Gibbs 现象；窗函数的旁瓣决定阻带衰减，主瓣宽度决定阻带波纹。')
    c.drawString(MARGIN_X, top-158, '主瓣宽度决定过渡带宽，窗函数选择时要同时看阻带衰减和过渡带宽。')
    doc.y=top-h


def window_table(doc):
    headers=['窗函数类型','旁瓣峰值(dB)','过渡带宽 Δω','阻带最小衰减(dB)']
    rows=[
        ['矩形窗','-13','4π/N','-21'],
        ['三角形窗','-25','8π/N','-25'],
        ['汉宁窗','-31','8π/N','-44'],
        ['海明窗','-41','8π/N','-53'],
        ['布莱克曼窗','-57','12π/N','-74'],
    ]
    doc.table(headers, rows, [150,120,120,130], row_h=28)
    red_line(doc,'选择窗函数时先看阻带衰减，再用过渡带宽估算 N；考试中常用 Δω 与 α_s 对应表。',size=9.0)


def zero_plane(doc):
    h=230
    doc.ensure(h+8)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-6,'例：由已知零点补全线性相位 FIR 零点')
    c.setFont('CN',8.8); c.setFillColor(TEXT)
    draw_auto_math_text(c,MARGIN_X,top-28,'0.5 是自镜像零点；0.5e^{±jπ/4} 还需补它们关于单位圆的倒数共轭零点。',font='CN',size=8.8)
    c.setFont('CNB',8.8); c.setFillColor(RED)
    draw_auto_math_text(c,MARGIN_X,top-45,'因此最低阶数为 7 个零点，对应 N=8，群延迟 τ=(N-1)/2=3.5。',font='CNB',size=8.8,color=RED)
    cx=MARGIN_X+385; cy=top-125; r=48
    c.setStrokeColor(BLUE); c.circle(cx,cy,r,stroke=1,fill=0)
    arrow(c,cx-r-25,cy,cx+r+35,cy,BLACK,0.9); arrow(c,cx,cy-r-24,cx,cy+r+26,BLACK,0.9)
    c.setFont('CN',7.5); c.setFillColor(TEXT); c.drawString(cx+r+38,cy-3,'Re'); c.drawString(cx+4,cy+r+26,'Im')
    pts=[(1,0,'1'),(0.5,0,'0.5'),(0.5/math.sqrt(2),0.5/math.sqrt(2),r'0.5e^{j\pi/4}'),(0.5/math.sqrt(2),-0.5/math.sqrt(2),r'0.5e^{-j\pi/4}'),(2/math.sqrt(2),2/math.sqrt(2),r'2e^{j\pi/4}'),(2/math.sqrt(2),-2/math.sqrt(2),r'2e^{-j\pi/4}')]
    for px,py,lab in pts:
        xx=cx+px*r; yy=cy+py*r
        c.setFillColor(RED if abs(px)>1 or abs(py)>1 else BLACK); c.circle(xx,yy,3,stroke=0,fill=1)
    draw_math_at(c,r'\{1,0.5,0.5e^{\pm j\frac{\pi}{4}}\}\Rightarrow\{2e^{\pm j\frac{\pi}{4}}\}',MARGIN_X+30,top-125,250,28,13,name='zeros_set')
    doc.y=top-h

def sampled_response(doc):
    h=155
    doc.ensure(h+8)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK)
    draw_auto_math_text(c,MARGIN_X,top-6,'频率采样例题：N=33 的低通采样',font='CNB',size=10,color=BLUE_DARK)
    x=MARGIN_X+75; y=top-92; w=380; hh=58
    mini_axis(c,x,y,w,hh,'H_k',[(0,'0'),(8/33,'8'),(9/33,'9'),(16/33,'16'),(25/33,'25'),(32/33,'32')],[],red=True)
    c.setStrokeColor(BLUE); c.setFillColor(colors.Color(0.55,0.75,1,alpha=0.6))
    for k in list(range(0,9))+list(range(25,33)):
        xx=x+w*k/33
        c.line(xx,y,xx,y+45); c.circle(xx,y+45,1.8,stroke=0,fill=1)
    c.setFont('CN',8.2); c.setFillColor(TEXT); c.drawString(x+145,y-25,'0.5π 对应 8.25 点，按线性相位约束取 0...8 与 25...32 为通带采样点。')
    doc.y=top-h


def sampling_structure(doc):
    h=125
    doc.ensure(h+8)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-8,'频率采样结构')
    draw_formula_block(doc,r'H(z)=\sum_{n=0}^{N-1}h(n)z^{-n}=\frac{1}{N}(1-z^{-N})\sum_{k=0}^{N-1}\frac{H(k)}{1-W_N^kz^{-1}}','freq_sampling_structure',fontsize=13,max_h=42,gap=8)
    red_line(doc,'FIR 直接型结构与频率采样型结构是同一个 H(z) 的两种实现。',size=9.0)


def source_window_definitions():
    return [
        ('矩形窗', r'w(n)=R_N(n)'),
        ('三角窗', r'w(n)=\begin{cases}\frac{2n}{N-1},&0\leq n\leq\frac{N-1}{2}\\2-\frac{2n}{N-1},&\frac{N-1}{2}<n\leq N-1\end{cases}'),
        ('汉宁窗(升余弦窗)', r'w(n)=\frac{1}{2}\left[1-cos\frac{2\pi n}{N-1}\right]R_N(n)'),
        ('海明窗(改进的升余弦窗)', r'w(n)=\left[0.54-0.46cos\frac{2\pi n}{N-1}\right]R_N(n)'),
        ('布莱克曼窗', r'w(n)=\left[0.42-0.5cos\frac{2\pi n}{N-1}+0.08cos\frac{4\pi n}{N-1}\right]R_N(n)'),
    ]


def draw_window_definitions(doc):
    doc.h2('6.5.2 常用窗函数')
    red_line(doc, '常见窗函数及其性能指标要牢记；考试可能不提供。', size=10.2)
    for idx, (name, expr) in enumerate(source_window_definitions()):
        doc.ensure(66)
        doc.c.setFont('CNB', 10.3); doc.c.setFillColor(TEXT)
        doc.c.drawString(MARGIN_X, doc.y, f'（{idx + 1}）{name}')
        doc.y -= 10
        if name == '三角窗':
            draw_piecewise2(doc, 'source_window_triangle', r'w(n)=',
                            r'\frac{2n}{N-1},\ 0\leq n\leq\frac{N-1}{2}',
                            r'2-\frac{2n}{N-1},\ \frac{N-1}{2}<n\leq N-1',
                            height=70, fontsize=15)
        else:
            draw_formula_block(doc, expr, f'source_window_{idx}', fontsize=13.5, max_h=46, gap=12)


def draw_window_six_diagrams(doc):
    doc.h2('6.5.2 窗函数截断的时域与频域过程')
    doc.p('用窗函数将无限长理想冲激响应截成有限长序列。时域是相乘，频域是卷积。')
    c = doc.c
    top = doc.y - 8
    left = MARGIN_X + 22
    right = MARGIN_X + 300
    row_gap = 145
    labels = [('h_d(n)', 'H_d(e^{jω})'), ('R_N(n)', 'W(e^{jω})'), ('h(n)', 'H(e^{jω})')]
    for row, (lt, rt) in enumerate(labels):
        cy = top - row * row_gap - 62
        # Left: source-style finite/infinite sample sequence.
        x0 = left + 12; w = 190
        arrow(c, x0, cy, x0 + w, cy, BLACK, 0.9)
        arrow(c, x0 + w / 2, cy - 35, x0 + w / 2, cy + 48, BLACK, 0.9)
        c.setFont('CN', 8.2); c.setFillColor(TEXT)
        draw_auto_math_text(
            c, x0 + 4, cy + 51, lt, font='CN', size=8.2,
            color=TEXT, math_size=10.5, math_height=14,
        )
        for k in range(-6, 7):
            xx = x0 + w / 2 + k * 13
            if row == 0:
                val = 34 * math.sin(0.58 * (k + 0.001)) / (2.8 * (k + 0.001))
            elif row == 1:
                val = 29 if -4 <= k <= 4 else 0
            else:
                val = (34 * math.sin(0.58 * (k + 0.001)) / (2.8 * (k + 0.001))) if -4 <= k <= 4 else 0
            if abs(val) > 0.3:
                c.setStrokeColor(BLACK); c.line(xx, cy, xx, cy + val)
                c.setFillColor(BLACK); c.circle(xx, cy + val, 1.6, stroke=0, fill=1)
        # Right: ideal, window, and resulting response.
        rx = right + 10; rw = 190
        arrow(c, rx, cy, rx + rw, cy, BLACK, 0.9)
        arrow(c, rx + rw / 2, cy - 32, rx + rw / 2, cy + 48, BLACK, 0.9)
        draw_auto_math_text(
            c, rx + 4, cy + 51, rt, font='CN', size=8.2,
            color=TEXT, math_size=10.5, math_height=14,
        )
        c.setStrokeColor(RED); c.setLineWidth(1.3)
        if row == 0:
            c.line(rx + 14, cy + 31, rx + 76, cy + 31); c.line(rx + 76, cy + 31, rx + 76, cy)
            c.line(rx + 114, cy, rx + 114, cy + 31); c.line(rx + 114, cy + 31, rx + 176, cy + 31)
        elif row == 1:
            pts = [(0,30),(18,26),(37,15),(55,4),(73,-2),(92,3),(111,-2),(130,4),(150,15),(170,26),(188,30)]
            for (a,b),(d,e) in zip(pts,pts[1:]): c.line(rx+a,cy+b,rx+d,cy+e)
        else:
            pts = [(0,30),(28,29),(46,27),(61,20),(74,8),(84,2),(95,5),(106,2),(118,8),(132,20),(147,27),(166,29),(188,30)]
            for (a,b),(d,e) in zip(pts,pts[1:]): c.line(rx+a,cy+b,rx+d,cy+e)
    doc.y = top - 3 * row_gap + 8


def draw_gibbs_page(doc):
    doc.h2('截断引起的 Gibbs 现象')
    doc.p('频谱的主瓣与窗函数卷积后必然产生拓展、变宽和旁瓣，从而造成截断效应，即频谱泄漏。')
    c = doc.c; x = MARGIN_X + 45; y = doc.y - 230; w = CONTENT_W - 90; h = 160
    arrow(c, x, y, x + w, y, BLACK, 1.0)
    arrow(c, x + w * 0.52, y - 18, x + w * 0.52, y + h, BLACK, 1.0)
    c.setFont('CN', 8.5); c.setFillColor(TEXT)
    c.drawString(x + w + 4, y - 3, 'ω')
    draw_auto_math_text(c,x+w*0.52+5,y+h-2,'|H(ω)|',font='CN',size=8.5)
    pts=[]
    for i in range(160):
        t=-4.2+8.4*i/159
        base=1/(1+math.exp(6.2*t))
        ripple=0.11*math.sin(17*t)*math.exp(-0.55*abs(t))
        pts.append((x+w*(i/159), y+22+(base+ripple)*105))
    c.setStrokeColor(RED); c.setLineWidth(1.35)
    for p,q in zip(pts,pts[1:]): c.line(p[0],p[1],q[0],q[1])
    c.setStrokeColor(colors.HexColor('#777777')); c.setDash(3,3)
    c.line(x+w*.43,y,x+w*.43,y+132); c.line(x+w*.61,y,x+w*.61,y+132)
    c.setDash()
    c.setFont('CNB', 9.1); c.setFillColor(RED)
    c.drawString(x+18,y+140,'实际低通'); c.drawString(x+w*.39,y-14,'主瓣展宽与过渡带'); c.drawString(x+w*.63,y+72,'旁瓣与波纹')
    doc.y = y - 34
    red_line(doc, '主瓣宽度决定过渡带宽；旁瓣峰值决定阻带最小衰减。', size=10)


def draw_sampling_constraints(doc):
    doc.h2('频率采样法的线性相位约束条件')
    doc.p('设计线性相位滤波器时，必须先判断 N 的奇偶、h(n) 的对称性和滤波器类型。')
    headers=['条件','一类线性相位','二类线性相位']
    rows=[
        ['对称性','h(n)=h(N-1-n)','h(n)=-h(N-1-n)'],
        ['相位','θ_k=-(N-1)πk/N','θ_k=π/2-(N-1)πk/N'],
        ['N为奇数','H_k=H_{N-k}；H(ω) 关于 0、2π 偶对称','H_k=-H_{N-k}；H(0)=H(π)=0'],
        ['N为偶数','H_k=-H_{N-k}；H(ω) 关于 π 奇对称','H_k=H_{N-k}；H(π)=0'],
    ]
    doc.table(headers, rows, [110,205,205], row_h=42)
    red_line(doc, '重要：幅度采样 H_k 的正负号和端点零值由对称类型与 N 的奇偶共同决定。', size=9.5)


def draw_sampling_process(doc):
    doc.h2('频率采样法设计过程')
    steps=[
        '根据题目给出的采样点数 N 和滤波器类型判断线性相位是哪一类。',
        '根据对称性写出线性相位 θ_k 和幅度 H_k 的表达式。',
        '通过题目设计滤波器的截止频率 ω_c，求出截止频率处对应的 k 值。',
        '在频率采样点处画出频率响应采样后的幅频图像。',
        '根据频域采样后的幅频图像写出H(k)的表达式。',
    ]
    for i, text in enumerate(steps, 1):
        doc.p(f'（{i}）{text}', size=10.1, leading=17)
    draw_formula_block(doc, r'H(k)=H_ke^{j\theta_k}', 'sampling_process_Hk', fontsize=18, max_h=42)


def fir_chapter_map(doc):
    doc.h2('本章导图')
    c=doc.c; top=doc.y-20; cx=MARGIN_X+CONTENT_W/2; cy=top-240
    c.setFillColor(BLUE_DARK); c.setStrokeColor(BLUE_DARK)
    c.roundRect(cx-75,cy-28,150,56,7,stroke=1,fill=0)
    draw_centered_multiline_text(c,cx,cy,'FIR 滤波器结构与\n滤波器设计','CNB',11,leading=17,color=BLUE_DARK)
    branches=[
        ('线性相位 FIR', MARGIN_X+85, top-65, ['四类线性相位','零点成组性质','系统函数结构']),
        ('理想滤波器', MARGIN_X+82, top-370, ['低通/高通','带通/带阻','无限长 h_d(n)']),
        ('窗函数法', MARGIN_X+CONTENT_W-95, top-65, ['五种常用窗','指标与经验公式','设计步骤与例题']),
        ('频率采样法', MARGIN_X+CONTENT_W-98, top-370, ['幅度与相位约束','设计过程','N=33 例题']),
    ]
    for title,bx,by,items in branches:
        c.setStrokeColor(colors.HexColor('#666666')); c.setLineWidth(1.0)
        arrow(c,cx+(35 if bx>cx else -35),cy+(12 if by>cy else -12),bx,by,colors.HexColor('#666666'),1.0)
        c.setFillColor(colors.white); c.setStrokeColor(BLUE)
        c.roundRect(bx-58,by-18,116,36,5,stroke=1,fill=1)
        c.setFont('CNB',9.5); c.setFillColor(BLUE_DARK); c.drawCentredString(bx,by-3,title)
        yy=by-36
        c.setFont('CN',8.3); c.setFillColor(TEXT)
        for item in items:
            draw_auto_math_text(
                c, bx, yy, item, font='CN', size=8.3, color=TEXT,
                align='center', math_size=10.2, math_height=13,
            )
            yy-=15
    doc.y=top-500


def draw_source_367_374(doc):
    doc.h2('6.4.3 线性相位 FIR 系统函数零点特点')
    linear_phase_classification_example(doc)
    doc.h3('由 z 变换表达式和线性相位条件分析零点')
    draw_formula_block(doc,r'H(z)=\sum_{n=0}^{N-1}h(n)z^{-n}', 'source369_Hz', fontsize=16, max_h=38)
    doc.p('h(n) 为 N 点长因果序列，H(z) 是 N-1 阶多项式，并且全部零点位于 z 平面原点以外的有限位置。')
    draw_formula_block(doc,r'H(z)=\pm z^{-(N-1)}H(z^{-1})', 'source370_relation', fontsize=17, max_h=40)
    label_line(doc,'结论 1','线性相位 FIR 滤波器的零点关于单位圆镜像对称。',red=True)
    label_line(doc,'结论 2','若 h(n) 为实序列，零点还具有共轭对称。',red=True)
    doc.bullet(['N-1 个零点中，关于单位圆镜像成对出现。','z 平面圆以外的极点只有原点，因此 FIR 系统稳定。'])
    zero_plane(doc)


def draw_source_375_379(doc):
    doc.new_page(); doc.h2('6.5.1 线性相位 FIR 理想滤波器')
    doc.h3('1. 理想低通滤波器')
    draw_piecewise2(doc, 'source375_lp', r'H_d(e^{j\omega})=',
                    r'e^{-j\omega\tau},\ |\omega|\leq\omega_c',
                    r'0,\ \omega_c<|\omega|\leq\pi', height=68, fontsize=16)
    draw_formula_block(doc,r'\tau=\frac{N-1}{2}', 'source375_tau', fontsize=15, max_h=34)
    draw_formula_block(doc,r'h_d(n)=\frac{\sin[\omega_c(n-\tau)]}{\pi(n-\tau)}', 'source375_lph', fontsize=16, max_h=38)
    doc.h3('2. 理想高通滤波器')
    draw_formula_block(doc,r'h_d(n)=\frac{\sin[\pi(n-\tau)]-\sin[\omega_c(n-\tau)]}{\pi(n-\tau)}', 'source376_hph', fontsize=15, max_h=42)
    red_line(doc,'高通滤波器 = 全通滤波器 - 低通滤波器。',size=9.6)
    doc.h3('3. 理想带通滤波器')
    draw_formula_block(doc,r'h_d(n)=\frac{\sin[\omega_2(n-\tau)]-\sin[\omega_1(n-\tau)]}{\pi(n-\tau)}', 'source377_bph', fontsize=15, max_h=42)
    red_filter_relation(doc, '带通滤波器', '低通滤波器', '-', '低通滤波器', 'source377_relation')
    doc.h3('4. 理想带阻滤波器')
    draw_formula_block(doc,r'h_d(n)=\frac{\sin[\pi(n-\tau)]-\sin[\omega_2(n-\tau)]+\sin[\omega_1(n-\tau)]}{\pi(n-\tau)}', 'source378_bsh', fontsize=14, max_h=42)
    red_filter_relation(doc, '带阻滤波器', '高通滤波器', '+', '低通滤波器', 'source378_relation')
    ideal_filters(doc)
    doc.h2('6.5.2 利用窗函数法设计 FIR 滤波器')
    window_flow(doc)
    draw_formula_block(doc,r'h(n)=h_d(n)w(n),\qquad H(e^{j\omega})=H_d(e^{j\omega})*W(e^{j\omega})', 'source379_window', fontsize=16, max_h=42)
    doc.bullet([
        '无限长理想冲激响应 h_d(n) 与有限长窗函数 w(n) 在时域相乘，得到可实现的有限长 h(n)。',
        '对 h(n) 作 DTFT 后，时域相乘对应频域卷积，因此实际频响等于理想频响与窗函数频谱的卷积。',
        '窗函数的主瓣宽度影响过渡带宽，旁瓣峰值影响阻带最小衰减，二者共同决定实际滤波器性能。',
    ], size=9.8, leading=17)


def draw_source_380_384(doc):
    doc.new_page(); draw_window_six_diagrams(doc)
    doc.new_page(); draw_gibbs_page(doc)
    doc.new_page(); draw_window_definitions(doc)
    doc.new_page(); doc.h2('窗函数性能指标与设计步骤')
    window_table(doc)
    doc.h3('用窗函数法设计 FIR 滤波器的步骤')
    doc.bullet(['求数字滤波器指标 ω_p、ω_st、α_p、α_s、Δω。','求 h_d(n)。','根据阻带衰减 α_s 选择窗函数，所选窗的 α_s 要比题目给定数值大。','由过渡带宽确定 N。','求 FIR 滤波器 h(n)。'],size=10,leading=17)
    doc.p('阻带衰减 α_s 决定窗函数类型；过渡带宽 Δω 决定长度 N。', size=9.8)
    draw_formula_block(doc,r'\alpha_s\Longrightarrow w(n),\qquad \Delta\omega=\frac{A}{N}\Longrightarrow N=\frac{A}{\Delta\omega}', 'source384_steps', fontsize=14, max_h=46)


def draw_source_385_389(doc):
    doc.new_page(); doc.h2('例：窗函数法设计低通 FIR 数字滤波器')
    doc.p('指标：抽样频率 f_s=15 kHz；通带截止频率 f_p=1.5 kHz；阻带截止频率 f_{st}=3 kHz；阻带衰减不小于 50 dB。')
    doc.h3('（1）求数字滤波器指标')
    draw_formula_block(doc,r'\omega_p=2\pi\frac{f_p}{f_s}=0.2\pi,\quad \omega_{st}=2\pi\frac{f_{st}}{f_s}=0.4\pi', 'source386_freq', fontsize=15, max_h=42)
    draw_formula_block(doc,r'\omega_c=\frac{\omega_p+\omega_{st}}{2}=0.3\pi,\quad \Delta\omega=\omega_{st}-\omega_p=0.2\pi', 'source386_wc', fontsize=15, max_h=42)
    doc.h3('（2）根据题目要求写出理想滤波器')
    draw_piecewise2(doc, 'source387_hd', r'H_d(e^{j\omega})=',
                    r'e^{-j\omega\tau},\ |\omega|\leq\omega_c',
                    r'0,\ \omega_c<|\omega|\leq\pi', height=68, fontsize=16)
    draw_formula_block(doc,r'\tau=\frac{N-1}{2}', 'source387_tau', fontsize=15, max_h=34)
    draw_formula_block(doc,r'h_d(n)=\frac{\sin[\omega_c(n-\tau)]}{\pi(n-\tau)}', 'source387_hd_n', fontsize=16, max_h=38)
    red_line(doc,'tips：理想滤波器的四大类必须背住。',size=9.6)
    doc.new_page(); doc.h3('（3）根据阻带衰减选择窗函数并确定 N')
    doc.p('阻带衰减为 50 dB。根据指标表，矩形窗与三角窗不满足，选择海明窗。')
    draw_formula_block(doc,r'w(n)=\left[0.54-0.46\cos\frac{2\pi n}{N-1}\right]R_N(n)', 'source388_hamming', fontsize=15, max_h=42)
    draw_formula_block(doc,r'N=\frac{A}{\Delta\omega}=\frac{6.6\pi}{0.2\pi}=33,\qquad \tau=\frac{N-1}{2}=16', 'source388_N', fontsize=16, max_h=42)
    doc.h3('（4）确定 FIR 滤波器的 h(n)')
    draw_formula_block(doc,r'h(n)=\frac{\sin[0.3\pi(n-16)]}{\pi(n-16)}\left[0.54-0.46\cos\frac{2\pi n}{32}\right]R_{33}(n)', 'source389_hn', fontsize=14, max_h=55)
    red_line(doc,'设计滤波器时必须牢记每一步，N 满足线性相位中心位置的要求。',size=9.6)


def draw_source_390_397(doc):
    doc.new_page(); doc.h2('6.5.3 利用频率采样法设计 FIR 滤波器')
    doc.h3('1. 基本思想')
    doc.p('在 0 到 2π 之间等间隔采样 N 点，得到 H_d(k)，再作 N 点 IDFT 得到 h(n)。')
    draw_formula_block(doc,r'H(k)=H_d(e^{j\omega})\mid_{\omega=\frac{2\pi k}{N}},\quad k=0,1,\ldots,N-1', 'source390_sample', fontsize=15, max_h=42)
    draw_formula_block(doc,r'h(n)=\frac{1}{N}\sum_{k=0}^{N-1}H(k)W_N^{-kn},\quad n=0,1,\ldots,N-1', 'source390_idft', fontsize=15, max_h=42)
    sampling_structure(doc)
    doc.new_page(); draw_sampling_constraints(doc)
    doc.new_page(); draw_sampling_process(doc)
    doc.new_page(); doc.h2('例：频率采样法设计线性相位低通 FIR')
    doc.p('理想幅频特性为低通，截止频率 ω_c=0.5π，采样点数为奇数 N=33。求各采样点幅值 H_k、相位 θ_k，并写出 H(k)。')
    doc.p('（1）N=33 是奇数，设计低通滤波器，判定为一类线性相位。')
    doc.p('（2）根据一类线性相位写出幅度和相位约束。')
    draw_formula_block(doc,r'H_k=H_{N-k},\qquad \theta_k=-\frac{N-1}{N}\pi k=-\frac{32}{33}\pi k', 'source395_constraint', fontsize=15, max_h=42)
    doc.p('（3）由截止频率求 k：')
    draw_formula_block(doc,r'k=\frac{\omega_c}{2\pi}N=\frac{0.5\pi}{2\pi}\cdot 33=8.25', 'source395_k', fontsize=16, max_h=40)
    doc.p('（4）画出频率响应采样后的幅频图像：')
    sampled_response(doc)
    doc.p('（5）写出H(k)的表达式：')
    draw_piecewise2(doc, 'source397_Hk', r'H_k=',
                    r'1,\ 0\leq k\leq8,\ 25\leq k\leq32',
                    r'0,\ 9\leq k\leq24', height=68, fontsize=16)
    draw_formula_block(doc,r'H(k)=H_ke^{j\theta_k},\qquad \theta_k=-\frac{32}{33}\pi k,\quad 0\leq k\leq32', 'source397_H', fontsize=15, max_h=42)


def draw_source_398_399(doc):
    doc.new_page(); fir_chapter_map(doc)
    doc.new_page(); doc.h2('课后习题')
    doc.bullet([
        '1：简单的对 FIR 滤波器的幅频和相频响应的描述。',
        '2：频率采样法设计滤波器的知识点，还要考核对两个响应形式的理解，关注 N 的奇偶。',
        '3：与第一题本质上差不多，需要进一步给出两个响应的具体形式，其实应该算最基础的小问。',
        '4-5-6：窗函数法设计 FIR 滤波器，注意 N 的限制。',
        '8：第一小问做个回顾，常规的小综合题。',
        '13-14-15：频率采样法设计 FIR 滤波器。',
        '17：同上。',
        '18：与上一题差不多，只不过频域的离散值要自己求出来，注意 ω 和 k 的互相转化。',
    ],size=10.2,leading=18)


def build():
    register_fonts(); OUT_DIR.mkdir(exist_ok=True)
    doc=Doc(PDF_PATH); doc.section='第六章 FIR滤波器设计'; doc.start()

    draw_source_367_374(doc)
    draw_source_375_379(doc)
    draw_source_380_384(doc)
    draw_source_385_389(doc)
    draw_source_390_397(doc)
    draw_source_398_399(doc)

    doc.save()
    NOTE_PATH.write_text('第十二批覆盖原 PPT 367-399 页，已按源页内容组展开为完整 A4 讲义：保留线性相位零点、四类理想滤波器、五种窗函数定义、指标表、窗函数法例题、频率采样约束与例题、章节导图和完整课后题。\n',encoding='utf-8')
    print(PDF_PATH)

if __name__=='__main__':
    build()




