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
    c=doc.c; c.setFont('CNB',size); c.setFillColor(RED)
    for line in lines:
        c.drawString(MARGIN_X,doc.y,line); doc.y-=leading
    doc.y-=3


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
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-6,title)
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
            c.drawRightString(xx-5,y-14,txt)
        else:
            c.drawCentredString(xx,y-12,txt)
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
    draw_formula_block(doc,r'X_d(e^{j\omega})=\frac{1}{M}\sum_{i=0}^{M-1}X(e^{j(\omega-2\pi i)/M})','dec_freq',fontsize=15,max_h=45)
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
        r'X_d(e^{j\omega})=\frac{1}{M}\sum_{i=0}^{M-1}X(e^{j(\omega-2\pi i)/M})',
        'dec_full_result', fontsize=17, max_h=46
    )
    doc.p('因此，抽取后的频谱由原频谱压缩 M 倍后平移叠加得到。各平移分量若相互重叠，就会产生不可逆的混叠。')
    doc.h3('M=2 的特例')
    draw_formula_block(
        doc,
        r'X_d(e^{j\omega})=\frac{1}{2}\left[X(e^{j\omega/2})+X(e^{j(\omega/2-\pi)})\right]',
        'dec_m2_case', fontsize=16, max_h=48
    )
    red_line(doc,'无混叠条件：抽取前应限制原信号带宽，使 |ω|≤π/M。')


def interpolation_derivation(doc):
    draw_formula_block(doc,r'x_p(n)=x(n/L),\quad n=0,\pm L,\pm 2L,\ldots;\qquad x_p(n)=0,\quad \mathrm{else}','interp_piece',fontsize=12,max_h=42)
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


def lm_conversion(doc):
    h=200; doc.ensure(h+8); c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-6,'L/M 倍采样率转换结构')
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


def tdm_fdm(doc):
    h=330; doc.ensure(h+8); c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-6,'时分复用与频分复用')
    x=MARGIN_X+20; y=top-70
    c.setFont('CNB',9); c.setFillColor(TEXT); c.drawString(MARGIN_X, y+44, '时分复用（TDM）')
    for i in range(3):
        yy=y+28-i*24
        draw_math_at(c,fr'x_{i+1}(n)',x,yy+5,43,14,9.5,name=f'tdmx{i}')
        arrow(c,x+45,yy,x+82,yy,RED,0.9)
        block(c,x+88,yy,40,20,'',stroke=RED)
        draw_centered_multiline_text(c,x+108,yy,'↑3','CNB',8.8,color=TEXT)
        arrow(c,x+128,yy,x+205,y,RED,0.9)
    block(c,x+211,y,78,30,'TDM 串行通道',stroke=GREEN,fill=LIGHT_YELLOW)
    # tdm_demux: three centered down-sampling blocks on the receive side.
    for i in range(3):
        yy=y+28-i*24
        arrow(c,x+289,y,x+345,yy,RED,0.9)
        block(c,x+351,yy,40,20,'',stroke=RED)
        draw_centered_multiline_text(c,x+371,yy,'↓3','CNB',8.8,color=TEXT)
        arrow(c,x+391,yy,x+430,yy,RED,0.9)
        draw_math_at(c,fr'x_{i+1}(n)',x+435,yy+5,43,14,9.5,name=f'tdm_out_{i}')
    c.setFont('CN',8.6); c.setFillColor(TEXT); c.drawString(x,y-48,'TDM：三路序列按时间交织为一路串行序列，接收端再按相位分离。')

    y2=top-225
    c.setFont('CNB',9); c.setFillColor(TEXT); c.drawString(MARGIN_X, y2+44, '频分复用（FDM）')
    for i,lab in enumerate(['LP','BP','HP']):
        draw_math_at(c,fr'x_{i+1}(n)',x,y2+28-i*24,45,14,9.5,name=f'fdmx{i}')
        arrow(c,x+55,y2+26-i*24,x+132,y2+26-i*24,RED,0.9)
        block(c,x+138,y2+26-i*24,58,20,lab+' 滤波',stroke=RED)
        arrow(c,x+196,y2+26-i*24,x+292,y2,RED,0.9)
    block(c,x+300,y2,72,38,'频带合成\ny(n)',stroke=GREEN,fill=LIGHT_YELLOW)
    c.setFont('CN',8.6); c.setFillColor(TEXT); c.drawString(x,y2-48,'FDM：三路数据分别搬移到低频、中频和高频子带后合成。')
    doc.y=top-h


def triangle_spectrum(c, x, y, w, h, label, half_band='π/3', peaks=(0.5,)):
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.9)
    arrow(c, x, y, x + w, y, BLACK, 0.9)
    c.setFillColor(TEXT)
    c.setFont('CN', 7.5)
    c.drawString(x + w + 3, y - 2, 'ω')
    c.drawCentredString(x + w / 2, y - 26, label)
    for peak in peaks:
        center = x + w * peak
        half = w * 0.11
        c.line(center - half, y, center, y + h)
        c.line(center, y + h, center + half, y)
    center = x + w / 2
    c.drawCentredString(center - w * 0.11, y - 13, '-' + half_band)
    c.drawCentredString(center, y - 13, '0')
    c.drawCentredString(center + w * 0.11, y - 13, half_band)


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

    doc.h3('例 3  ↑2、低通滤波器与 ↓2 的等效系统')
    system_chain(doc, '原课件系统框图', ['↑2', '低通滤波器\nωc=π/4，增益2', '↓2'], [YELLOW, CYAN, YELLOW])
    doc.p('内插产生镜像，经截止频率 π/4、增益 2 的低通滤波器后再作 2 倍抽取。对原输入而言，整个系统等效为低通滤波器。')
    red_line(doc, '答案：截止频率为 π/2，增益为 1（选 D）。')

    doc.h2('课后题与答案')
    doc.h3('第 2 题  D=2 直接抽取')
    doc.p('信号 x(n) 的频谱支撑区间为 |ω|≤π/3。按因子 D=2 直接抽取，得到 y(m)=x(2m)。画出 y(m) 的频谱，并判断是否丢失信息。')
    draw_formula_block(doc, r'y(m)=x(2m),\qquad Y(e^{j\omega})=\frac{1}{2}\left[X(e^{j\omega/2})+X(e^{j(\omega/2-\pi)})\right]', 'exercise_d2', fontsize=14, max_h=44)
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
    freq_replicas(doc,'抽取造成的频谱压缩和混叠',mode='dec')
    filter_cascade(doc,'dec')
    doc.h3('例：抽取滤波器设计')
    doc.p('若 x(n) 的取样频率为 f_s=2f_h，h 为信号最高频率。要作 M=8 的抽取，需要先用抗混叠低通滤波器限制带宽。')
    draw_formula_block(doc,r'\omega_c=\frac{\pi}{M}=\frac{\pi}{8},\qquad h(n)=h_d(n)w(n)','dec_example',fontsize=15,max_h=36)
    doc.p('若采用汉宁窗设计 40 阶 FIR 抗混叠滤波器，则 N=41，群延迟为 20，系统差分方程为卷积和形式。')
    draw_formula_block(doc,r'x_d(n)=\sum_{k=0}^{40}h(k)x(8n-k)','dec_diff',fontsize=15,max_h=36)
    red_line(doc,'FIR 滤波器的差分方程也就是线性卷积表达式。')

    doc.h2('7.3 信号的整数倍内插')
    doc.p('L 倍内插通过在相邻样本之间插入 L-1 个零，使采样率提高为原来的 L 倍。')
    system_chain(doc,'L 倍内插结构',['↑L\n内插'],[YELLOW])
    interpolation_derivation(doc)
    interpolation_full_derivation(doc)
    freq_replicas(doc,'内插造成的镜像频谱',mode='int')
    filter_cascade(doc,'int')
    doc.h3('抽取滤波器与内插滤波器的级联位置')
    doc.bullet(['抽取时：先低通滤波，再抽取，用于抗混叠。','内插时：先插零，再低通滤波，用于抗镜像。','两者的截止频率分别和 M、L 有关，通带增益不同。'])

    doc.h2('7.4 采样率转换与应用')
    lm_conversion(doc)
    doc.p('实现分数倍采样率转换时，一般先内插、再滤波、最后抽取。这样可避免直接在低采样率下丢失应保留的频谱信息。')
    fractional_conversion_details(doc)
    tdm_fdm(doc)
    source_exercises_and_answers(doc)

    doc.save()
    NOTE_PATH.write_text('第十三批覆盖原 PPT 400-436 页。手绘重排多采样率章节：抽取、内插、级联滤波、L/M 变换、多级结构、TDM/FDM 和课后题。最终合并前需继续与原 PDF 逐页比对。\n',encoding='utf-8')
    print(PDF_PATH)

if __name__=='__main__':
    build()
