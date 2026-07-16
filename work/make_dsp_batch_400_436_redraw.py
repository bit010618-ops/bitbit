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
from make_dsp_sample_handout_v2 import draw_auto_math_block, draw_auto_math_text

OUT_DIR=ROOT/'outputs'
PDF_PATH=OUT_DIR/'DSP讲义重制_第十三批_原PPT400-436页_多采样率数字信号处理_手绘复刻版.pdf'
NOTE_PATH=OUT_DIR/'DSP讲义重制_第十三批_原PPT400-436页_多采样率数字信号处理_手绘复刻版_校对记录.md'
BLACK=colors.HexColor('#111111')
GREEN=colors.HexColor('#149647')
ORANGE=colors.HexColor('#F59E0B')
LIGHT_YELLOW=colors.HexColor('#FFF8CC')
CYAN=colors.HexColor('#DFF7FF')


def red_line(doc,text,size=9.2,leading=14):
    lines=wrap(text,CONTENT_W,'CNB',size)
    doc.ensure(len(lines)*leading+4)
    bottom=draw_auto_math_block(
        doc.c,MARGIN_X,doc.y+size,text,CONTENT_W,
        font='CNB',size=size,leading=leading,color=RED,
    )
    doc.y=bottom-size-3


def blue_label(doc,text):
    doc.ensure(18); doc.c.setFont('CNB',10); doc.c.setFillColor(BLUE_DARK); doc.c.drawString(MARGIN_X,doc.y,text); doc.y-=17


def block(c,x,y,w,h,label,stroke=BLUE,fill=None,font=9.2):
    if fill: c.setFillColor(fill); c.roundRect(x,y-h/2,w,h,3,stroke=0,fill=1)
    c.setStrokeColor(stroke); c.setLineWidth(1.1); c.roundRect(x,y-h/2,w,h,3,stroke=1,fill=0)
    draw_centered_multiline_text(c,x+w/2,y,label,'CNB',font,leading=13,color=TEXT)


def tdm_rate_block_geometry():
    return {
        'input_block_center_x': 108,
        'input_label_center_x': 108,
        'output_block_center_x': 371,
        'output_label_center_x': 371,
        'block_center_y': 0,
        'label_center_y': 0,
    }


def system_chain(doc,title,labels,colors_fill=None):
    h=95; doc.ensure(h+8); c=doc.c; top=doc.y
    draw_auto_math_text(c,MARGIN_X,top-6,title,font='CNB',size=10,color=BLUE_DARK)
    x=MARGIN_X+40; y=top-50
    colors_fill=colors_fill or [None]*len(labels)
    draw_math_at(c,r'x(n)',x-42,y+7,38,16,11,name=title+'x')
    for i,lab in enumerate(labels):
        bx=x+i*105
        arrow(c,bx-30 if i==0 else bx-26,y,bx,y,BLUE,1.1)
        block(c,bx,y,68,32,lab,stroke=BLUE,fill=colors_fill[i])
    arrow(c,x+(len(labels)-1)*105+68,y,x+(len(labels)-1)*105+112,y,BLUE,1.1)
    draw_math_at(c,r'y(n)',x+(len(labels)-1)*105+118,y+7,40,16,11,name=title+'y')
    doc.y=top-h


def draw_dat_conversion_chain(doc):
    h = 95
    doc.ensure(h + 8)
    c = doc.c
    top = doc.y
    c.setFont('CNB', 10)
    c.setFillColor(BLUE_DARK)
    c.drawString(MARGIN_X, top - 6, '单级转换系统')
    x = MARGIN_X + 40
    y = top - 50
    draw_math_at(c, r'x(n)', x - 42, y + 7, 38, 16, 11, name='dat_chain_x')
    labels = ['↑L\n内插', '', '↓M\n抽取']
    fills = [YELLOW, CYAN, YELLOW]
    for i, label in enumerate(labels):
        bx = x + i * 105
        arrow(c, bx - 30 if i == 0 else bx - 26, y, bx, y, BLUE, 1.1)
        block(c, bx, y, 68, 32, label, stroke=BLUE, fill=fills[i])
        if i == 1:
            draw_math_at(c, r'H(e^{j\omega})', bx + 7, y + 11, 54, 13, 9.5, name='dat_chain_filter')
            c.setFillColor(TEXT)
            c.setFont('CNB', 7.6)
            c.drawCentredString(bx + 34, y - 10, '低通滤波')
    arrow(c, x + 2 * 105 + 68, y, x + 2 * 105 + 112, y, BLUE, 1.1)
    draw_math_at(c, r'y(n)', x + 2 * 105 + 118, y + 7, 40, 16, 11, name='dat_chain_y')
    doc.y = top - h


def spectrum_axis_geometry():
    return {"vertical_arrow_headroom": 12}


def spectrum_axis(c,x,y,w,h,label='',peaks=None,color=RED):
    geometry = spectrum_axis_geometry()
    c.setStrokeColor(BLACK); c.setFillColor(BLACK); c.setLineWidth(0.9)
    arrow(c,x,y,x+w,y,BLACK,0.9)
    arrow(c,x+w/2,y-8,x+w/2,y+h+geometry["vertical_arrow_headroom"],BLACK,0.9)
    c.setFont('CN',7.2); c.drawString(x+w+3,y-3,'ω')
    if label: c.drawCentredString(x+w/2,y-28,label)
    for pos,txt in [(0,'-π'),(.25,'-π/2'),(.5,'0'),(.75,'π/2'),(1,'π')]:
        xx=x+w*pos; c.line(xx,y-3,xx,y+3)
        if txt == '0':
            draw_auto_math_text(c,xx-5,y-14,txt,font='CN',size=7.2,color=BLACK,align='right')
        else:
            draw_auto_math_text(
                c,xx,y-12,txt,font='CN',size=7.2,color=BLACK,
                align='center',math_size=9.3,math_height=13,
            )
    peaks=peaks or [(.5,1.0)]
    c.setStrokeColor(color); c.setLineWidth(1.2)
    for pos,amp in peaks:
        xx=x+w*pos; c.line(xx,y,xx,y+h*amp); c.circle(xx,y+h*amp,2,stroke=0,fill=1)


def freq_replicas(doc,title='频谱重复与混叠示意',mode='dec'):
    h=180; doc.ensure(h+8); c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-6,title)
    y=top-70
    if mode=='dec':
        spectrum_axis(c,MARGIN_X+25,y,210,48,'抽取前',[(.5,1),(.25,.55),(.75,.55)],RED)
        spectrum_axis(c,MARGIN_X+310,y,210,48,'抽取后：谱间距变大，可能混叠',[(.5,1),(.15,.55),(.85,.55),(.35,.45),(.65,.45)],RED)
        c.setFont('CNB',9); c.setFillColor(RED); c.drawString(MARGIN_X+250,y+15,'M 倍抽取')
    else:
        spectrum_axis(c,MARGIN_X+25,y,210,48,'内插前',[(.5,1),(.3,.5),(.7,.5)],RED)
        spectrum_axis(c,MARGIN_X+310,y,210,48,'内插后：产生镜像谱',[(.5,1),(.25,.6),(.75,.6),(.08,.35),(.92,.35)],RED)
        c.setFont('CNB',9); c.setFillColor(RED); c.drawString(MARGIN_X+250,y+15,'L 倍内插')
    doc.y=top-h


def decimation_derivation(doc):
    draw_formula_block(doc,r'x_d(n)=x(nM),\qquad F_d=\frac{F_x}{M},\qquad T_d=MT','dec_time',fontsize=15,max_h=38)
    draw_formula_block(doc,r'X_d(e^{j\omega})=\frac{1}{M}\sum_{i=0}^{M-1}X(e^{j\frac{\omega-2\pi i}{M}})','dec_freq',fontsize=15,max_h=45)
    red_line(doc,'抽取会压缩并叠加频谱；若原信号不先限带，就会产生频谱混叠。')


def decimation_full_derivation(doc):
    """Source pages 406-408: retain the complete frequency-domain derivation."""
    doc.h2('7.2.1 抽取的频域推导')
    doc.p('从抽取序列 x_d(n)=x(nM) 的 DTFT 出发，将每隔 M 点保留一个样本写成 M 个移位频谱的叠加。')
    draw_formula_block(
        doc,
        r'X_d(e^{j\omega})=\sum_{n=-\infty}^{\infty}x(nM)e^{-j\omega n}',
        'dec_full_start', fontsize=15, max_h=38
    )
    draw_formula_block(
        doc,
        r'X_d(e^{j\omega})=\frac{1}{M}\sum_{i=0}^{M-1}X(e^{j\frac{\omega-2\pi i}{M}})',
        'dec_full_result', fontsize=17, max_h=46
    )
    doc.p('因此，抽取后的频谱由原频谱压缩 M 倍后平移叠加得到。各平移分量若相互重叠，就会产生不可逆的混叠。')
    doc.h3('M=2 的特例')
    draw_formula_block(
        doc,
        r'X_d(e^{j\omega})=\frac{1}{2}\left[X(e^{j\frac{\omega}{2}})+X(e^{j(\frac{\omega}{2}-\pi)})\right]',
        'dec_m2_case', fontsize=16, max_h=48
    )
    red_line(doc,'无混叠条件：抽取前应限制原信号带宽，使 |ω|≤π/M。')


def interpolation_derivation(doc):
    draw_formula_block(doc,r'x_p(n)=x(\frac{n}{L}),\quad n=0,\pm L,\pm 2L,\ldots','interp_piece',fontsize=14,max_h=34)
    doc.p('其余整数 n 处取值均为 0。')
    draw_formula_block(doc,r'X_p(e^{j\omega})=X(e^{j\omega L})','interp_freq',fontsize=18,max_h=36)
    red_line(doc,'内插使采样率提高，同时在频域产生 L-1 个镜像谱，必须接低通内插滤波器去除镜像。')


def interpolation_full_derivation(doc):
    """Source pages 417-420: preserve zero-stuffing and spectrum derivation."""
    doc.h2('7.3.1 内插的时域与频域推导')
    doc.p('L 倍内插先在相邻样本之间插入 L-1 个零。插零序列可由冲激序列精确表示为')
    draw_formula_block(
        doc,
        r'x_p(n)=\sum_{k=-\infty}^{\infty}x(k)\delta(n-kL)',
        'interp_impulse_form', fontsize=17, max_h=42
    )
    draw_formula_block(
        doc,
        r'X_p(e^{j\omega})=\sum_{n=-\infty}^{\infty}x_p(n)e^{-j\omega n}'
        r'=\sum_{k=-\infty}^{\infty}x(k)e^{-j\omega kL}=X(e^{j\omega L})',
        'interp_full_result', fontsize=15, max_h=70
    )
    doc.p('频率变量被放大 L 倍，因此在 [-π,π] 内出现 L 个周期性镜像。理想内插低通滤波器保留基带并去除其余镜像。')
    draw_formula_block(
        doc,
        r'H_i(e^{j\omega})=L,\quad 0\leq |\omega|\leq \frac{\pi}{L}',
        'interp_ideal_filter_pass', fontsize=15, max_h=34
    )
    draw_formula_block(
        doc,
        r'H_i(e^{j\omega})=0,\quad \frac{\pi}{L}<|\omega|\leq\pi',
        'interp_ideal_filter_stop', fontsize=15, max_h=34
    )
    red_line(doc,'内插滤波器的通带增益为 L，用于补偿插零造成的幅度缩小。')


def filter_cascade(doc,kind='dec'):
    if kind=='dec':
        system_chain(doc,'抽取滤波器（抗混叠滤波器）与抽取器级联',['h_a(n)\n抗混叠','↓M\n抽取'],[CYAN,YELLOW])
        draw_formula_block(doc,r'H_a(e^{j\omega})=1,\quad 0\leq |\omega|\leq \frac{\pi}{M};\qquad H_a(e^{j\omega})=0,\quad \frac{\pi}{M}\leq |\omega|\leq \pi','anti_alias',fontsize=12,max_h=46)
        draw_formula_block(doc,r'x_d(n)=w(nM)=\sum_{k=-\infty}^{\infty}h_a(k)x(nM-k)','dec_filter_eq',fontsize=13,max_h=40)
        red_line(doc,'作用：消除频谱混叠；截止频率取前述抗混叠截止频率。')
    else:
        system_chain(doc,'内插滤波器（抗镜像滤波器）与内插器级联',['↑L\n内插','h_i(n)\n抗镜像'],[YELLOW,CYAN])
        draw_formula_block(doc,r'H_i(e^{j\omega})=L,\quad 0\leq |\omega|\leq \frac{\pi}{L};\qquad H_i(e^{j\omega})=0,\quad \frac{\pi}{L}\leq |\omega|\leq \pi','anti_image',fontsize=12,max_h=46)
        draw_formula_block(doc,r'h_i(n)=L\frac{\sin\left(\frac{\pi n}{L}\right)}{\pi n}','interp_filter_eq',fontsize=15,max_h=36)
        red_line(doc,'内插滤波器要补偿插零造成的幅度变化，所以通带增益为 L。')


def draw_decimation_filter_example_page(doc):
    """Source pages 414-416: complete M=8 Hanning-window FIR example."""
    doc.new_page()
    doc.h2('7.2.4 例：M=8 抽取滤波器设计')
    doc.p('对输入序列作 8 倍抽取。为避免混叠，先设计截止频率为 π/8 的 40 阶线性相位 FIR 低通滤波器，再进行抽取。')
    draw_formula_block(
        doc,
        r'\omega_c=\frac{\pi}{M}=\frac{\pi}{8},\qquad N-1=40,\qquad '
        r'\tau=\frac{N-1}{2}=20',
        'dec_m8_order_delay', fontsize=17, max_h=45,
    )
    blue_label(doc, '汉宁窗')
    draw_formula_block(
        doc,
        r'w(n)=\left[0.5-0.5\cos\left(\frac{n\pi}{20}\right)\right]R_{41}(n)',
        'dec_m8_hanning_window', fontsize=17, max_h=44,
    )
    blue_label(doc, '理想低通冲激响应平移并加窗')
    draw_formula_block(
        doc,
        r'h(n)=\frac{\sin\left[\frac{\pi}{8}(n-20)\right]}{\pi(n-20)}'
        r'\left[0.5-0.5\cos\left(\frac{n\pi}{20}\right)\right]R_{41}(n)',
        'dec_m8_full_impulse', fontsize=15.5, max_h=62,
    )
    doc.p('滤波器输出每隔 8 点保留一个样本，系统差分方程为')
    draw_formula_block(
        doc,
        r'x_d(n)=\sum_{k=0}^{40}h(k)x(8n-k)',
        'dec_m8_difference_equation', fontsize=18, max_h=42,
    )
    red_line(doc, '先抗混叠滤波，再作 8 倍抽取；40 阶 FIR 的群延迟为 20 个输入采样周期。')


def draw_source_filter_cascade_page(doc):
    """Source page 422: preserve the two different filter/operator orders."""
    doc.new_page()
    doc.h2('7.3.3 抽取滤波器与内插滤波器的级联位置')
    system_chain(doc, 'M 倍抽取：先抗混叠滤波，再抽取', ['h_a(n)\n抗混叠', '↓M\n抽取'], [CYAN, YELLOW])
    draw_formula_block(
        doc,
        r'\omega_{c,a}=\frac{\pi}{M},\qquad x_d(n)=\left[x(n)*h_a(n)\right]_{n=mM}',
        'source_decimation_cascade', fontsize=15, max_h=40,
    )
    system_chain(doc, 'L 倍内插：先插零，再抗镜像滤波', ['↑L\n内插', 'h_i(n)\n抗镜像'], [YELLOW, CYAN])
    draw_formula_block(
        doc,
        r'\omega_{c,i}=\frac{\pi}{L},\qquad x_i(n)=x_p(n)*h_i(n)',
        'source_interpolation_cascade', fontsize=15, max_h=40,
    )
    red_line(doc, '两条级联的顺序不能互换：抽取滤波器位于抽取器之前，内插滤波器位于内插器之后。')


def _rate_circle_colored(c, x, y, label, color):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(1.15)
    c.circle(x, y, 18, stroke=1, fill=0)
    c.setFont('CNB', 10.5)
    c.drawCentredString(x, y - 4, label)


def _dashed_group(c, x, y, w, h, label, color):
    c.saveState()
    c.setStrokeColor(color)
    c.setDash(4, 3)
    c.setLineWidth(1.0)
    c.rect(x, y, w, h, stroke=1, fill=0)
    c.restoreState()
    c.setFillColor(color)
    c.setFont('CNB', 9.2)
    c.drawCentredString(x + w / 2, y + h - 14, label)


def draw_fractional_conversion_source_page(doc):
    """Source page 423: two source subsystems and their combined equivalent."""
    doc.new_page()
    doc.h2('7.4.1 L/M 倍采样率转换的单级结构')
    c = doc.c
    top = doc.y - 12
    y = top - 92
    x0 = MARGIN_X + 18
    up_x, hi_x, hd_x, down_x = x0 + 80, x0 + 138, x0 + 290, x0 + 390

    _dashed_group(c, x0 + 50, y - 39, 205, 92, '内插', RED)
    _dashed_group(c, x0 + 275, y - 39, 190, 92, '抽取', BLUE)
    draw_math_at(c, r'x(n)', x0 - 2, y + 10, 45, 18, 11, name='fractional_source_x')
    arrow(c, x0 + 44, y, up_x - 18, y, RED, 1.1)
    _rate_circle_colored(c, up_x, y, '↑L', RED)
    arrow(c, up_x + 18, y, hi_x, y, RED, 1.1)
    block(c, hi_x, y, 82, 38, '', stroke=RED, fill=LIGHT_YELLOW)
    draw_math_at(c, r'h_i(n)', hi_x + 14, y + 8, 54, 20, 11, name='fractional_hi')
    arrow(c, hi_x + 82, y, hd_x, y, BLUE, 1.1)
    block(c, hd_x, y, 82, 38, '', stroke=BLUE, fill=CYAN)
    draw_math_at(c, r'h_d(n)', hd_x + 14, y + 8, 54, 20, 11, name='fractional_hd')
    arrow(c, hd_x + 82, y, down_x - 18, y, BLUE, 1.1)
    _rate_circle_colored(c, down_x, y, '↓M', BLUE)
    arrow(c, down_x + 18, y, down_x + 58, y, BLUE, 1.1)
    draw_math_at(c, r'x_d(n)', down_x + 62, y + 10, 52, 18, 11, name='fractional_source_y')

    doc.y = y - 62
    draw_formula_block(doc, r'h(n)=h_i(n)*h_d(n)', 'fractional_time_product', fontsize=16, max_h=36)
    draw_formula_block(doc, r'H(e^{j\omega})=H_i(e^{j\omega})H_d(e^{j\omega})', 'fractional_freq_product', fontsize=16, max_h=36)

    c = doc.c
    y2 = doc.y - 52
    ex0 = MARGIN_X + 108
    draw_math_at(c, r'x(n)', ex0 - 62, y2 + 8, 44, 18, 11, name='fractional_eq_x')
    arrow(c, ex0 - 18, y2, ex0, y2, RED, 1.1)
    _rate_circle_colored(c, ex0 + 18, y2, '↑L', RED)
    arrow(c, ex0 + 36, y2, ex0 + 72, y2, RED, 1.1)
    block(c, ex0 + 72, y2, 84, 38, '', stroke=RED, fill=LIGHT_YELLOW)
    draw_math_at(c, r'h(n)', ex0 + 90, y2 + 8, 48, 20, 11, name='fractional_h')
    arrow(c, ex0 + 156, y2, ex0 + 198, y2, BLUE, 1.1)
    _rate_circle_colored(c, ex0 + 216, y2, '↓M', BLUE)
    arrow(c, ex0 + 234, y2, ex0 + 278, y2, BLUE, 1.1)
    draw_math_at(c, r'x_d(n)', ex0 + 282, y2 + 8, 52, 18, 11, name='fractional_eq_y')
    doc.y = y2 - 48
    draw_formula_block(
        doc,
        r'H(e^{j\omega})=L,\quad |\omega|\leq\omega_c;\qquad '
        r'H(e^{j\omega})=0,\quad \omega_c<|\omega|\leq\pi',
        'fractional_source_filter', fontsize=14.5, max_h=48,
    )
    draw_formula_block(doc, r'\omega_c=\min\left(\frac{\pi}{L},\frac{\pi}{M}\right)',
                       'fractional_source_cutoff', fontsize=19, max_h=42)


def multistage_source_geometry():
    return {
        'group_count': 2,
        'first_group_x': MARGIN_X + 94,
        'second_group_x': MARGIN_X + 292,
        'group_width': 168,
        'right_edge': MARGIN_X + 460,
    }


def _draw_multistage_group(c, x, y, suffix):
    _dashed_group(c, x - 12, y - 43, 168, 86, '', RED)
    _rate_circle_colored(c, x + 15, y, f'↑L{suffix}', RED)
    arrow(c, x + 33, y, x + 54, y, RED, 1.0)
    block(c, x + 54, y, 56, 36, '', stroke=RED, fill=LIGHT_YELLOW)
    draw_math_at(c, fr'h_{suffix}(n)', x + 61, y + 7, 42, 18, 10, name=f'multistage_h_{suffix}')
    arrow(c, x + 110, y, x + 122, y, RED, 1.0)
    _rate_circle_colored(c, x + 140, y, f'↓M{suffix}', RED)


def draw_multistage_factorization_page(doc):
    """Source pages 427 and 431-432: exact first/last-stage topology plus DAT example."""
    doc.new_page()
    doc.h2('7.4.2 多级采样率转换')
    draw_formula_block(doc, r'\frac{L}{M}=\prod_{i=1}^{r}\frac{L_i}{M_i}',
                       'multistage_source_ratio', fontsize=19, max_h=42)
    draw_formula_block(doc, r'\frac{147}{160}=\frac{7}{8}\cdot\frac{7}{5}\cdot\frac{3}{4}',
                       'multistage_source_factorization', fontsize=17, max_h=38)
    doc.p('当 L 或 M 很大时，单级低通滤波器的截止频率很小、实现代价很高；可分解为多级采样率转换系统。')
    geometry = multistage_source_geometry()
    c = doc.c
    y = doc.y - 65
    draw_math_at(c, r'x(n)', MARGIN_X + 18, y + 8, 42, 18, 11, name='multistage_x')
    arrow(c, MARGIN_X + 62, y, geometry['first_group_x'] - 12, y, RED, 1.0)
    for i in range(2):
        gx = geometry['first_group_x'] if i == 0 else geometry['second_group_x']
        suffix = '1' if i == 0 else 'r'
        _draw_multistage_group(c, gx, y, suffix)
    arrow(c, geometry['first_group_x'] + 158, y, geometry['first_group_x'] + 174, y, RED, 1.0)
    c.setFillColor(TEXT)
    c.setFont('CNB', 12)
    c.drawCentredString(geometry['first_group_x'] + 184, y - 3, '...')
    arrow(c, geometry['first_group_x'] + 194, y, geometry['second_group_x'] - 12, y, RED, 1.0)
    arrow(c, geometry['right_edge'], y, geometry['right_edge'] + 20, y, RED, 1.0)
    draw_math_at(c, r'x_d(n)', geometry['right_edge'] + 2, y + 24, 45, 18, 11, name='multistage_y')
    doc.y = y - 68
    red_line(doc, '每一级均按“内插、滤波、抽取”连接；各级因子的乘积分别等于总 L 和总 M。')

    doc.new_page()
    doc.h2('例：DAT 44.1 kHz 转换为 48 kHz')
    doc.p('数字录音带（DAT）驱动器的采样频率为 48 kHz，而激光唱盘（CD）播放器以 44.1 kHz 工作。为把声音从 CD 录制到 DAT，画出单级转换系统，并求 L、M 的最小可能值以及适当的滤波器。')
    draw_dat_conversion_chain(doc)
    draw_formula_block(doc, r'\frac{48000}{44100}=\frac{160}{147}=\frac{2^5\cdot5}{3\cdot7^2}',
                       'dat_source_ratio', fontsize=18, max_h=44)
    draw_formula_block(doc, r'L=160,\qquad M=147', 'dat_source_factors', fontsize=18, max_h=36)
    draw_formula_block(doc, r'\omega_c=\min\left(\frac{\pi}{L},\frac{\pi}{M}\right)=\frac{\pi}{160}',
                       'dat_source_cutoff', fontsize=17, max_h=40)
    red_line(doc, '单级结构的最小整数因子为 L=160、M=147；实际实现通常再分解为多级以降低运算量。')


def lm_conversion(doc):
    h=200; doc.ensure(h+8); c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK)
    draw_auto_math_text(c,MARGIN_X,top-6,'L/M 倍采样率转换结构',font='CNB',size=10,color=BLUE_DARK)
    x=MARGIN_X+35; y=top-70
    draw_math_at(c,r'x(n)',x-35,y+7,35,16,11,name='lm_x')
    for i,lab in enumerate(['↑L','h(n)','↓M']):
        bx=x+i*105
        arrow(c,bx-28 if i==0 else bx-25,y,bx,y,BLUE,1.1)
        block(c,bx,y,60,32,lab,stroke=BLUE,fill=YELLOW if i!=1 else CYAN)
    arrow(c,x+2*105+60,y,x+2*105+105,y,BLUE,1.1)
    draw_math_at(c,r'x_d(n)',x+2*105+112,y+7,48,16,11,name='lm_y')
    doc.y=top-116
    draw_formula_block(doc,r'H(e^{j\omega})=L,\quad |\omega|\leq \omega_c;\qquad H(e^{j\omega})=0,\quad \omega_c<|\omega|\leq \pi,\qquad \omega_c=\min\left(\frac{\pi}{L},\frac{\pi}{M}\right)','lm_filter',fontsize=12,max_h=50)
    doc.y=top-h


def multistage(doc):
    h=175; doc.ensure(h+8); c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-6,'多级采样率变换')
    doc.y = top - 24
    draw_formula_block(doc,r'\frac{F_2}{F_1}=\frac{L}{M}=\prod_i\frac{L_i}{M_i},\qquad \omega_c=\min\left(\frac{\pi}{L},\frac{\pi}{M}\right)','multi_ratio',fontsize=14,max_h=45)
    c.setFont('CN',9); c.setFillColor(TEXT)
    c.drawString(MARGIN_X,doc.y,'当 L 或 M 很大时，单级滤波器代价高；分解为多级后，每级过渡带可放宽，计算量明显降低。')
    doc.y -= 18
    draw_formula_block(doc,r'44100\to48000:\quad \frac{48000}{44100}=\frac{160}{147}=\frac{2^5\cdot5}{3\cdot7^2}','audio_ratio',fontsize=14,max_h=38)
    doc.y=top-h


def _figure_page(doc, title):
    """Reserve a full A4 content page for one source-slide figure group."""
    doc.ensure(690)
    doc.h2(title)
    return doc.c, doc.y - 10


def _stem_envelope(c, x, y, w, h, sample_count, keep_every=1, label=''):
    """Source-style red discrete samples under a dotted smooth envelope."""
    c.setStrokeColor(BLUE_DARK)
    c.setFillColor(BLUE_DARK)
    c.setLineWidth(0.8)
    arrow(c, x, y, x + w, y, BLUE_DARK, 0.8)
    arrow(c, x, y - 5, x, y + h + 8, BLUE_DARK, 0.8)
    points = []
    for i in range(sample_count):
        u = i / max(1, sample_count - 1)
        amp = h * (0.28 + 0.68 * math.sin(math.pi * u) ** 0.8)
        points.append((x + 8 + u * (w - 18), y + amp))
    c.setStrokeColor(RED)
    c.setFillColor(RED)
    c.setLineWidth(0.85)
    for i, (px, py) in enumerate(points):
        if i % keep_every:
            continue
        c.line(px, y, px, py)
        c.circle(px, py, 1.7, stroke=0, fill=1)
    c.setDash(2, 2)
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        c.line(x1, y1, x2, y2)
    c.setDash()
    if label:
        draw_auto_math_text(
            c, x + 3, y + h + 14, label, font='CNB', size=8.5,
            color=TEXT, math_size=10.5, math_height=14,
        )


def _draw_spectrum_title(c, x, y, w, h, title):
    if not title:
        return
    draw_auto_math_text(
        c, x + 3, y + h + 14, title, font='CNB', size=8.4,
        color=TEXT, math_size=10.5, math_height=14,
    )


def _triangle_spectrum(c, x, y, w, h, centers, half_width, labels=(), title=''):
    """Draw the periodic triangular spectra used on source pages 409-412."""
    c.setStrokeColor(BLUE_DARK)
    c.setFillColor(BLUE_DARK)
    c.setLineWidth(0.8)
    arrow(c, x, y, x + w, y, BLUE_DARK, 0.8)
    arrow(c, x + w / 2, y - 4, x + w / 2, y + h + 8, BLUE_DARK, 0.8)
    c.setStrokeColor(RED)
    c.setLineWidth(1.1)
    for center, amp in centers:
        cx = x + w / 2 + center * w
        hw = half_width * w
        c.line(cx - hw, y, cx, y + h * amp)
        c.line(cx, y + h * amp, cx + hw, y)
    for rel, text in labels:
        draw_auto_math_text(
            c, x + w / 2 + rel * w, y - 12, text,
            font='CN', size=7.2, color=TEXT, align='center',
            math_size=9.3, math_height=13,
        )
    _draw_spectrum_title(c, x, y, w, h, title)


def draw_decimation_sampling_theorem_page(doc):
    """Recreate source page 409: M=2 sampling and spectrum correspondence."""
    c, top = _figure_page(doc, '7.2.2 用图示采样定理理解整数倍抽取')
    draw_formula_block(doc, r'x_d(n)=x(nM),\quad M=2', 'dec_graph_m2', fontsize=16, max_h=34)
    top = doc.y - 8
    left = MARGIN_X + 12
    right = MARGIN_X + 292
    row_gap = 190

    _stem_envelope(c, left, top - 80, 225, 62, 19, keep_every=1, label=r'x(n)')
    draw_math_at(c, r'f_{s1}=16\,\mathrm{kHz}', left + 62, top - 94, 110, 18, 10.5, name='dec_fs16')
    _triangle_spectrum(
        c, right, top - 80, 235, 62,
        [(-0.42, .72), (0, 1), (.42, .72)], .10,
        [(-.42, '-16'), (-.10, '-4'), (0, '0'), (.10, '4'), (.42, '16')],
        title=r'X_1(jf)',
    )

    _stem_envelope(c, left, top - row_gap - 80, 225, 62, 19, keep_every=2, label=r'x_d(n)=x(nM)')
    draw_math_at(c, r'f_{s2}=8\,\mathrm{kHz}', left + 68, top - row_gap - 94, 105, 18, 10.5, name='dec_fs8')
    _triangle_spectrum(
        c, right, top - row_gap - 80, 235, 62,
        [(-.42, .70), (-.21, .42), (0, 1), (.21, .42), (.42, .70)], .13,
        [(-.42, '-8'), (-.21, '-4'), (0, '0'), (.21, '4'), (.42, '8')],
        title=r'X_2(jf)',
    )

    c.setFillColor(RED)
    c.setFont('CNB', 9.2)
    c.drawString(MARGIN_X + 25, top - 405, '抽取后采样率减半，频谱副本间隔也减半；若副本相交就会发生混叠。')
    doc.y = 78


def draw_decimation_spectral_construction_page(doc):
    """Recreate source pages 410-412: stretch, shift, sum and no-alias condition."""
    c, top = _figure_page(doc, '7.2.3 抽取频谱的拉伸、移位与求和')
    draw_formula_block(
        doc,
        r'X_d(e^{j\omega})=\frac{1}{2}\left[X_1(e^{j\omega})+X_1(e^{j(\omega-\pi)})\right]',
        'dec_shift_sum_formula', fontsize=16, max_h=40,
    )
    top = doc.y - 12
    panel_w = 225
    panel_h = 62
    left = MARGIN_X + 18
    right = MARGIN_X + 296
    rows = [top - 75, top - 245, top - 415]

    _triangle_spectrum(c, left, rows[0], panel_w, panel_h, [(0, 1), (-.38, .72), (.38, .72)], .12,
                       [(-.38, '-2π'), (-.12, '-π/2'), (0, '0'), (.12, 'π/2'), (.38, '2π')], title=r'X_1(e^{j\omega})')
    _triangle_spectrum(c, right, rows[0], panel_w, panel_h, [(0, 1), (-.30, .72), (.30, .72)], .18,
                       [(-.30, '-2π'), (0, '0'), (.30, '2π')], title='频率轴拉伸')

    _triangle_spectrum(c, left, rows[1], panel_w, panel_h, [(0, 1), (-.30, .72), (.30, .72)], .18,
                       [(-.30, '-2π'), (0, '0'), (.30, '2π')], title=r'X_1(e^{j\omega})')
    _triangle_spectrum(c, right, rows[1], panel_w, panel_h,
                       [(0, 1), (-.30, .72), (.30, .72), (-.15, .68), (.15, .68)], .14,
                       [(-.30, '-2π'), (-.15, '-π'), (0, '0'), (.15, 'π'), (.30, '2π')], title='频移 π 后的频谱')

    _triangle_spectrum(c, left, rows[2], panel_w, panel_h,
                       [(0, .62), (-.30, .46), (.30, .46), (-.15, .44), (.15, .44)], .14,
                       [(-.30, '-2π'), (-.15, '-π'), (0, '0'), (.15, 'π'), (.30, '2π')], title='求和并乘以 1/2')
    draw_math_at(
        c,
        r'\frac{1}{2}\left[X_1(e^{j\omega})+X_1(e^{j(\omega-\pi)})\right]',
        right + 8, rows[2] + 30, 210, 32, 12.5, name='dec_shift_sum_result',
    )
    c.setFillColor(RED)
    c.setFont('CNB', 9.2)
    draw_auto_math_text(c,MARGIN_X+30,top-520,'无混叠条件：抽取前原序列必须限带到 |ω|≤π/M。',font='CNB',size=9.2,color=RED)
    doc.y = 78


def draw_interpolation_sampling_theorem_page(doc):
    """Recreate source pages 419-421: zero stuffing, mirror spectra and filtering."""
    c, top = _figure_page(doc, '7.3.2 L=2 内插的插零、镜像频谱与抗镜像滤波')
    draw_formula_block(doc, r'X_p(e^{j\omega})=X(e^{j2\omega}),\qquad L=2', 'interp_graph_l2', fontsize=16, max_h=36)
    top = doc.y - 8
    left = MARGIN_X + 12
    right = MARGIN_X + 292
    row_gap = 178

    _stem_envelope(c, left, top - 72, 225, 58, 13, keep_every=1, label=r'x(n)')
    draw_math_at(c, r'f_{s1}=8\,\mathrm{kHz}', left + 64, top - 88, 105, 18, 10.5, name='interp_fs8')
    _triangle_spectrum(c, right, top - 72, 235, 58,
                       [(-.38, .70), (0, 1), (.38, .70)], .13,
                       [(-.38, '-2π'), (-.10, '-π/2'), (0, '0'), (.10, 'π/2'), (.38, '2π')], title=r'X(e^{j\omega})')

    _stem_envelope(c, left, top - row_gap - 72, 225, 58, 25, keep_every=2, label=r'x_p(n)')
    draw_math_at(c, r'f_{s2}=16\,\mathrm{kHz}', left + 62, top - row_gap - 88, 110, 18, 10.5, name='interp_fs16')
    _triangle_spectrum(c, right, top - row_gap - 72, 235, 58,
                       [(-.38, .68), (-.19, .68), (0, 1), (.19, .68), (.38, .68)], .095,
                       [(-.38, '-2π'), (-.19, '-π'), (0, '0'), (.19, 'π'), (.38, '2π')], title=r'X_p(e^{j\omega})=X(e^{j2\omega})')

    _stem_envelope(c, left, top - 2 * row_gap - 72, 225, 58, 25, keep_every=1, label=r'x_i(n)')
    _triangle_spectrum(c, right, top - 2 * row_gap - 72, 235, 58,
                       [(0, 1), (-.38, .65), (.38, .65)], .10,
                       [(-.38, '-2π'), (-.10, '-π/2'), (0, '0'), (.10, 'π/2'), (.38, '2π')], title='抗镜像滤波后')
    draw_math_at(c, r'H_i(e^{j\omega})', right + 72, top - 2 * row_gap - 106, 90, 20, 11, name='interp_hi_label')
    c.setFillColor(RED)
    c.setFont('CNB', 9.2)
    c.drawString(MARGIN_X + 25, top - 520, '插零使频谱出现 L-1 个镜像；理想低通滤波器保留基带并补偿幅度。')
    doc.y = 78


def fractional_conversion_details(doc):
    """Source pages 423-432: single-stage order and multistage factorization."""
    doc.h2('7.4.1 单级与多级采样率转换')
    doc.p('L/M 倍采样率转换必须按“先内插、再滤波、最后抽取”的顺序连接。中间低通滤波器同时承担抗镜像和抗混叠作用。')
    draw_formula_block(
        doc,
        r'\omega_c=\min\left(\frac{\pi}{L},\frac{\pi}{M}\right)',
        'fractional_cutoff', fontsize=18, max_h=38
    )
    doc.h3('32 kHz 转换为 48 kHz')
    draw_formula_block(
        doc,
        r'\frac{48}{32}=\frac{3}{2}\quad\Rightarrow\quad L=3,\ M=2',
        'fractional_32_48', fontsize=18, max_h=40
    )
    doc.p('先作 3 倍内插，再通过截止频率为下式的低通滤波器，最后作 2 倍抽取。')
    draw_formula_block(
        doc,
        r'\omega_c=\min\left(\frac{\pi}{3},\frac{\pi}{2}\right)=\frac{\pi}{3}',
        'fractional_32_48_cutoff', fontsize=14, max_h=32
    )
    doc.h3('44.1 kHz 转换为 48 kHz')
    draw_formula_block(
        doc,
        r'\frac{48000}{44100}=\frac{160}{147}=\frac{2^5\cdot5}{3\cdot7^2}',
        'fractional_441_48', fontsize=18, max_h=42
    )
    doc.p('当 L 和 M 较大时，将该采样率比分解成若干小整数级联，可放宽各级过渡带并降低总计算量。')
    red_line(doc,'多级分解时，各级因子的乘积必须分别等于总内插因子 L 和总抽取因子 M。')


def _rate_circle(c, x, y, label):
    c.setStrokeColor(RED)
    c.setFillColor(RED)
    c.setLineWidth(1.15)
    c.circle(x, y, 17, stroke=1, fill=0)
    c.setFont('CNB', 10.5)
    c.drawCentredString(x, y - 4, label)


def _delay_mark(c, x, y, name):
    draw_math_at(c, r'z^{-1}', x, y, 34, 15, 10.2, name=name)


def _draw_green_transmission_arrow(c, x, y, direction='horizontal'):
    c.saveState()
    c.setStrokeColor(GREEN)
    c.setFillColor(LIGHT_YELLOW)
    c.setLineWidth(1.25)
    p = c.beginPath()
    if direction == 'vertical':
        p.moveTo(x - 13, y - 26)
        p.lineTo(x + 13, y - 26)
        p.lineTo(x + 13, y + 7)
        p.lineTo(x + 22, y + 7)
        p.lineTo(x, y + 30)
        p.lineTo(x - 22, y + 7)
        p.lineTo(x - 13, y + 7)
        p.close()
        c.drawPath(p, stroke=1, fill=1)
        draw_centered_multiline_text(c, x, y - 7, '数据\n传输', 'CNB', 7.8, leading=10, color=TEXT)
    else:
        width, height = 94, 32
        p.moveTo(x, y - height / 2)
        p.lineTo(x + width - 19, y - height / 2)
        p.lineTo(x + width - 19, y - height / 2 - 7)
        p.lineTo(x + width, y)
        p.lineTo(x + width - 19, y + height / 2 + 7)
        p.lineTo(x + width - 19, y + height / 2)
        p.lineTo(x, y + height / 2)
        p.close()
        c.drawPath(p, stroke=1, fill=1)
        c.setFillColor(TEXT)
        c.setFont('CNB', 8.4)
        c.drawCentredString(x + 40, y - 3, '数据传输')
    c.restoreState()


def tdm_source_geometry():
    return {
        'input_x': MARGIN_X + 20,
        'rate_x': MARGIN_X + 138,
        'left_bus': MARGIN_X + 252,
        'data_x': MARGIN_X + 260,
        'right_bus': MARGIN_X + 320,
        'out_rate_x': MARGIN_X + 400,
        'output_label_end': MARGIN_X + 514,
    }


def fdm_source_geometry():
    return {
        'input_x': MARGIN_X + 28,
        'rate_x': MARGIN_X + 132,
        'filter_x': MARGIN_X + 198,
        'bus_x': MARGIN_X + 330,
        'left_spectrum_x': MARGIN_X + 22,
        'middle_spectrum_x': MARGIN_X + 205,
        'right_spectrum_x': MARGIN_X + 372,
        'right_spectrum_end': MARGIN_X + 490,
    }


def draw_tdm_source_topology(doc):
    doc.new_page()
    doc.h2('7.4.3 多采样率系统的应用 - 时分复用（TDM）')
    c = doc.c
    y3, y2, y1 = doc.y - 70, doc.y - 140, doc.y - 210
    geometry = tdm_source_geometry()
    input_x, rate_x, left_bus = geometry['input_x'], geometry['rate_x'], geometry['left_bus']
    right_bus, out_rate_x = geometry['right_bus'], geometry['out_rate_x']

    for idx, (row_y, subscript) in enumerate(((y3, 3), (y2, 2), (y1, 1))):
        draw_math_at(c, fr'x_{subscript}(n)', input_x, row_y + 7, 56, 20, 12, name=f'tdm_in_x{subscript}')
        arrow(c, input_x + 60, row_y, rate_x - 17, row_y, RED, 1.1)
        _rate_circle(c, rate_x, row_y, '↑3')
        arrow(c, rate_x + 17, row_y, left_bus, row_y, RED, 1.1)

    # Source page 428: each upper branch is delayed before joining the next row.
    c.setStrokeColor(RED)
    c.setLineWidth(1.15)
    arrow(c, left_bus, y3, left_bus, y2, RED, 1.1)
    arrow(c, left_bus, y2, left_bus, y1, RED, 1.1)
    _delay_mark(c, left_bus - 42, (y3 + y2) / 2, 'tdm_tx_delay_1')
    _delay_mark(c, left_bus - 42, (y2 + y1) / 2, 'tdm_tx_delay_2')
    arrow(c, left_bus, y1, left_bus + 42, y1, RED, 1.1)
    draw_math_at(c, r'y(n)', left_bus + 44, y1 + 8, 38, 18, 11, name='tdm_serial_y')

    # The source depicts transmission as an annotation between two independent chains.
    data_x = geometry['data_x'] + 28
    _draw_green_transmission_arrow(c, data_x, y2, direction='vertical')
    arrow(c, right_bus - 42, y3, right_bus, y3, RED, 1.1)
    draw_math_at(c, r'y(n)', right_bus - 40, y3 + 22, 38, 18, 11, name='tdm_rx_y')

    # Receive side: two z^-1 delays feed the three ↓3 phase branches.
    arrow(c, right_bus, y3, right_bus, y2, RED, 1.1)
    arrow(c, right_bus, y2, right_bus, y1, RED, 1.1)
    _delay_mark(c, right_bus + 8, (y3 + y2) / 2, 'tdm_rx_delay_1')
    _delay_mark(c, right_bus + 8, (y2 + y1) / 2, 'tdm_rx_delay_2')
    for row_y, subscript in ((y3, 1), (y2, 2), (y1, 3)):
        arrow(c, right_bus, row_y, out_rate_x - 17, row_y, RED, 1.1)
        _rate_circle(c, out_rate_x, row_y, '↓3')
        arrow(c, out_rate_x + 17, row_y, out_rate_x + 58, row_y, RED, 1.1)
        draw_math_at(c, fr'x_{subscript}(n)', out_rate_x + 62, row_y + 7, 52, 20, 12, name=f'tdm_out_x{subscript}')

    doc.y = y1 - 65
    draw_formula_block(
        doc,
        r'y(n)=\{\ldots,x_1(0),x_2(0),x_3(0),x_1(1),x_2(1),x_3(1),\ldots\}',
        'tdm_serial_sequence', fontsize=13.5, max_h=34, gap=7,
    )
    doc.p('三路序列经不同延时后按时间交织为一路串行序列；接收端用相同延时链和三个相位支路分离。')


def _fdm_mini_spectrum(c, x, y, w, h, expr, kind):
    if kind in ('u1', 'u2', 'u3'):
        c.saveState()
        c.setFillColor(CYAN)
        if kind == 'u1':
            _fill_band(c, x + w * .18, y, w * .64, h)
        elif kind == 'u2':
            _fill_band(c, x, y, w * .24, h)
            _fill_band(c, x + w * .76, y, w * .24, h)
        else:
            _fill_band(c, x, y, w * .56, h)
        c.restoreState()
    c.setStrokeColor(BLACK)
    c.setFillColor(BLACK)
    c.setLineWidth(0.8)
    arrow(c, x, y, x + w, y, BLACK, 0.8)
    arrow(c, x, y - 3, x, y + h, BLACK, 0.8)
    draw_math_at(c, expr, x + 2, y + h + 9, w * 0.72, 15, 9.5, name='fdm_spec_' + kind)
    c.setStrokeColor(RED)
    c.setLineWidth(1.05)
    if kind in ('x1', 'u1'):
        pts = [(0, 0), (.42, .70), (1, 0)]
    elif kind in ('x2', 'u2'):
        pts = [(0, 0), (.50, .72), (1, 0)]
    elif kind in ('x3', 'u3'):
        pts = [(0, .72), (.50, 0), (1, .72)]
    else:
        pts = [(0, 0), (.18, .65), (.36, 0), (.54, .65), (.72, 0), (.90, .65), (1, 0)]
    p = c.beginPath()
    p.moveTo(x + pts[0][0] * w, y + pts[0][1] * h)
    for px, py in pts[1:]:
        p.lineTo(x + px * w, y + py * h)
    c.drawPath(p, stroke=1, fill=0)
    c.setFillColor(TEXT)
    c.setFont('CN', 7.2)
    c.drawString(x - 4, y - 12, '0')
    c.drawRightString(x + w, y - 12, '2π')
    c.drawString(x + w + 4, y - 2, 'ω')


def draw_fdm_source_topology(doc):
    doc.new_page()
    doc.h2('7.4.3 多采样率系统的应用 - 频分复用（FDM）')
    c = doc.c
    rows = [doc.y - 58, doc.y - 116, doc.y - 174]
    geometry = fdm_source_geometry()
    input_x, rate_x, filter_x, bus_x = geometry['input_x'], geometry['rate_x'], geometry['filter_x'], geometry['bus_x']
    filter_exprs = (r'\mathrm{LP\ DF}\quad G_1(z)', r'\mathrm{BP\ DF}\quad G_2(z)', r'\mathrm{HP\ DF}\quad G_3(z)')
    for i, row_y in enumerate(rows, start=1):
        draw_math_at(c, fr'x_{i}(n)', input_x, row_y + 7, 52, 19, 11.5, name=f'fdm_input_{i}')
        arrow(c, input_x + 58, row_y, rate_x - 17, row_y, RED, 1.1)
        _rate_circle(c, rate_x, row_y, '↑3')
        arrow(c, rate_x + 17, row_y, filter_x, row_y, RED, 1.1)
        block(c, filter_x, row_y, 94, 42, '', stroke=RED, fill=None)
        draw_math_at(c, filter_exprs[i - 1], filter_x + 8, row_y + 1, 78, 29, 10.5, name=f'fdm_filter_{i}')
        arrow(c, filter_x + 94, row_y, bus_x, row_y, RED, 1.1)

    c.setStrokeColor(RED)
    c.setLineWidth(1.15)
    c.line(bus_x, rows[0], bus_x, rows[2])
    arrow(c, bus_x, rows[2], bus_x + 42, rows[2], RED, 1.1)
    draw_math_at(c, r'y(n)', bus_x + 46, rows[2] + 12, 38, 18, 11, name='fdm_output_y')
    _draw_green_transmission_arrow(c, bus_x + 78, rows[2], direction='horizontal')

    panel_y = doc.y - 330
    left, middle, right = geometry['left_spectrum_x'], geometry['middle_spectrum_x'], geometry['right_spectrum_x']
    for i, expr in enumerate((r'X_1(e^{j\omega})', r'X_2(e^{j\omega})', r'X_3(e^{j\omega})')):
        _fdm_mini_spectrum(c, left, panel_y - i * 86, 118, 42, expr, f'x{i + 1}')
        _fdm_mini_spectrum(c, middle, panel_y - i * 86, 118, 42, expr.replace('e^{j\\omega}', 'e^{j3\\omega}'), f'u{i + 1}')
    _fdm_mini_spectrum(c, right, panel_y - 86, 118, 42, r'Y(e^{j\omega})', 'y')
    c.setFillColor(RED)
    c.setFont('CNB', 9.2)
    c.drawString(MARGIN_X + 24, panel_y - 278, '三路频谱分别配置到低频、中频和高频子带后，在公共汇流线上合成。')
    doc.y = 75


def _fill_band(c, x, y, w, h):
    c.rect(x, y, w, h, stroke=0, fill=1)


def draw_tdm_fdm_definition_page(doc):
    doc.new_page()
    doc.h2('时分复用与频分复用的基本概念')
    red_line(doc, '时分复用（TDM）是一种将多个数据流在同一个通信介质上同时进行传输的方法。其基本原理是通过时间轴的切割，使得每个数据流在一定时间内占据全部传输资源。')
    c = doc.c
    top = doc.y - 18
    input_x = MARGIN_X + 36
    mux_x = MARGIN_X + 176
    slot_x = MARGIN_X + 252
    demux_x = MARGIN_X + 398
    output_x = MARGIN_X + 514
    colors_slots = (colors.HexColor('#BDE7FF'), colors.HexColor('#A9D9FF'), colors.HexColor('#8CCBFF'), colors.HexColor('#73BAF2'))
    rows = [top - i * 28 for i in range(4)]
    for i, (row_y, label) in enumerate(zip(rows, ('A', 'B', 'C', 'D'))):
        c.setFillColor(TEXT)
        c.setFont('CNB', 8.8)
        c.drawCentredString(input_x, row_y - 3, label)
        arrow(c, input_x + 12, row_y, mux_x - 10, top - 42, BLACK, .8)
        c.drawCentredString(output_x, row_y - 3, label)
        arrow(c, demux_x + 10, top - 42, output_x - 12, row_y, BLACK, .8)
    c.setStrokeColor(BLACK)
    c.setFillColor(colors.white)
    c.circle(mux_x, top - 42, 13, stroke=1, fill=1)
    c.circle(demux_x, top - 42, 13, stroke=1, fill=1)
    c.setFont('CNB', 7.5)
    c.setFillColor(TEXT)
    c.drawCentredString(mux_x, top - 45, '复用')
    c.drawCentredString(demux_x, top - 45, '分离')
    arrow(c, mux_x + 14, top - 42, slot_x, top - 42, BLACK, .9)
    slot_w = 25
    for i, fill in enumerate(colors_slots):
        c.setFillColor(fill)
        c.setStrokeColor(BLACK)
        c.rect(slot_x + i * slot_w, top - 53, slot_w, 22, stroke=1, fill=1)
        c.setFillColor(TEXT)
        c.setFont('CNB', 7.8)
        c.drawCentredString(slot_x + i * slot_w + slot_w / 2, top - 46, str(i + 1))
    arrow(c, slot_x + 4 * slot_w, top - 42, demux_x - 14, top - 42, BLACK, .9)
    c.setFillColor(TEXT)
    c.setFont('CN', 8.3)
    c.drawCentredString(slot_x + 2 * slot_w, top - 72, '同一传输通道中的连续时隙')
    doc.y = top - 112
    doc.p('频分复用（FDM）是将用于传输信道的总带宽划分成若干个子频带（或称子信道），每一个子信道传输一路信号。')
    red_line(doc, '频分复用的所有用户在同一时间占用不同的带宽资源（频率）。')


def tdm_fdm(doc):
    draw_tdm_source_topology(doc)
    draw_fdm_source_topology(doc)
    draw_tdm_fdm_definition_page(doc)


def triangle_spectrum(c, x, y, w, h, label, half_band='π/3', peaks=(0.5,)):
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.9)
    arrow(c, x, y, x + w, y, BLACK, 0.9)
    c.setFillColor(TEXT)
    c.setFont('CN', 7.5)
    c.drawString(x + w + 3, y - 2, 'ω')
    draw_auto_math_text(
        c, x + w / 2, y - 26, label, font='CN', size=7.5,
        color=TEXT, align='center', math_size=10, math_height=14,
    )
    for peak in peaks:
        center = x + w * peak
        half = w * 0.11
        c.line(center - half, y, center, y + h)
        c.line(center, y + h, center + half, y)
    center = x + w / 2
    draw_auto_math_text(
        c, center - w * 0.11, y - 13, '-' + half_band,
        font='CN', size=7.5, color=TEXT, align='center',
        math_size=9.5, math_height=13,
    )
    draw_auto_math_text(c, center, y - 13, '0', font='CN', size=7.5, color=TEXT, align='center')
    draw_auto_math_text(
        c, center + w * 0.11, y - 13, half_band,
        font='CN', size=7.5, color=TEXT, align='center',
        math_size=9.5, math_height=13,
    )


def draw_up2_filter_down2_spectra_page(doc):
    """Source page 426: retain all four spectra in the ↑2/filter/↓2 example."""
    doc.new_page()
    doc.h2('例 3  ↑2、低通滤波器与 ↓2 的等效系统')
    system_chain(doc, '原课件系统框图', ['↑2', '低通滤波器\nωc=π/4，增益2', '↓2'], [YELLOW, CYAN, YELLOW])
    c = doc.c
    top = doc.y - 12
    left = MARGIN_X + 32
    right = MARGIN_X + 302
    row1 = top - 78
    row2 = top - 255
    panel_w, panel_h = 220, 58
    _triangle_spectrum(
        c, left, row1, panel_w, panel_h,
        [(0, 1), (-.40, .72), (.40, .72)], .12,
        [(-.40, '-2π'), (-.12, '-π/2'), (0, '0'), (.12, 'π/2'), (.40, '2π')],
        title='原信号频谱',
    )
    _triangle_spectrum(
        c, right, row1, panel_w, panel_h,
        [(0, 1), (-.20, .82), (.20, .82), (-.40, .62), (.40, .62)], .09,
        [(-.40, '-2π'), (-.20, '-π'), (0, '0'), (.20, 'π'), (.40, '2π')],
        title='插零后频谱',
    )
    _triangle_spectrum(
        c, left, row2, panel_w, panel_h,
        [(0, 1), (-.40, .62), (.40, .62)], .08,
        [(-.40, '-2π'), (-.10, '-π/4'), (0, '0'), (.10, 'π/4'), (.40, '2π')],
        title='低通后频谱',
    )
    _triangle_spectrum(
        c, right, row2, panel_w, panel_h,
        [(0, 1), (-.40, .72), (.40, .72)], .12,
        [(-.40, '-2π'), (-.12, '-π/2'), (0, '0'), (.12, 'π/2'), (.40, '2π')],
        title='抽取后频谱',
    )
    c.setFillColor(RED)
    c.setFont('CNB', 9.2)
    draw_auto_math_text(c,MARGIN_X+38,top-395,'等效系统：截止频率为 π/2，增益为 1 的低通滤波器。',font='CNB',size=9.2,color=RED)
    doc.y = 78


def source_exercises_and_answers(doc):
    """Source pages 424-436: examples, review questions, and supplied answers."""
    doc.h2('本章原课件例题与课后题')
    doc.h3('例 1  分数倍采样率转换的操作顺序')
    doc.p('若实现序列的 L/M 倍采样率转换，一般先对信号做什么操作，然后再做什么操作？')
    red_line(doc, '答案：先插值，再抽取。中间必须设置低通滤波器，同时抑制镜像和混叠。')

    doc.h3('例 2  32 kHz 音乐信号转换为 48 kHz（多选）')
    doc.bullet([
        'A. 选择升采样率因子 L=3。',
        'B. 选择升采样率因子 L=2。',
        'C. 选择降采样率因子 M=2。',
        'D. 选择降采样率因子 M=3。',
    ])
    red_line(doc, '答案：A、C。因为 48/32=3/2，所以 L=3，M=2。')

    draw_up2_filter_down2_spectra_page(doc)

    doc.h2('课后题与答案')
    doc.h3('第 2 题  D=2 直接抽取')
    doc.p('信号 x(n) 的频谱支撑区间为 |ω|≤π/3。按因子 D=2 直接抽取，得到 y(m)=x(2m)。画出 y(m) 的频谱，并判断是否丢失信息。')
    draw_formula_block(doc, r'y(m)=x(2m),\qquad Y(e^{j\omega})=\frac{1}{2}\left[X(e^{j\frac{\omega}{2}})+X(e^{j(\frac{\omega}{2}-\pi)})\right]', 'exercise_d2', fontsize=14, max_h=44)
    c = doc.c
    top = doc.y
    triangle_spectrum(c, MARGIN_X + 40, top - 55, 210, 42, '输入频谱 X(e^{jω})', 'π/3')
    triangle_spectrum(c, MARGIN_X + 315, top - 55, 210, 42, '抽取后频谱 Y(e^{jω})', '2π/3')
    doc.y = top - 105
    red_line(doc, '答案：D=2，而原信号带宽为 π/3<π/2，因此抽取过程中不会丢失信息。')

    doc.h3('第 3 题  D=4 抽取器')
    doc.p('已知 Fx=1 kHz、Fy=250 Hz，输入频谱在 [-π,π] 内。画出理想抗混叠低通滤波器及滤波后、抽取后的频谱。')
    draw_formula_block(doc, r'D=\frac{F_x}{F_y}=\frac{1000}{250}=4,\qquad \omega_c=\frac{\pi}{D}=\frac{\pi}{4}', 'exercise_d4', fontsize=16, max_h=42)
    system_chain(doc, 'D=4 抽取结构', ['h_D(n)\n理想低通', '↓4\n抽取'], [CYAN, YELLOW])
    doc.p('理想抗混叠滤波器仅保留 |ω|≤π/4。滤波后再抽取，输出频谱扩展到 [-π,π]，且不发生混叠。')
    red_line(doc, '原课件结论：先按 π/4 截止频率限带，再进行 4 倍抽取。')

def build():
    register_fonts(); OUT_DIR.mkdir(exist_ok=True)
    doc=Doc(PDF_PATH); doc.section='第七章 多采样率信号处理'; doc.start()

    doc.h1('第七章 多采样率数字信号处理')
    doc.p('多采样率处理研究在数字域改变序列采样率的方法，核心操作是整数倍抽取、整数倍内插以及二者组合。')
    doc.table(['模块','内容'],[['7.1','多采样率信号处理引入'],['7.2','信号的整数倍抽取'],['7.3','信号的整数倍内插'],['7.4','单级、多级采样率转换与应用']], [90,430], row_h=28)
    doc.h2('7.1 多采样率信号处理的引入')
    doc.p('数字信号处理中常需要改变采样率。例如音频系统中常见 32 kHz、44.1 kHz、48 kHz 等采样频率，CD 常用 44.1 kHz，而数字音频广播可用 32 kHz。')
    system_chain(doc,'采样率直接转换',['采样率\n转换器'],[YELLOW])
    system_chain(doc,'采样率间接转换',['D/A','模拟\n滤波','A/D'],[CYAN,None,CYAN])
    red_line(doc,'改变采样率是在数字域实现的，即对采样后的数字信号 x(n) 进行采样率转换。')

    doc.h2('7.2 信号的整数倍抽取')
    doc.p('M 倍抽取表示每隔 M 点取一点，采样率降低为原来的 1/M。')
    system_chain(doc,'M 倍抽取结构',['↓M\n抽取'],[YELLOW])
    decimation_derivation(doc)
    decimation_full_derivation(doc)
    draw_decimation_sampling_theorem_page(doc)
    draw_decimation_spectral_construction_page(doc)
    freq_replicas(doc,'抽取造成的频谱压缩和混叠',mode='dec')
    filter_cascade(doc,'dec')
    draw_decimation_filter_example_page(doc)

    doc.h2('7.3 信号的整数倍内插')
    doc.p('L 倍内插通过在相邻样本之间插入 L-1 个零，使采样率提高为原来的 L 倍。')
    system_chain(doc,'L 倍内插结构',['↑L\n内插'],[YELLOW])
    interpolation_derivation(doc)
    interpolation_full_derivation(doc)
    draw_interpolation_sampling_theorem_page(doc)
    freq_replicas(doc,'内插造成的镜像频谱',mode='int')
    filter_cascade(doc,'int')
    draw_source_filter_cascade_page(doc)

    doc.h2('7.4 采样率转换与应用')
    draw_fractional_conversion_source_page(doc)
    draw_multistage_factorization_page(doc)
    tdm_fdm(doc)
    source_exercises_and_answers(doc)

    doc.save()
    NOTE_PATH.write_text('第十三批覆盖原 PPT 400-436 页。手绘重排多采样率章节：抽取、内插、级联滤波、L/M 变换、多级结构、TDM/FDM 和课后题。最终合并前需继续与原 PDF 逐页比对。\n',encoding='utf-8')
    print(PDF_PATH)

if __name__=='__main__':
    build()
