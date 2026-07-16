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
PDF_PATH=OUT_DIR/'DSP讲义重制_第八批_原PPT228-265页_FFT_手绘复刻版.pdf'
NOTE_PATH=OUT_DIR/'DSP讲义重制_第八批_原PPT228-265页_FFT_手绘复刻版_校对记录.md'
BLACK=colors.HexColor('#111111')
GREEN=colors.HexColor('#149647')
PINK=colors.HexColor('#FFE3F8')
CYAN=colors.HexColor('#DFF7FF')


def red_line(doc,text,size=9.2,leading=14):
    lines=wrap(text,CONTENT_W,'CNB',size)
    doc.ensure(len(lines)*leading+4)
    bottom=draw_auto_math_block(
        doc.c,MARGIN_X,doc.y+size,text,CONTENT_W,
        font='CNB',size=size,leading=leading,color=RED,
    )
    doc.y=bottom-size-3


def block(c,x,y,w,h,label,stroke=RED,fill=None,font=9.0):
    if fill:
        c.setFillColor(fill); c.roundRect(x,y-h/2,w,h,3,stroke=0,fill=1)
    c.setStrokeColor(stroke); c.setLineWidth(1.1); c.roundRect(x,y-h/2,w,h,3,stroke=1,fill=0)
    draw_centered_multiline_text(c,x+w/2,y,label,'CNB',font,leading=12,color=TEXT)


def sequence_block(c,x,y,w,h,items,title='',stroke=RED,fill=None,font=7.6,
                   top_pad=18,bottom_pad=14):
    """Draw a full-height sequence with evenly distributed entries."""
    if fill:
        c.setFillColor(fill); c.roundRect(x,y-h/2,w,h,3,stroke=0,fill=1)
    c.setStrokeColor(stroke); c.setLineWidth(1.1); c.roundRect(x,y-h/2,w,h,3,stroke=1,fill=0)
    usable=h-top_pad-bottom_pad
    step=usable/(len(items)-1)
    top=y+h/2-top_pad
    for i,item in enumerate(items):
        draw_auto_math_text(
            c,x+w/2,top-i*step,item,
            font='CNB',size=font,color=TEXT,align='center',
        )
    if title:
        draw_auto_math_text(
            c,x+w/2,y+h/2+11,title,
            font='CNB',size=8,color=TEXT,align='center',
        )


def two_col_table(doc):
    h=132; doc.ensure(h+8); c=doc.c; top=doc.y
    x=MARGIN_X; y=top; widths=[130,190,190]; rh=28
    c.setFillColor(BLUE_DARK); c.roundRect(x,y-rh,sum(widths),rh,4,stroke=0,fill=1)
    c.setFillColor(colors.white); c.setFont('CNB',8.8)
    xx=x
    for i,head in enumerate(['算法','复数乘法','复数加法']):
        c.drawCentredString(xx+widths[i]/2,y-18,head); xx+=widths[i]
    rows=[('一点 DFT','0','0'),('N 点 DFT',r'N^2',r'N(N-1)'),('N 点 FFT',r'\frac{N}{2}\log_2N',r'N\log_2N')]
    y0=y-rh
    for r,row in enumerate(rows):
        c.setFillColor(colors.white if r%2==0 else PALE_BLUE); c.rect(x,y0-rh,sum(widths),rh,stroke=0,fill=1)
        c.setStrokeColor(colors.HexColor('#C8DDF0')); c.rect(x,y0-rh,sum(widths),rh,stroke=1,fill=0)
        c.setFillColor(TEXT); c.setFont('CN',8.6); c.drawString(x+8,y0-18,row[0])
        draw_math_at(c,row[1],x+widths[0]+12,y0-14,90,16,10,name=f'opmul_{r}')
        draw_math_at(c,row[2],x+widths[0]+widths[1]+12,y0-14,100,16,10,name=f'opadd_{r}')
        y0-=rh
    doc.y=top-h

def twiddle_table(doc):
    items=[
        ('定义',r'W_N^{kn}=e^{-j\frac{2\pi}{N}kn}'),
        ('对称性',r'W_N^{-kn}=W_N^{N-kn}=(W_N^{kn})^*'),
        ('周期性',r'W_N^{k(n+N)}=W_N^{kn}'),
        ('可约性',r'W_N^{kn}=W_{N/m}^{kn/m}'),
        ('特殊点',r'W_N^0=1,\quad W_N^{N/2}=-1,\quad W_N^{k+N/2}=-W_N^k'),
    ]
    h=150; doc.ensure(h+8); c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-6,'旋转因子的常用性质')
    y=top-34
    for i,(lab,expr) in enumerate(items):
        yy=y-i*24
        c.setFont('CNB',9); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,yy-4,lab)
        draw_math_at(c,expr,MARGIN_X+75,yy,390,19,11,name=f'twiddle_{i}')
    doc.y=top-h

def split_flow(doc):
    # Match the source page's complete odd/even split diagram: sequence boxes,
    # two 4-point DFTs and the final recombination are all retained.
    h=235; doc.ensure(h+8); c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-6,'按奇偶分解的基 2 DIT-FFT')
    x=MARGIN_X-2; y=top-118
    sequence_block(c,x,y,48,170,[f'x({i})' for i in range(8)],'x(n)',fill=CYAN,font=7.6)

    upper=y+43; lower=y-43
    sequence_block(c,x+92,upper,92,79,
                   ['x(0)=x1(0)','x(2)=x1(1)','x(4)=x1(2)','x(6)=x1(3)'],
                   fill=YELLOW,font=7.2,top_pad=13,bottom_pad=10)
    sequence_block(c,x+92,lower,92,79,
                   ['x(1)=x2(0)','x(3)=x2(1)','x(5)=x2(2)','x(7)=x2(3)'],
                   fill=YELLOW,font=7.2,top_pad=13,bottom_pad=10)
    c.setFont('CNB',7.7); c.setFillColor(TEXT); c.drawCentredString(x+138,upper+49,'x1(r)'); c.drawCentredString(x+138,lower-51,'x2(r)')
    block(c,x+210,upper,48,62,'4点\nDFT',fill=YELLOW,font=8.4)
    block(c,x+210,lower,48,62,'4点\nDFT',fill=YELLOW,font=8.4)
    sequence_block(c,x+282,upper,71,84,
                   ['= X1(0)','= X1(1)','= X1(2)','= X1(3)'],
                   fill=YELLOW,font=7.2,top_pad=14,bottom_pad=11)
    sequence_block(c,x+282,lower,71,84,
                   ['= X2(0)','= X2(1)','= X2(2)','= X2(3)'],
                   fill=YELLOW,font=7.2,top_pad=14,bottom_pad=11)
    c.setFont('CNB',7.7); c.setFillColor(TEXT); c.drawCentredString(x+318,upper+52,'X1(k)'); c.drawCentredString(x+318,lower-52,'X2(k)')
    # The original slide deliberately leaves recombination as the next question.
    # Keep its large yellow question-arrow instead of inventing extra links.
    arrow_x=x+386; arrow_y=y
    c.setFillColor(YELLOW); c.setStrokeColor(RED); c.setLineWidth(1.2)
    p=c.beginPath(); p.moveTo(arrow_x,arrow_y+24); p.lineTo(arrow_x+26,arrow_y+24)
    p.lineTo(arrow_x+26,arrow_y+40); p.lineTo(arrow_x+52,arrow_y)
    p.lineTo(arrow_x+26,arrow_y-40); p.lineTo(arrow_x+26,arrow_y-24)
    p.lineTo(arrow_x,arrow_y-24); p.close(); c.drawPath(p,stroke=1,fill=1)
    c.setFillColor(BLACK); c.setFont('CNB',22); c.drawCentredString(arrow_x+28,arrow_y-8,'?')
    sequence_block(c,x+450,y,50,170,[f'X({i})' for i in range(8)],'X(k)',fill=CYAN,font=7.5)
    for yy in [upper,lower]:
        arrow(c,x+184,yy,x+210,yy,RED,1.0)
        arrow(c,x+258,yy,x+282,yy,RED,1.0)
    arrow(c,arrow_x+52,arrow_y,x+450,arrow_y,RED,1.0)
    c.setFont('CNB',5.8); c.setFillColor(TEXT)
    c.drawCentredString(x+82,upper+15,'偶序号')
    draw_auto_math_text(c,x+82,upper+7,'x(2r)',font='CNB',size=5.8,align='center')
    c.drawCentredString(x+82,lower+15,'奇序号')
    draw_auto_math_text(c,x+82,lower+7,'x(2r+1)',font='CNB',size=5.8,align='center')
    # Source slide 238 branches once from x(n), then routes vertically to the
    # even and odd subsequences.  Keep the shared stem instead of two unrelated
    # arrows starting at different rows of the input frame.
    branch_x=x+72
    c.setStrokeColor(RED); c.setLineWidth(1.0)
    c.line(branch_x,lower,branch_x,upper)
    arrow(c,x+48,y,branch_x,y,RED,1.0,head=3.2)
    arrow(c,branch_x,upper,x+92,upper,RED,1.0,head=3.2)
    arrow(c,branch_x,lower,x+92,lower,RED,1.0,head=3.2)
    doc.y=top-h

def _fft_graph_spec(kind):
    """Return the exact N=8 source-slide topology for DIT, DIF, or IFFT."""
    if kind == 'DIT':
        return {
            'input_order': [0, 4, 2, 6, 1, 5, 3, 7],
            'output_order': list(range(8)),
            'stage_pairs': [
                [(0, 1), (2, 3), (4, 5), (6, 7)],
                [(0, 2), (1, 3), (4, 6), (5, 7)],
                [(0, 4), (1, 5), (2, 6), (3, 7)],
            ],
            'stage_exponents': [
                [0, 0, 0, 0],
                [0, 2, 0, 2],
                [0, 1, 2, 3],
            ],
            'title_banner': 'pink',
            'stage_fill': 'green',
            'stage_count_badge': r'M=\log_2N',
            'output_scale': None,
        }
    if kind in ('DIF', 'IFFT'):
        sign = -1 if kind == 'IFFT' else 1
        return {
            'input_order': list(range(8)),
            'output_order': [0, 4, 2, 6, 1, 5, 3, 7],
            'stage_pairs': [
                [(0, 4), (1, 5), (2, 6), (3, 7)],
                [(0, 2), (1, 3), (4, 6), (5, 7)],
                [(0, 1), (2, 3), (4, 5), (6, 7)],
            ],
            'stage_exponents': [
                [0, sign, 2 * sign, 3 * sign],
                [0, 2 * sign, 0, 2 * sign],
                [0, 0, 0, 0],
            ],
            'title_banner': 'pink',
            'outer_frame': 'green',
            'output_scale': ['1/N'] * 8 if kind == 'IFFT' else None,
        }
    raise ValueError(f'unsupported FFT flowgraph kind: {kind}')


def _stage_twiddle_exponents(kind, stage):
    return _fft_graph_spec(kind)['stage_exponents'][stage]


def _twiddle_tex(kind, exponent):
    base = '8' if kind == 'DIT' else 'N'
    return fr'W_{base}^{{{exponent}}}'

def fft_butterfly(doc,kind='DIT'):
    h=352; doc.ensure(h+12); c=doc.c; top=doc.y
    titles={
        'DIT':'基 2-DIT-FFT 蝶形流图（N=8，M=3）',
        'DIF':'基 2-DIF-FFT 运算流图（N=8）',
        'IFFT':'DIF-IFFT 运算流图（N=8）',
    }
    title=titles[kind]
    spec=_fft_graph_spec(kind)
    banner_fill=colors.HexColor('#F7C8F4')
    banner_w=330 if kind=='DIT' else 245
    banner_x=MARGIN_X+(CONTENT_W-banner_w)/2-(26 if kind=='DIT' else 0)
    c.setFillColor(banner_fill); c.rect(banner_x,top-26,banner_w,24,stroke=0,fill=1)
    c.setFont('CNB',11); c.setFillColor(BLACK)
    c.drawCentredString(banner_x+banner_w/2,top-19,title)
    if kind=='DIT':
        badge_x=MARGIN_X+CONTENT_W-102
        c.setStrokeColor(colors.HexColor('#D100D8')); c.setLineWidth(1.0)
        c.setFillColor(colors.HexColor('#23E4E4')); c.rect(badge_x,top-26,102,24,stroke=1,fill=1)
        draw_math_at(c,r'M=\log_2N',badge_x+8,top-9,86,18,12,name='dit_stage_badge')
    x=MARGIN_X+6; y_top=top-58; dy=25
    ys=[y_top-i*dy for i in range(8)]
    line_color=RED if kind=='DIT' else BLACK
    panel_fill=colors.HexColor('#D9F9D6')
    input_order=spec['input_order']; output_order=spec['output_order']
    input_x=x+75; output_x=x+438
    stage_left=[x+92,x+210,x+328]
    stage_right=[v+98 for v in stage_left]

    def path(points):
        p=c.beginPath(); p.moveTo(*points[0])
        for point in points[1:]: p.lineTo(*point)
        c.drawPath(p,stroke=1,fill=0)

    if kind == 'DIT':
        # Source slide 245 has cyan input/output sequence frames.
        c.setStrokeColor(RED); c.setLineWidth(1.2); c.setFillColor(CYAN)
        c.rect(x+25,ys[-1]-15,46,ys[0]-ys[-1]+30,stroke=1,fill=1)
        c.rect(x+443,ys[-1]-15,48,ys[0]-ys[-1]+30,stroke=1,fill=1)
    else:
        # Source slides 251 and 253 use one green outer frame, not three stage boxes.
        c.setStrokeColor(colors.HexColor('#21B83F')); c.setLineWidth(1.2)
        c.rect(x+5,ys[-1]-25,500,ys[0]-ys[-1]+50,stroke=1,fill=0)
    for i,n in enumerate(input_order):
        symbol='X' if kind=='IFFT' else 'x'
        label_x=x+31 if kind=='DIT' else x+10
        draw_math_at(c,fr'{symbol}({n})',label_x,ys[i]+1,38,14,10,name=f'{kind}_input_{i}')
        c.setFillColor(line_color); c.circle(input_x,ys[i],2.2,stroke=0,fill=1)
    for i,n in enumerate(output_order):
        c.setFillColor(line_color); c.circle(output_x,ys[i],2.2,stroke=0,fill=1)
        symbol='x' if kind=='IFFT' else 'X'
        label_x=x+450 if kind=='DIT' else x+447
        draw_math_at(c,fr'{symbol}({n})',label_x,ys[i]+1,39,14,10,name=f'{kind}_output_{i}')

    # DIT source uses three filled green stage panels; DIF/IFFT use only the outer frame.
    for s,(left,right) in enumerate(zip(stage_left,stage_right)):
        if kind=='DIT':
            c.setStrokeColor(RED); c.setFillColor(panel_fill); c.rect(left,ys[-1]-18,right-left,ys[0]-ys[-1]+36,stroke=1,fill=1)
            c.setFillColor(YELLOW); c.roundRect(left+15,ys[0]+10,62,19,2,stroke=0,fill=1)
            c.setFillColor(BLACK); c.setFont('CNB',8.2)
            draw_auto_math_text(c,left+46,ys[0]+16,'N/2 个蝶形',font='CNB',size=8.2,align='center')
        c.setStrokeColor(line_color); c.setLineWidth(1.05)

    # Each stage follows the exact row pairings and branch direction shown in the source.
    for s,(left,right) in enumerate(zip(stage_left,stage_right)):
        pairs=spec['stage_pairs'][s]
        exponents=spec['stage_exponents'][s]
        for pi,(a,b) in enumerate(pairs):
            mid=(left+right)/2
            lead=18
            path([(left,ys[a]),(mid-lead,ys[a]),(mid+lead,ys[b]),(right,ys[b])])
            path([(left,ys[b]),(mid-lead,ys[b]),(mid+lead,ys[a]),(right,ys[a])])
            c.setFillColor(line_color); c.circle(mid, (ys[a]+ys[b])/2, 3.0, stroke=0, fill=1)
            exponent = exponents[pi]
            if kind == 'DIT':
                # Twiddle factor is attached to the lower-input/upward branch.
                arrow(c,mid-7,(ys[a]+ys[b])/2-7,mid+8,(ys[a]+ys[b])/2+8,line_color,0.75,head=3.2)
                label_x=mid-35; label_y=ys[b]+11
            else:
                # DIF/IFFT multiply on the lower output branch after the sum/difference node.
                arrow(c,mid+5,(ys[a]+ys[b])/2-5,mid+20,(ys[a]+ys[b])/2-20,line_color,0.75,head=3.2)
                label_x=mid+23; label_y=ys[b]+12
            draw_math_at(c,_twiddle_tex(kind,exponent),label_x,label_y,39,14,8.8,name=f'{kind}_twiddle_{s}_{pi}')

        # Source drawings mark every stage boundary, making routing unambiguous.
        c.setFillColor(line_color)
        for yy in ys:
            c.circle(left,yy,1.8,stroke=0,fill=1)
            c.circle(right,yy,1.8,stroke=0,fill=1)

    # Connect the stage boundaries and the output frame with clean horizontal segments.
    c.setStrokeColor(line_color); c.setLineWidth(1.05)
    for row,yy in enumerate(ys):
        c.line(input_x,yy,stage_left[0],yy)
        c.line(stage_right[0],yy,stage_left[1],yy)
        c.line(stage_right[1],yy,stage_left[2],yy)
        if kind == 'IFFT':
            arrow(c,stage_right[-1],yy,output_x,yy,line_color,0.8,head=3.2)
            draw_math_at(c,r'\frac{1}{N}',stage_right[-1]+11,yy+8,28,12,8,name=f'ifft_scale_{row}')
        else:
            c.line(stage_right[-1],yy,output_x,yy)

    if kind=='DIT':
        c.setFillColor(TEXT); c.setFont('CNB',10)
        c.drawCentredString(x+260,ys[-1]-45,'M级蝶形运算')
        c.setFillColor(RED); c.setFont('CNB',9)
        c.drawString(MARGIN_X,ys[-1]-75,'基 2-DIT-FFT 复数乘法次数：')
        draw_math_at(
            c, r'\frac{N}{2}\times M=\frac{N}{2}\log_2N',
            MARGIN_X+220, ys[-1]-70, 190, 24, 15,
            color='#E00000', name='dit_ops'
        )
    elif kind=='DIF':
        c.setFillColor(TEXT); c.setFont('CN',9)
        c.drawCentredString(x+270,ys[-1]-40,'频率抽取法和时间抽取法总的计算量相同。')
    doc.y=top-h


def small_butterfly(doc):
    h=110; doc.ensure(h+8); c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-6,'蝶形运算')
    x=MARGIN_X+230; y=top-50
    draw_math_at(c,r'X_1(k)',x-65,y+35,55,14,10,name='bf_x1')
    draw_math_at(c,r'X_2(k)',x-65,y-25,55,14,10,name='bf_x2')
    draw_math_at(c,r'X_1(k)+W_N^kX_2(k)',x+85,y+35,135,16,10,name='bf_y1')
    draw_math_at(c,r'X_1(k)-W_N^kX_2(k)',x+85,y-25,135,16,10,name='bf_y2')
    arrow(c,x,y+30,x+70,y-30,BLACK,0.9,head=3.2)
    arrow(c,x,y-30,x+70,y+30,BLACK,0.9,head=3.2)
    dot(c,x+35,y,2.5,BLACK)
    draw_math_at(c,r'W_N^k',x+2,y-7,30,13,8.5,name='bf_twiddle')
    doc.y=top-h


def _convolution_layout():
    return {
        'label_x': 5,
        'input_arrow': (45, 90),
        'pad_x': 95,
        'pad_w': 60,
        'fft_arrow': (155, 200),
        'fft_x': 205,
        'fft_w': 52,
        'merge_x': 305,
        'multiply_x': 310,
        'multiply_w': 38,
        'output_arrow': (348, 405),
        'ifft_x': 410,
        'ifft_w': 55,
        'right_edge': 465,
    }


def convolution_fft(doc):
    h=170; doc.ensure(h+8); c=doc.c; top=doc.y
    x=MARGIN_X; y=top-40; layout=_convolution_layout()
    for row,lab in enumerate([r'x(n)',r'h(n)']):
        yy=y-row*50
        draw_math_at(c,lab,x+layout['label_x'],yy+5,35,14,10,name=f'conv_{row}')
        arrow(c,x+layout['input_arrow'][0],yy,x+layout['input_arrow'][1],yy,RED,0.9)
        block(c,x+layout['pad_x'],yy,layout['pad_w'],26,'补零至\nN点',stroke=RED)
        arrow(c,x+layout['fft_arrow'][0],yy,x+layout['fft_arrow'][1],yy,RED,0.9)
        block(c,x+layout['fft_x'],yy,layout['fft_w'],26,'N点\nFFT',stroke=RED)
    arrow(c,x+layout['fft_x']+layout['fft_w'],y,x+layout['merge_x'],y-25,RED,0.9)
    arrow(c,x+layout['fft_x']+layout['fft_w'],y-50,x+layout['merge_x'],y-25,RED,0.9)
    block(c,x+layout['multiply_x'],y-25,layout['multiply_w'],32,'×',stroke=RED,fill=PINK,font=14)
    arrow(c,x+layout['output_arrow'][0],y-25,x+layout['output_arrow'][1],y-25,RED,0.9)
    block(c,x+layout['ifft_x'],y-25,layout['ifft_w'],30,'N点\nIFFT',stroke=RED)
    doc.y=top-125
    draw_formula_block(doc,r'N\geq N_1+N_2-1,\qquad y(n)=IDFT[X(k)H(k)]=x(n)*h(n)','conv_fft_formula',fontsize=14,max_h=40)
    doc.y=min(doc.y,top-h)


def real_fft(doc):
    doc.p('实际工程中常把两个 N 点实序列合成为一个 N 点复序列，只做一次 N 点 FFT，再由共轭关系分离两个频谱。')
    draw_formula_block(doc,r'y(n)=x_1(n)+jx_2(n),\qquad Y(k)=Y_{ep}(k)+Y_{op}(k)','realfft1',fontsize=15,max_h=36)
    draw_formula_block(doc,r'X_1(k)=\frac{1}{2}[Y(k)+Y^*(N-k)],\qquad X_2(k)=\frac{1}{2j}[Y(k)-Y^*(N-k)]','realfft2',fontsize=14,max_h=42)


def build():
    register_fonts(); OUT_DIR.mkdir(exist_ok=True)
    doc=Doc(PDF_PATH); doc.section='第四章 快速傅里叶变换'; doc.start()
    doc.h1('4 快速傅里叶变换')
    doc.p('DFT 可以直接计算频谱，但 N 点 DFT 的计算量较大。FFT 利用旋转因子的周期性和对称性，把长序列分解为短序列，显著减少运算量。')
    doc.h2('4.1 快速傅里叶变换的定义')
    draw_formula_block(doc,r'X(k)=\sum_{n=0}^{N-1}x(n)W_N^{kn},\qquad 0\leq k\leq N-1','fft_def',fontsize=15,max_h=40)
    two_col_table(doc)
    red_line(doc,'FFT 用于减少计算量，本质仍然是 DFT；FFT 仅仅是 DFT 的一种快速算法。')
    doc.h3('旋转因子的相关性质')
    twiddle_table(doc)

    doc.h2('4.2 快速傅里叶变换的分类')
    doc.p('按时间抽取称为 DIT，按频率抽取称为 DIF；按变换方向还可分为 FFT 和 IFFT。')
    split_flow(doc)
    draw_formula_block(doc,r'X(k)=X_1(k)+W_N^kX_2(k),\qquad X(k+\frac{N}{2})=X_1(k)-W_N^kX_2(k)','dit_formula',fontsize=15,max_h=44)
    small_butterfly(doc)

    doc.h2('基于时间抽取的基 2 FFT')
    draw_formula_block(doc,r'N=2^M,\qquad M=\log_2N,\qquad \frac{N}{2}','dit_count',fontsize=14,max_h=36)
    doc.p('其中 M 为级数，每一级包含 N/2 个蝶形运算。')
    draw_formula_block(doc,r'\frac{N}{2}\log_2N,\qquad N\log_2N','fft_ops',fontsize=14,max_h=40)
    doc.p('上式分别表示复数乘法次数和复数加法次数。')
    draw_formula_block(doc,r'N=8:\qquad N^2=64,\qquad \left(\frac{N}{2}\right)^2+\left(\frac{N}{2}\right)^2+\frac{N}{2}=36',
                       'fft_n8_compare',fontsize=12.5,max_h=38)
    doc.p('直接计算需要 64 次复数乘法；完成一次奇偶抽取后降为 36 次，继续逐级分解即可得到 FFT。')
    fft_butterfly(doc,'DIT')
    doc.h3('例：64 点 DFT 的运算时间')
    doc.p('直接 DFT 需 N^2 次复乘和 N(N-1) 次复加；FFT 只需 (N/2)log2N 次复乘和 Nlog2N 次复加，运算量明显降低。')

    doc.h2('基于频率抽取的基 2 FFT')
    draw_formula_block(doc,r'x_1(n)=x(n)+x(n+\frac{N}{2}),\qquad x_2(n)=[x(n)-x(n+\frac{N}{2})]W_N^n','dif_def',fontsize=15,max_h=42)
    doc.bullet(['DIT：输入按倒位序排列，输出为自然顺序。','DIF：输入为自然顺序，输出按倒位序排列。','两种算法的总运算量相同，区别在于分解方向和旋转因子所在支路。'])
    fft_butterfly(doc,'DIF')

    doc.h2('4.3 快速傅里叶反变换 IFFT')
    draw_formula_block(doc,r'x(n)=\frac{1}{N}\sum_{k=0}^{N-1}X(k)W_N^{-kn},\qquad W_N^{-k}=W_N^{N-k}','ifft_def',fontsize=15,max_h=40)
    fft_butterfly(doc,'IFFT')
    doc.bullet(['IFFT 可用 FFT 结构实现，只需改变旋转因子方向，并在输出端乘以 1/N。','输入输出关系与 DFT/IDFT 对应，公式中不要漏掉 1/N。'])

    doc.h2('FFT 法实现线性卷积')
    convolution_fft(doc)
    doc.h2('实序列的 FFT 算法')
    real_fft(doc)
    doc.h3('一次 N 点 FFT 计算两个 N 点实序列')
    doc.bullet(['构造复序列 y(n)=x_1(n)+jx_2(n)。','对 y(n) 作一次 N 点 FFT。','利用共轭对称关系分离 X_1(k) 与 X_2(k)。'])

    doc.h2('第四章小结与课后习题')
    draw_note(doc,'章节导图', ['FFT 定义：利用 DFT 运算中旋转因子的周期性和对称性。','DIT：按时间序列奇偶分解；DIF：按频率序列分组。','线性卷积：补零、FFT、相乘、IFFT。','实序列 FFT：一次 N 点 FFT 可拆分为两个 N 点实序列的频谱。'])
    draw_note(doc,'课后习题', ['4-3：一次 N 点 FFT 计算两个 N 点实序列。','4-4、4-8：DIT/DIF 分解与蝶形图。','第 4 章综合题：注意补零长度 N≥N1+N2-1。'])
    doc.save()
    NOTE_PATH.write_text('第八批覆盖原 PPT 228-265 页。该版本去掉原内容版中的裁图依赖，FFT 蝶形图、IFFT、线性卷积框图均为手绘重排。最终合并前仍需逐页对照原 PDF。\n',encoding='utf-8')
    print(PDF_PATH)

if __name__=='__main__':
    build()

