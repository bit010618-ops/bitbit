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
PDF_PATH=OUT_DIR/'DSP讲义重制_第十二批_原PPT367-399页_FIR滤波器设计_手绘复刻版.pdf'
NOTE_PATH=OUT_DIR/'DSP讲义重制_第十二批_原PPT367-399页_FIR滤波器设计_手绘复刻版_校对记录.md'
BLACK=colors.HexColor('#111111')
GREEN=colors.HexColor('#0A8F3A')
LIGHT_RED=colors.HexColor('#FFF1F1')
GRID=colors.HexColor('#B8B8B8')


def red_line(doc, text, size=9.5, leading=15):
    lines=wrap(text, CONTENT_W, 'CN', size)
    doc.ensure(len(lines)*leading+4)
    c=doc.c; c.setFont('CNB', size); c.setFillColor(RED)
    for line in lines:
        c.drawString(MARGIN_X, doc.y, line); doc.y-=leading
    doc.y-=3


def label_line(doc, label, text, red=False):
    doc.ensure(18)
    c=doc.c
    c.setFont('CNB',9.6); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X, doc.y, label)
    c.setFont('CN',9.4); c.setFillColor(RED if red else TEXT); c.drawString(MARGIN_X+72, doc.y, text)
    doc.y-=17


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
        c.drawString(x+10,y+h*0.55+11,title)
    for pos,lab in marks:
        xx=x+w*pos
        c.line(xx,y-3,xx,y+3)
        c.drawCentredString(xx,y-12,lab)
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
    c.drawString(MARGIN_X, top-28, '0.5 是自镜像零点；0.5e^{±jπ/4} 还需补它们关于单位圆的倒数共轭零点。')
    c.setFont('CNB',8.8); c.setFillColor(RED)
    c.drawString(MARGIN_X, top-45, '因此最低阶数为 7 个零点，对应 N=8，群延迟 τ=(N-1)/2=3.5。')
    cx=MARGIN_X+385; cy=top-125; r=48
    c.setStrokeColor(BLUE); c.circle(cx,cy,r,stroke=1,fill=0)
    arrow(c,cx-r-25,cy,cx+r+35,cy,BLACK,0.9); arrow(c,cx,cy-r-24,cx,cy+r+26,BLACK,0.9)
    c.setFont('CN',7.5); c.setFillColor(TEXT); c.drawString(cx+r+38,cy-3,'Re'); c.drawString(cx+4,cy+r+26,'Im')
    pts=[(1,0,'1'),(0.5,0,'0.5'),(0.5/math.sqrt(2),0.5/math.sqrt(2),r'0.5e^{j\pi/4}'),(0.5/math.sqrt(2),-0.5/math.sqrt(2),r'0.5e^{-j\pi/4}'),(2/math.sqrt(2),2/math.sqrt(2),r'2e^{j\pi/4}'),(2/math.sqrt(2),-2/math.sqrt(2),r'2e^{-j\pi/4}')]
    for px,py,lab in pts:
        xx=cx+px*r; yy=cy+py*r
        c.setFillColor(RED if abs(px)>1 or abs(py)>1 else BLACK); c.circle(xx,yy,3,stroke=0,fill=1)
    draw_math_at(c,r'\{1,0.5,0.5e^{\pm j\pi/4}\}\Rightarrow\{2e^{\pm j\pi/4}\}',MARGIN_X+30,top-125,250,28,13,name='zeros_set')
    doc.y=top-h

def sampled_response(doc):
    h=155
    doc.ensure(h+8)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-6,'频率采样例题：N=33 的低通采样')
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


def build():
    register_fonts(); OUT_DIR.mkdir(exist_ok=True)
    doc=Doc(PDF_PATH); doc.section='第六章 FIR滤波器设计'; doc.start()

    doc.h2('6.4.3 线性相位 FIR 系统函数零点特点')
    doc.p('原课件从冲激响应的对称或反对称条件出发，说明线性相位 FIR 的零点分布具有成组出现的特点。')
    label_line(doc,'结论 1','h(n) 为 N 点有限长序列，H(z) 是 N-1 阶多项式，零点个数为 N-1 个。',red=True)
    label_line(doc,'结论 2','线性相位 FIR 的零点关于单位圆镜像对称；若 h(n) 为实序列，还具有共轭对称。',red=True)
    draw_formula_block(doc,r'H(z)=\pm z^{-(N-1)}H(z^{-1}),\qquad H(z_i^{-1})=0\Rightarrow z_i^{-1}','lp_zero_relation',fontsize=14,max_h=40)
    doc.bullet(['N-1 个零点中，关于单位圆镜像成对出现；实系数时还会出现共轭零点。','若某个零点在单位圆上，倒数镜像仍在同一点，只需要再考虑共轭关系。'])
    zero_plane(doc)
    linear_phase_classification_example(doc)

    doc.h2('6.5 线性相位 FIR 理想滤波器')
    doc.p('设计 FIR 滤波器时，先给定理想幅频响应和线性相位，再由反变换得到无限长冲激响应。实际实现必须截断为有限长。')
    ideal_filters(doc)
    draw_formula_block(doc,r'H_d(e^{j\omega})=|H_d(e^{j\omega})|e^{-j\omega\tau},\qquad \tau=\frac{N-1}{2}','ideal_phase',fontsize=15,max_h=38)
    draw_formula_block(doc,r'h_d(n)=\frac{1}{2\pi}\int_{-\pi}^{\pi}H_d(e^{j\omega})e^{j\omega n}\,d\omega','ideal_inv',fontsize=15,max_h=38)
    ideal_impulse_responses(doc)
    red_line(doc,'四类理想滤波器能否实现，要同时看 N 的奇偶和 h(n) 的对称类型。',size=9.2)

    doc.h2('6.5.2 利用窗函数法设计 FIR 滤波器')
    window_flow(doc)
    doc.p('用窗函数把无限长的 h_d(n) 截成有限长，时域是相乘，频域就是卷积。因此窗函数会决定过渡带宽和阻带波纹。')
    draw_formula_block(doc,r'h(n)=h_d(n)w(n),\qquad H(e^{j\omega})=H_d(e^{j\omega})*W(e^{j\omega})','window_main_formula',fontsize=15,max_h=38)
    window_effect(doc)
    doc.h3('常用窗函数及指标')
    red_line(doc,'常年记！！！考试可能不提供。',size=9.3)
    window_table(doc)
    doc.h3('窗函数法设计步骤')
    doc.bullet(['由技术指标确定通带、阻带边界频率以及过渡带宽 Δω。','根据阻带衰减 α_s 选择窗函数类型；再由窗函数的 Δω 公式估算阶数 N。','理想滤波器的截止频率通常取过渡带中点。','写出 h_d(n)，再乘窗函数得到 h(n)。'])
    draw_formula_block(doc,r'\alpha_s\ \Longrightarrow\ w(n),\qquad N\approx \frac{A}{\Delta\omega}','window_step',fontsize=15,max_h=38)

    doc.h3('例：窗函数法设计低通 FIR 数字滤波器')
    doc.p('指标：抽样频率 fs=15 kHz；通带截止 fp=1.5 kHz；阻带截止 fst=3 kHz；阻带衰减不小于 50 dB。')
    draw_formula_block(doc,r'\omega_p=2\pi\frac{f_p}{f_s}=0.2\pi,\qquad \omega_{st}=2\pi\frac{f_{st}}{f_s}=0.4\pi','win_ex_freq',fontsize=15,max_h=38)
    draw_formula_block(doc,r'\omega_c=\frac{\omega_p+\omega_{st}}{2}=0.3\pi,\qquad \Delta\omega=0.2\pi','win_ex_wc',fontsize=15,max_h=38)
    doc.p('阻带衰减 50 dB，可选海明窗；由 6.6π/N≈0.2π 得 N≈33，取 N=33，群延迟 α=(N-1)/2=16。')
    draw_formula_block(doc,r'h(n)=h_d(n)w(n)=\frac{\sin[0.3\pi(n-16)]}{\pi(n-16)}\left[0.54-0.46\cos\frac{2\pi n}{32}\right]R_{33}(n)','win_ex_hn',fontsize=13,max_h=52)
    red_line(doc,'设计时最容易漏的是取截止频率为过渡带中点，以及确认 N 为奇数时线性相位中心在整数点。',size=9.2)

    doc.h2('6.5.3 利用频率采样法设计 FIR 滤波器')
    doc.p('频率采样法把期望频响 H_d(e^{jω}) 在 N 个等间隔频率点上采样，得到 H(k)，再作 N 点 IDFT 得到 h(n)。')
    draw_formula_block(doc,r'H(k)=H_d(e^{j\omega})\mid_{\omega=2\pi k/N},\qquad h(n)=\frac{1}{N}\sum_{k=0}^{N-1}H(k)W_N^{-kn}','freq_sample_basic',fontsize=14,max_h=45)
    sampling_structure(doc)
    doc.h3('线性相位约束条件')
    doc.bullet(['对称 h(n)=h(N-1-n)：幅度采样满足 H_k=H_{N-k}，相位 θ_k=-[(N-1)/N]πk。','反对称 h(n)=-h(N-1-n)：幅度采样满足 H_k=-H_{N-k}，相位仍按线性相位关系确定。','设计流程：先判滤波器类型与 h(n) 对称性，再写出幅度 H_k 和相位 θ_k，最后由 IDFT 求 h(n)。'])
    red_line(doc,'设计线性相位滤波器时，一定要先判断 N 的奇偶、h(n) 的对称性和滤波器类型。',size=9.2)

    doc.h3('例：频率采样法设计线性相位低通 FIR')
    doc.p('已知 ω_c=0.5π，采样点数为奇数 N=33，试求各采样点幅值 H_k 与相位 θ_k。')
    sampled_response(doc)
    draw_formula_block(doc,r'H_k=1,\quad 0\leq k\leq 8,\ 25\leq k\leq 32;\qquad H_k=0,\quad 9\leq k\leq 24','freq_ex_hk',fontsize=13,max_h=42)
    draw_formula_block(doc,r'\theta_k=-\frac{N-1}{N}\pi k=-\frac{32}{33}\pi k,\qquad 0\leq k\leq 32','freq_ex_theta',fontsize=13,max_h=34)
    doc.p('因为 N=33 为奇数，低通滤波器选择第一类线性相位 FIR，幅度采样关于 k=0 共轭对称。')

    doc.h2('本章导图与课后题')
    doc.p('本章围绕 FIR 滤波器设计展开：先掌握线性相位条件与四类结构，再掌握两种主要设计方法。')
    doc.bullet(['单纯的 FIR 频域设计必须和相频响应一起看，不能只记幅度。','窗函数法的核心是由指标选窗函数和 N；频率采样法的核心是写对 H(k) 的幅度与相位。','若第一遍掌握不牢，优先整理两个响应的具体形式：理想响应 H_d(e^{jω}) 与实际有限长 h(n)。'])
    draw_note(doc,'课后题', [
        '1：简单 FIR 滤波器幅频响应和相频响应的描述。',
        '2：频率采样法设计滤波器的知识点，并结合一类线性相位与 N 的奇偶判断。',
        '3：与第 1 题本质相同，进一步求两个响应的具体形式。',
        '4-5：窗函数法设计 FIR 滤波器，注意 N 的限制。',
        '8：常规综合题，先回顾前置知识。',
        '13-14、15、17：频率采样法设计 FIR 滤波器。',
        '18：与上一题同类，但频率采样值需自行求出，注意 ω 与 k 的互相转化。'])

    doc.save()
    NOTE_PATH.write_text('第十二批覆盖原 PPT 367-399 页。图形均为重画：保留线性相位零点、理想滤波器、窗函数法、频率采样法、例题、红字重点和课后题；最终合并前仍需逐页对照原 PDF。\n',encoding='utf-8')
    print(PDF_PATH)

if __name__=='__main__':
    build()




