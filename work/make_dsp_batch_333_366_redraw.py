from pathlib import Path
import math
import sys
from reportlab.lib import colors

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'work'
sys.path.insert(0,str(WORK))

from make_dsp_batch_266_300_redraw import (
    BLUE, BLUE_DARK, CONTENT_W, MARGIN_X, TEXT, Doc, register_fonts,
    RED, PURPLE, PALE_BLUE, YELLOW, draw_math_at, draw_formula_block,
    draw_note, arrow, dot, delay_box, sum_node, wrap, draw_centered_multiline_text
)
from make_dsp_sample_handout_v2 import draw_auto_math_text

OUT_DIR=ROOT/'outputs'
PDF_PATH=OUT_DIR/'DSP讲义重制_第十一批_原PPT333-366页_FIR结构与线性相位_手绘复刻版.pdf'
NOTE_PATH=OUT_DIR/'DSP讲义重制_第十一批_原PPT333-366页_FIR结构与线性相位_手绘复刻版_校对记录.md'


def fir_source_topology():
    rails = ('forward_delay_chain', 'reverse_delay_chain', 'output_bus')
    return {
        'linear_phase': {
            'odd_n': {'rails': rails, 'paired_fold_branches': True,
                      'center_tap': True, 'terminal_delay': False},
            'even_n': {'rails': rails, 'paired_fold_branches': True,
                       'center_tap': False, 'terminal_delay': True},
        },
        'frequency_sampling': {
            'comb': '1-z^-N',
            'branches': ('H(0)', 'H(1)', '...', 'H(N-1)'),
            'branch_elements': ('W_N^-k', 'z^-1'),
            'output_gain': '1/N',
        },
    }


def linear_phase_fir_source_table():
    """Source-locked FIR design choices from PPT pages 365-366."""
    return {
        'type_i': {
            'n_parity': 'odd', 'symmetry': 'even',
            'filters': ('LP', 'HP', 'BP', 'BS'), 'forced_zeros': (),
            'coefficient_domain': 'other_n', 'plot_annotation': '',
        },
        'type_ii': {
            'n_parity': 'even', 'symmetry': 'even',
            'filters': ('LP', 'BP'), 'forced_zeros': ('pi',),
            'plot_annotation': 'H(pi)=0',
        },
        'type_iii': {
            'n_parity': 'odd', 'symmetry': 'odd',
            'filters': ('BP',), 'forced_zeros': ('0', 'pi'),
            'plot_annotation': 'H(0)=H(pi)=0',
        },
        'type_iv': {
            'n_parity': 'even', 'symmetry': 'odd',
            'filters': ('HP', 'BP'), 'forced_zeros': ('0',),
            'plot_annotation': 'H(0)=0',
        },
    }


def linear_phase_critical_pages_contract():
    """Elements that must remain visible on each of the two critical pages."""
    return {
        'page_count': 2,
        'shared_blocks': (
            'importance_banner',
            'symmetry_definition',
            'phase_equation',
            'phase_plot',
            'odd_n_checklist',
            'odd_n_impulse_plot',
            'odd_n_amplitude_plot',
            'odd_n_coefficient_formula',
            'odd_n_symmetry_conclusion',
            'even_n_checklist',
            'even_n_impulse_plot',
            'even_n_amplitude_plot',
            'even_n_coefficient_formula',
            'even_n_symmetry_conclusion',
        ),
        'pages': ('type_i_and_ii', 'type_iii_and_iv'),
    }


def _draw_checklist(c, x, y, allowed, name):
    labels = ('LP', 'HP', 'BP', 'BS')
    cell_w, cell_h = 34, 22
    c.setLineWidth(0.75)
    for index, label in enumerate(labels):
        xx = x + index * cell_w
        c.setStrokeColor(colors.HexColor('#7D3340'))
        c.rect(xx, y, cell_w, cell_h, stroke=1, fill=0)
        c.setFillColor(TEXT)
        c.setFont('CNB', 9.3)
        c.drawCentredString(xx + cell_w / 2, y + 7, label)
        symbol_x = xx + cell_w - 7
        symbol_y = y + cell_h / 2
        c.setStrokeColor(RED)
        c.setLineWidth(2.2)
        if label in allowed:
            c.line(symbol_x - 5, symbol_y, symbol_x - 1, symbol_y - 5)
            c.line(symbol_x - 1, symbol_y - 5, symbol_x + 6, symbol_y + 7)
        else:
            c.line(symbol_x - 4, symbol_y - 5, symbol_x + 5, symbol_y + 5)
            c.line(symbol_x - 4, symbol_y + 5, symbol_x + 5, symbol_y - 5)


def _draw_impulse_panel(c, x, y, w, h, values, center, name, frame):
    c.setStrokeColor(frame)
    c.setLineWidth(1.25)
    c.rect(x, y, w, h, stroke=1, fill=0)
    x0, axis_y = x + 17, y + h * 0.43
    arrow(c, x0, axis_y, x + w - 10, axis_y, BLUE, 0.85, head=4)
    arrow(c, x0, y + 9, x0, y + h - 9, BLUE, 0.85, head=4)
    c.setFillColor(TEXT)
    c.setFont('CNB', 8)
    c.drawString(x0 + 3, y + h - 13, 'h(n)')
    c.drawRightString(x + w - 4, axis_y - 13, 'n')
    usable = w - 40
    step = usable / (len(values) - 1)
    scale = h * 0.28 / max(abs(value) for value in values if value != 0)
    for index, value in enumerate(values):
        xx = x0 + index * step
        yy = axis_y + value * scale
        c.setStrokeColor(RED)
        c.setLineWidth(1.0)
        c.line(xx, axis_y, xx, yy)
        c.setFillColor(RED)
        c.circle(xx, yy, 2.2, stroke=0, fill=1)
        c.setFillColor(BLUE_DARK)
        c.setFont('CN', 5.8)
        c.drawCentredString(xx, axis_y - 9, str(index))
    center_x = x0 + center * step
    c.setStrokeColor(colors.HexColor('#333333'))
    c.setDash(3, 2)
    c.line(center_x, y + 7, center_x, y + h - 7)
    c.setDash()


def _draw_amplitude_panel(c, x, y, w, h, kind, name, frame):
    c.setStrokeColor(frame)
    c.setLineWidth(1.25)
    c.rect(x, y, w, h, stroke=1, fill=0)
    x0, axis_y = x + 18, y + h * 0.46
    arrow(c, x0, axis_y, x + w - 10, axis_y, colors.black, 0.85, head=4)
    arrow(c, x0, y + 10, x0, y + h - 9, colors.black, 0.85, head=4)
    c.setFillColor(TEXT)
    c.setFont('CNB', 8)
    draw_auto_math_text(c,x0+3,y+h-13,'H(ω)',font='CNB',size=8)
    c.drawRightString(x + w - 3, axis_y - 12, 'ω')
    c.setFont('CN', 6.2)
    c.drawString(x0 + 1, axis_y - 10, '0')
    c.drawCentredString(x0 + (w - 32) / 2, axis_y - 10, 'π')
    c.drawRightString(x + w - 14, axis_y - 10, '2π')
    c.setStrokeColor(RED)
    c.setLineWidth(1.35)
    points = []
    for index in range(121):
        t = 2 * math.pi * index / 120
        if kind == 'type_i':
            value = 0.45 * math.cos(t) + 0.18 * math.cos(3 * t) + 0.12
        elif kind == 'type_ii':
            value = (0.5 * math.cos(t / 2) + 0.16 * math.cos(5 * t / 2))
        elif kind == 'type_iii':
            value = 0.62 * math.sin(t)
        else:
            value = 0.54 * math.sin(t / 2) + 0.12 * math.sin(5 * t / 2)
        px = x0 + (w - 32) * index / 120
        py = axis_y + value * h * 0.42
        points.append((px, py))
    path = c.beginPath()
    path.moveTo(*points[0])
    for point in points[1:]:
        path.lineTo(*point)
    c.drawPath(path, stroke=1, fill=0)
    forced = {'type_ii': (math.pi,), 'type_iii': (0, math.pi), 'type_iv': (0,)}[kind] if kind != 'type_i' else ()
    c.setStrokeColor(colors.HexColor('#333333'))
    c.setDash(3, 2)
    for omega in forced:
        xx = x0 + (w - 32) * omega / (2 * math.pi)
        c.line(xx, y + 7, xx, y + h - 7)
    c.setDash()
    annotation = linear_phase_fir_source_table()[kind]['plot_annotation']
    if annotation:
        c.setFillColor(TEXT)
        c.setFont('CNB', 7.2)
        c.drawRightString(x + w - 7, y + h - 14, annotation.replace('pi', 'π'))


def _draw_phase_panel(c, x, y, w, h, antisymmetric, name):
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.25)
    c.rect(x, y, w, h, stroke=1, fill=0)
    x0, axis_y = x + 28, y + h * 0.68
    arrow(c, x + 8, axis_y, x + w - 10, axis_y, colors.black, 0.85, head=4)
    arrow(c, x0, y + 10, x0, y + h - 9, colors.black, 0.85, head=4)
    c.setFillColor(TEXT)
    c.setFont('CNB', 8.5)
    draw_auto_math_text(c,x0+3,y+h-15,'θ(ω)',font='CNB',size=8.5)
    draw_auto_math_text(c,x+w-3,axis_y-12,'ω(rad)',font='CNB',size=8.5,align='right')
    c.setFont('CN', 7)
    c.drawString(x0 - 8, axis_y + 5, '0')
    c.drawCentredString(x0 + (w - 48) / 2, axis_y + 5, 'π')
    c.drawRightString(x + w - 29, axis_y + 5, '2π')
    start_y = axis_y + (18 if antisymmetric else 0)
    end_y = y + 30
    c.setStrokeColor(RED)
    c.setLineWidth(1.5)
    c.line(x0, start_y, x + w - 36, end_y)
    c.setStrokeColor(BLUE_DARK)
    c.setDash(3, 2)
    c.line(x + w - 36, end_y, x + w - 36, axis_y)
    c.line(x0, end_y, x + w - 36, end_y)
    c.setDash()
    draw_math_at(c, r'\frac{\pi}{2}' if antisymmetric else r'0', x + 4, start_y + 2, 28, 15, 8.8, name=f'{name}_start')
    end_expr = r'-\pi\left(N-\frac{3}{2}\right)' if antisymmetric else r'-\pi(N-1)'
    draw_math_at(c, end_expr, x0 + 5, end_y - 10, 92, 18, 8.2, name=f'{name}_end')


def draw_linear_phase_critical_page(doc, antisymmetric=False):
    """Redraw one full source page from PPT 365/366 without omitting blocks."""
    doc.new_page()
    c = doc.c
    page_tag = 'odd_symmetry' if antisymmetric else 'even_symmetry'
    c.setFillColor(RED)
    c.setFont('CNB', 17)
    c.drawCentredString(MARGIN_X + CONTENT_W / 2, doc.y - 8,
                        '本节最重要的两张表！！！（记住这两张表，用于设计 FIR）')
    divider_x = MARGIN_X + 190
    c.setStrokeColor(colors.HexColor('#36A544'))
    c.setLineWidth(1.8)
    c.line(divider_x, 72, divider_x, doc.y - 34)
    left_x = MARGIN_X + 8
    c.setFillColor(TEXT)
    c.setFont('CNB', 16)
    c.drawCentredString(left_x + 82, doc.y - 78, '二类线性相位' if antisymmetric else '一类线性相位')
    draw_math_at(c, r'h(n)=-h(N-1-n)' if antisymmetric else r'h(n)=h(N-1-n)',
                 left_x + 4, doc.y - 158, 166, 34, 17, name=f'{page_tag}_symmetry')
    arrow(c, left_x + 82, doc.y - 111, left_x + 82, doc.y - 132, colors.HexColor('#8CB5E8'), 1.2, head=5)
    arrow(c, left_x + 82, doc.y - 183, left_x + 82, doc.y - 207, colors.HexColor('#8CB5E8'), 1.2, head=5)
    phase_expr = (r'\theta(\omega)=\pm\frac{\pi}{2}-\frac{N-1}{2}\omega'
                  if antisymmetric else r'\theta(\omega)=-\frac{N-1}{2}\omega')
    draw_math_at(c, phase_expr, left_x, doc.y - 247, 175, 40, 16, name=f'{page_tag}_phase_eq')
    _draw_phase_panel(c, left_x + 2, 115, 170, 145, antisymmetric, f'{page_tag}_phase')

    right_x = divider_x + 18
    panel_w = 165
    formula_x = right_x + panel_w + 16
    table = linear_phase_fir_source_table()
    upper_type = 'type_iii' if antisymmetric else 'type_i'
    lower_type = 'type_iv' if antisymmetric else 'type_ii'
    upper_y, lower_y = 487, 198
    frame_upper = colors.HexColor('#C739B7')
    frame_lower = colors.HexColor('#168CD2')

    for block_y, type_key, parity, frame in (
        (upper_y, upper_type, 'N 为奇数', frame_upper),
        (lower_y, lower_type, 'N 为偶数', frame_lower),
    ):
        c.setFillColor(TEXT)
        c.setFont('CNB', 14)
        c.drawString(right_x, block_y + 224, parity)
        _draw_checklist(c, formula_x - 5, block_y + 219,
                        table[type_key]['filters'], f'{page_tag}_{type_key}_checklist')
        if type_key == 'type_i':
            values = (.6, .3, .7, -.4, .3, .8, .3, -.4, .7, .3, .6); center = 5
        elif type_key == 'type_ii':
            values = (.6, .3, .7, -.4, .3, .3, -.4, .7, .3, .6); center = 4.5
        elif type_key == 'type_iii':
            values = (.6, .3, .7, -.4, .3, 0, -.3, .4, -.7, -.3, -.6); center = 5
        else:
            values = (.6, .3, .7, -.4, .3, -.3, .4, -.7, -.3, -.6); center = 4.5
        _draw_impulse_panel(c, right_x, block_y + 128, panel_w, 72,
                            values, center, f'{page_tag}_{type_key}_impulse', frame)
        _draw_amplitude_panel(c, right_x, block_y + 23, panel_w, 92,
                              type_key, f'{page_tag}_{type_key}_amplitude', frame)

        if type_key == 'type_i':
            coeff = r'a(0)=h\left(\frac{N-1}{2}\right),\quad a(n)=2h\left(\frac{N-1}{2}-n\right)'
            transform = r'H(\omega)=\sum_{n=0}^{\frac{N-1}{2}}a(n)\cos(\omega n)'
            conclusion = 'H(ω) 对 ω=0、π、2π 呈偶对称'
        elif type_key == 'type_ii':
            coeff = r'b(n)=2h\left(\frac{N}{2}-n\right),\quad n\in\left[1,\frac{N}{2}\right]'
            transform = r'H(\omega)=\sum_{n=1}^{\frac{N}{2}}b(n)\cos\left[\omega\left(n-\frac{1}{2}\right)\right]'
            conclusion = 'H(ω) 对 ω=π 呈奇对称'
        elif type_key == 'type_iii':
            coeff = r'c(n)=2h\left(\frac{N-1}{2}-n\right),\quad n\in\left[1,\frac{N-1}{2}\right]'
            transform = r'H(\omega)=\sum_{n=1}^{\frac{N-1}{2}}c(n)\sin(\omega n)'
            conclusion = 'H(ω) 对 ω=0、π、2π 呈奇对称'
        else:
            coeff = r'd(n)=2h\left(\frac{N}{2}-n\right),\quad n\in\left[1,\frac{N}{2}\right]'
            transform = r'H(\omega)=\sum_{n=1}^{\frac{N}{2}}d(n)\sin\left[\omega\left(n-\frac{1}{2}\right)\right]'
            conclusion = 'H(ω) 对 ω=π 呈偶对称'
        draw_math_at(c, coeff, formula_x, block_y + 166, 142, 42, 9.5,
                     name=f'{page_tag}_{type_key}_coeff')
        if type_key == 'type_i':
            c.setFillColor(TEXT)
            c.setFont('CN', 7.2)
            c.drawRightString(formula_x + 142, block_y + 146, '（其余 n）')
        c.setStrokeColor(colors.HexColor('#2A92C8'))
        c.setLineWidth(1.1)
        c.rect(formula_x, block_y + 72, 142, 56, stroke=1, fill=0)
        draw_math_at(c, transform, formula_x + 4, block_y + 100, 134, 42, 9.4,
                     name=f'{page_tag}_{type_key}_transform')
        c.setFillColor(colors.HexColor('#C23A40'))
        c.setFont('CNB', 9.3)
        c.drawString(formula_x, block_y + 47, conclusion)
    c.setStrokeColor(colors.HexColor('#36A544'))
    c.setLineWidth(1.7)
    c.line(divider_x, 472, MARGIN_X + CONTENT_W, 472)
    doc.y = 60


def fir_tap_diagram(doc, title='FIR 直接型结构', taps=None):
    taps=taps or [r'h(0)', r'h(1)', r'h(2)', r'\cdots', r'h(N-1)']
    h=160
    doc.ensure(h+10)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X, top-14, title)
    x=MARGIN_X+60; y=top-56; branch_y=y-76
    draw_math_at(c,r'x(n)',x-48,y+8,45,18,12,name='fir_x')
    arrow(c,x,y,x+395,y,RED,1.25)
    for i,lab in enumerate(taps):
        xx=x+45+i*75
        dot(c,xx,y,3,RED)
        if i < len(taps)-1:
            delay_box(c,xx+14,y,30,18,r'z^{-1}')
        arrow(c,xx,y,xx,branch_y,RED,1.05)
        draw_math_at(c,lab,xx-18,y-38,54,18,10,name=f'tap_{i}_{title}')
        dot(c,xx,branch_y,3,RED)
        if i:
            arrow(c,xx-75,branch_y,xx,branch_y,RED,1.05)
    sum_node(c,x+45+(len(taps)-1)*75+26,branch_y,10,RED)
    arrow(c,x+45+(len(taps)-1)*75+36,branch_y,x+45+(len(taps)-1)*75+86,branch_y,RED,1.1)
    draw_math_at(c,r'y(n)',x+45+(len(taps)-1)*75+90,branch_y+8,45,18,12,name='fir_y')
    doc.y=top-h


def cascade_diagram(doc):
    h=145
    doc.ensure(h+10)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X, top-14, 'FIR 级联型结构')
    x=MARGIN_X+55; y=top-76
    draw_math_at(c,r'x(n)',x-45,y+8,42,17,12,name='casfir_x')
    for i,lab in enumerate([r'H_1(z)',r'H_2(z)',r'\cdots',r'H_K(z)']):
        bx=x+i*105
        arrow(c,bx-34 if i==0 else bx-43,y,bx,y,RED,1.1)
        c.setStrokeColor(RED); c.rect(bx,y-18,62,36,stroke=1,fill=0)
        draw_math_at(c,lab,bx+8,y,48,18,11,name=f'casfir_{i}')
    arrow(c,x+3*105+62,y,x+3*105+100,y,RED,1.1)
    draw_math_at(c,r'y(n)',x+3*105+105,y+8,42,17,12,name='casfir_y')
    doc.y=top-h


def freq_sampling_flow(doc):
    h=220
    doc.ensure(h+10)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-14,'频率采样定理')
    x=MARGIN_X+130; y=top-62
    # Same four-node transform relationship as the original 6.2 reference figure.
    draw_math_at(c,r'x_M(n)',x,y+8,72,22,15,name='fsm_xm')
    draw_math_at(c,r'X(e^{j\omega})',x+285,y+8,92,22,15,name='fsm_xw')
    arrow(c,x+78,y,x+265,y,colors.HexColor('#D100D8'),1.4)
    c.setFillColor(colors.HexColor('#146B36')); c.setFont('CNB',16)
    c.drawCentredString(x+170,y+18,'序列傅立叶变换')
    c.setStrokeColor(RED); c.setFillColor(YELLOW); c.rect(x+18,y-84,62,44,stroke=1,fill=1)
    draw_centered_multiline_text(c, x+49, y-62, 'N≥M', 'CNB', 16, color=BLUE_DARK)
    arrow(c,x+49,y-40,x+49,y-18,RED,1.2); arrow(c,x+49,y-84,x+49,y-108,RED,1.2)
    draw_math_at(c,r'x_N(n)',x,y-122,72,22,15,name='fsm_xn')
    draw_math_at(c,r'X(k)',x+286,y-122,60,22,15,name='fsm_xk')
    arrow(c,x+265,y-114,x+82,y-114,colors.HexColor('#D100D8'),1.4)
    c.setFillColor(colors.HexColor('#146B36')); c.setFont('CNB',16)
    c.drawCentredString(x+174,y-98,'离散傅立叶反变换')
    arrow(c,x+305,y-18,x+305,y-86,colors.HexColor('#D100D8'),1.4)
    c.setFillColor(RED); c.setFont('CNB',11)
    c.drawString(x+320,y-45,'单位圆上取 N 点')
    c.drawString(x+335,y-61,'（频域采样）')
    c.setFillColor(TEXT); c.setFont('CNB',12)
    c.drawCentredString(x+34,y+30,'M点'); c.drawCentredString(x+34,y-148,'N点')
    doc.y=top-h


def fir_direct_example(doc):
    """Source pages 340/356: four-tap direct-form realization."""
    h=155
    doc.ensure(h+8)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK)
    c.drawString(MARGIN_X,top-14,'例：直接型 FIR 结构')
    x=MARGIN_X+115; y=top-55; bus=y-72; step=82
    draw_math_at(c,r'x(n)',x-52,y+8,45,18,11,name='direct_ex_x')
    arrow(c,x-8,y,x+3*step+68,y,RED,1.15)
    coeffs=[r'0.96',r'2',r'2.8',r'1.5']
    for i,a in enumerate(coeffs):
        xx=x+i*step
        dot(c,xx,y,2.8,RED)
        if i<3:
            delay_box(c,xx+27,y,32,18,r'z^{-1}')
        c.setStrokeColor(RED); c.rect(xx-19,y-48,38,22,stroke=1,fill=0)
        draw_math_at(c,a,xx-15,y-32,30,15,9.5,name=f'direct_ex_a{i}')
        arrow(c,xx,y,xx,y-26,RED,1.0)
        arrow(c,xx,y-48,xx,bus,RED,1.0)
        dot(c,xx,bus,2.5,RED)
        if i:
            c.line(xx-step,bus,xx,bus)
    sum_node(c,x+3*step+28,bus,10,RED)
    arrow(c,x+3*step,bus,x+3*step+18,bus,RED,1.0)
    arrow(c,x+3*step+38,bus,x+3*step+78,bus,RED,1.0)
    draw_math_at(c,r'y(n)',x+3*step+82,bus+8,42,17,11,name='direct_ex_y')
    doc.y=top-h


def fir_cascade_example(doc):
    """Source page 341: two source-ordered second/first-order sections."""
    h=145
    doc.ensure(h+8)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK)
    c.drawString(MARGIN_X,top-14,'例：级联型 FIR 结构')
    x=MARGIN_X+95; y=top-62
    draw_math_at(c,r'x(n)',x-50,y+8,42,17,11,name='cascade_ex_x')
    arrow(c,x-8,y,x+395,y,RED,1.15)
    for base, vals in [(x+40,[r'0.6',r'0.5']), (x+235,[r'1.6',r'2',r'3'])]:
        dot(c,base,y,2.8,RED)
        c.setStrokeColor(RED); c.line(base,y,base,y-62)
        for j,val in enumerate(vals):
            yy=y-14-j*24
            delay_box(c,base+28,yy,28,16,r'z^{-1}') if j else None
            draw_math_at(c,val,base+64,yy+5,32,14,9,name=f'cascade_ex_{base}_{j}')
            c.line(base+56,yy,base+112,yy)
        c.line(base+112,y-62,base+112,y)
        arrow(c,base+112,y,base+145,y,RED,1.0)
    draw_math_at(c,r'y(n)',x+405,y+8,42,17,11,name='cascade_ex_y')
    doc.y=top-h


def frequency_sampling_network(doc):
    h=280
    doc.ensure(h+10)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK)
    c.drawString(MARGIN_X,top-14,'频率采样结构流图')
    x=MARGIN_X+75; y=top-50; right=x+390
    draw_math_at(c,r'x(n)',x-48,y+8,44,18,12,name='fsn_x')
    arrow(c,x,y,right,y,RED,1.15)
    # Comb path 1-z^-N at the left, with the -1 return exactly as in the PPT.
    comb_l=x+34; comb_r=x+92; comb_y=y-38
    dot(c,comb_l,y,2.8,RED); dot(c,comb_r,y,2.8,RED)
    c.setStrokeColor(RED); c.line(comb_l,y,comb_l,comb_y); c.line(comb_l,comb_y,comb_r,comb_y)
    arrow(c,comb_r,comb_y,comb_r,y,RED,1.0)
    draw_math_at(c,r'z^{-N}',comb_l+10,comb_y-8,42,15,9.5,name='fsn_comb_delay')
    draw_math_at(c,r'-1',comb_r+4,comb_y+12,28,14,9.5,name='fsn_comb_gain')
    branch_left=x+160; branch_right=x+315
    c.line(branch_left,y,branch_left,y-190); c.line(branch_right,y,branch_right,y-190)
    labels=[r'H(0)',r'H(1)',r'\vdots',r'H(N-1)']
    gains=[r'W_N^{0}',r'W_N^{-1}',r'',r'W_N^{-(N-1)}']
    ys=[y-8,y-64,y-116,y-172]
    for i,(lab,gain,yy) in enumerate(zip(labels,gains,ys)):
        if lab==r'\vdots':
            draw_math_at(c,lab,branch_left+66,yy+8,25,25,13,name='fsn_dots')
            continue
        c.setStrokeColor(RED); c.line(branch_left,yy,branch_right,yy)
        # Resonator triangular loop: W_N^-k and z^-1.
        apex=branch_right-40
        c.line(apex,yy,branch_right-8,yy-30)
        c.line(branch_right-8,yy-30,branch_right-8,yy)
        arrow(c,branch_right-8,yy,apex,yy,RED,0.95)
        draw_math_at(c,gain,apex-20,yy-21,58,16,9.5,name=f'fsn_gain_{i}')
        draw_math_at(c,r'z^{-1}',branch_right-5,yy-18,36,15,9.5,name=f'fsn_delay_{i}')
        draw_math_at(c,lab,branch_right-52,yy+13,62,17,10.5,name=f'fsn_h_{i}')
    arrow(c,branch_right,y,right,y,RED,1.05)
    draw_math_at(c,r'\frac{1}{N}',right-26,y+15,42,18,11,name='fsn_output_gain')
    draw_math_at(c,r'y(n)',right+8,y+8,44,18,12,name='fsn_y')
    doc.y=top-h


def comb_and_resonator(doc):
    doc.p('频率采样型结构由两部分级联：梳状滤波器和由 N 个谐振器组成的谐振柜。')
    draw_formula_block(doc,r'H(z)=(1-z^{-N})\frac{1}{N}\sum_{k=0}^{N-1}\frac{H(k)}{1-W_N^kz^{-1}}','fs_formula',fontsize=15,max_h=50)
    draw_formula_block(doc,r'H_1(z)=1-z^{-N},\qquad |H_1(e^{j\omega})|=2\left|\sin\frac{\omega N}{2}\right|','comb_formula',fontsize=15,max_h=42)
    draw_note(doc,'结构修正', ['梳状滤波器的零点会抵消谐振柜中的极点；为改善有限字长下的不稳定，可把半径从 1 改为 r，使极点移入单位圆。'])
    draw_formula_block(doc,r'H(z)=(1-r^Nz^{-N})\frac{1}{N}\sum_{k=0}^{N-1}\frac{H_r(k)}{1-rW_N^kz^{-1}},\qquad z_k=re^{j\frac{2\pi k}{N}}','fs_correct',fontsize=13,max_h=50)


def comb_response_geometry():
    return {
        'curve_baseline_offset': 0,
        'axis_y': 0,
        'zero_y': 0,
    }


def comb_response_points(width, height, lobes=8, samples_per_lobe=24):
    points = []
    for lobe in range(lobes):
        start = 0 if lobe == 0 else 1
        for sample in range(start, samples_per_lobe + 1):
            phase = sample / samples_per_lobe
            x = width * (lobe + phase) / lobes
            y = 0 if sample in (0, samples_per_lobe) else height * math.sin(math.pi * phase)
            points.append((x, y))
    return points


def comb_response_figure(doc):
    """Source page 344: unit-circle zeros and the comb magnitude response."""
    h=190
    doc.ensure(h+8)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK)
    c.drawString(MARGIN_X,top-14,'梳状滤波器零极点与幅频响应')
    cx=MARGIN_X+145; cy=top-92; r=48
    c.setStrokeColor(BLUE); c.setLineWidth(1.1); c.circle(cx,cy,r,stroke=1,fill=0)
    arrow(c,cx-r-28,cy,cx+r+34,cy,colors.black,0.9)
    arrow(c,cx,cy-r-24,cx,cy+r+28,colors.black,0.9)
    for k in range(8):
        import math
        px=cx+r*math.cos(2*math.pi*k/8); py=cy+r*math.sin(2*math.pi*k/8)
        c.setStrokeColor(RED); c.circle(px,py,4,stroke=1,fill=0)
    c.setStrokeColor(RED); c.line(cx-6,cy-6,cx+6,cy+6); c.line(cx-6,cy+6,cx+6,cy-6)
    x0=MARGIN_X+318; y0=top-145; w=205; hh=92
    arrow(c,x0,y0,x0+w,y0,colors.black,0.9); arrow(c,x0,y0,x0,y0+hh,colors.black,0.9)
    c.setStrokeColor(RED); c.setLineWidth(1.2)
    import math
    geometry = comb_response_geometry()
    curve_base = y0 + geometry['curve_baseline_offset']
    pts=[(x0+px, curve_base+py) for px,py in comb_response_points(w,68)]
    p=c.beginPath(); p.moveTo(*pts[0])
    for pt in pts[1:]: p.lineTo(*pt)
    c.drawPath(p,stroke=1,fill=0)
    for frac,lab in [(0,'0'),(.5,r'\pi'),(1,r'2\pi')]:
        draw_math_at(c,lab,x0+w*frac-10,y0-10,28,14,9,name=f'comb_axis_{frac}')
    draw_math_at(c,r'|H_1(e^{j\omega})|',x0+6,y0+hh+4,92,17,10,name='comb_mag_label')
    doc.y=top-h


def linear_phase_network(doc, kind='even'):
    h=224
    doc.ensure(h+10)
    c=doc.c; top=doc.y
    title='N 为奇数的线性相位 FIR 结构' if kind=='odd' else 'N 为偶数的线性相位 FIR 结构'
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK); c.drawString(MARGIN_X,top-14,title)
    x=MARGIN_X+62; y=top-54
    mid=y-68; bus=y-124
    draw_math_at(c,r'x(n)',x-50,y+8,42,17,12,name=f'lpnx_{kind}')
    stages=4
    step=86
    xs=[x+i*step for i in range(stages+1)]
    arrow(c,x-12,y,xs[-1]+20,y,RED,1.15)
    for i,xx in enumerate(xs):
        dot(c,xx,y,2.8,RED)
        if i<stages:
            delay_box(c,xx+28,y,30,17,r'z^{-1}')
    # Reverse delay rail and the right-hand turnaround match the source figure.
    c.setStrokeColor(RED); c.setLineWidth(1.05)
    c.line(xs[0],mid,xs[-1],mid)
    for i in range(stages):
        delay_box(c,xs[i]+28,mid,30,17,r'z^{-1}')
    arrow(c,xs[-1],y,xs[-1],mid,RED,1.0)
    # Symmetric/antisymmetric folded pairs feed coefficient taps.
    tap_count=4 if kind=='odd' else 5
    tap_xs=[xs[0]+i*(xs[-1]-xs[0])/(tap_count-1) for i in range(tap_count)]
    for i,tx in enumerate(tap_xs):
        mate=xs[-1]-min(i,stages-i)*step
        source_x=xs[min(i,stages)]
        c.setStrokeColor(RED); c.line(source_x,y,tx,mid)
        sign=r'+1' if kind=='odd' else r'\pm1'
        draw_math_at(c,sign,tx+3,mid+18,34,14,9.5,name=f'fold_sign_{kind}_{i}')
        arrow(c,tx,mid,tx,bus,RED,1.0)
        coeff = (r'h\left(\frac{N-1}{2}\right)' if kind=='odd' and i==tap_count-1
                 else (r'h\left(\frac{N}{2}-1\right)' if kind=='even' and i==tap_count-2
                       else (r'h\left(\frac{N}{2}\right)' if kind=='even' and i==tap_count-1
                             else rf'h({i})')))
        draw_math_at(c,coeff,tx-18,mid-29,64,17,9.5,name=f'fold_coeff_{kind}_{i}')
        dot(c,tx,bus,2.6,RED)
    c.line(tap_xs[0],bus,tap_xs[-1]+46,bus)
    arrow(c,tap_xs[-1]+46,bus,tap_xs[-1]+88,bus,RED,1.1)
    draw_math_at(c,r'y(n)',tap_xs[-1]+92,bus+8,42,17,12,name=f'lpny_{kind}')
    doc.y=top-h


def linear_phase_reduction_example(doc):
    """Source pages 356-357: direct and symmetry-reduced five-tap FIR."""
    h = 305
    doc.ensure(h + 10)
    c = doc.c
    top = doc.y
    c.setFillColor(BLUE_DARK)
    c.setFont('CNB', 10)
    c.drawString(MARGIN_X, top - 14, '例：线性相位结构化简')
    draw_math_at(
        c, r'H(z)=\frac{1}{10}(1+0.9z^{-1}+2.1z^{-2}+0.9z^{-3}+z^{-4})',
        MARGIN_X + 94, top - 38, CONTENT_W - 150, 26, 12.5, name='linear_reduce_hz'
    )

    c.setFillColor(TEXT)
    c.setFont('CNB', 9.2)
    c.drawString(MARGIN_X + 10, top - 62, '直接型结构')
    x = MARGIN_X + 98
    y = top - 86
    bus = y - 52
    step = 82
    draw_math_at(c, r'x(n)', x - 54, y + 8, 42, 17, 11, name='linear_direct_x')
    # linear_direct_input_arrow
    arrow(c, x - 34, y, x, y, RED, 1.0)
    draw_math_at(c, r'\frac{1}{10}', x - 16, y + 19, 38, 18, 11, name='linear_direct_scale')
    coeffs = [r'1', r'0.9', r'2.1', r'0.9', r'1']
    for index, coeff in enumerate(coeffs):
        xx = x + index * step
        dot(c, xx, y, 2.5, RED)
        if index < 4:
            arrow(c, xx, y, xx + step, y, RED, 1.0)
            draw_math_at(c, r'z^{-1}', xx + 28, y + 14, 28, 14, 8.8, name=f'linear_direct_delay_{index}')
        arrow(c, xx, y - 2, xx, bus, RED, 0.95)
        draw_math_at(c, coeff, xx + 7, (y + bus) / 2, 30, 14, 9.2, name=f'linear_direct_coeff_{index}')
    c.setStrokeColor(RED)
    c.setLineWidth(1.0)
    c.line(x, bus, x + 4 * step + 40, bus)
    arrow(c, x + 4 * step + 40, bus, x + 4 * step + 72, bus, RED, 1.0)
    draw_math_at(c, r'y(n)', x + 4 * step + 76, bus + 8, 42, 17, 11, name='linear_direct_y')

    c.setFillColor(TEXT)
    c.setFont('CNB', 9.2)
    c.drawString(MARGIN_X + 10, top - 164, '线性相位结构')
    draw_math_at(
        c, r'h(n)=\{1,0.9,2.1,0.9,1\}',
        MARGIN_X + 225, top - 164, 175, 18, 10.5, name='linear_sym_sequence'
    )
    x = MARGIN_X + 116
    y = top - 194
    mid = y - 40
    bus = y - 92
    step = 122
    draw_math_at(c, r'x(n)', x - 58, y + 8, 42, 17, 11, name='linear_sym_x')
    # linear_sym_input_arrow
    arrow(c, x - 34, y, x, y, RED, 1.0)
    draw_math_at(c, r'\frac{1}{10}', x - 18, y + 19, 38, 18, 11, name='linear_sym_scale')
    for index in range(3):
        xx = x + index * step
        dot(c, xx, y, 2.5, RED)
        if index < 2:
            arrow(c, xx, y, xx + step, y, RED, 1.0)
            draw_math_at(c, r'z^{-1}', xx + 44, y + 14, 30, 14, 8.8, name=f'linear_sym_top_delay_{index}')
    c.setStrokeColor(RED)
    c.line(x + 2 * step, y, x + 2 * step, mid)
    arrow(c, x + 2 * step, mid, x + step, mid, RED, 1.0)
    arrow(c, x + step, mid, x, mid, RED, 1.0)
    draw_math_at(c, r'z^{-1}', x + step + 42, mid + 14, 30, 14, 8.8, name='linear_sym_mid_delay_1')
    draw_math_at(c, r'z^{-1}', x + 42, mid + 14, 30, 14, 8.8, name='linear_sym_mid_delay_0')
    for index, coeff in enumerate((r'1', r'0.9', r'2.1')):
        xx = x + index * step
        arrow(c, xx, y - 2, xx, bus, RED, 0.95)
        draw_math_at(c, coeff, xx + 8, (mid + bus) / 2, 30, 14, 9.2, name=f'linear_sym_coeff_{index}')
    c.line(x, bus, x + 2 * step + 52, bus)
    arrow(c, x + 2 * step + 52, bus, x + 2 * step + 84, bus, RED, 1.0)
    draw_math_at(c, r'y(n)', x + 2 * step + 88, bus + 8, 42, 17, 11, name='linear_sym_y')
    doc.y = top - h


def linear_phase_table(doc):
    rows=[
        ['类别','N','h(n) 对称性','H(ω) 对称性','可实现滤波器'],
        ['一类','奇数','偶对称','关于 0, π, 2π 偶对称','LP、HP、BP、BS'],
        ['二类','偶数','偶对称','关于 π 奇对称','LP、BP'],
        ['三类','奇数','奇对称','关于 0, π, 2π 奇对称','BP'],
        ['四类','偶数','奇对称','关于 π 偶对称','HP、BP'],
    ]
    row_h=31; h=row_h*len(rows)+8
    doc.ensure(h+12)
    c=doc.c; top=doc.y
    widths=[50,42,125,170,CONTENT_W-387]
    y=top
    for r,row in enumerate(rows):
        y-=row_h
        c.setFillColor(BLUE_DARK if r==0 else (colors.HexColor('#F7F9FC') if r%2 else colors.white))
        c.rect(MARGIN_X,y,CONTENT_W,row_h,stroke=0,fill=1)
        x=MARGIN_X
        for ci,w in enumerate(widths):
            if ci>0:
                c.setStrokeColor(colors.HexColor('#CADCEB')); c.line(x,y,x,y+row_h)
            c.setFillColor(colors.white if r==0 else TEXT)
            c.setFont('CNB' if r==0 or ci==0 else 'CN',8.2)
            parts=wrap(row[ci],w-8,'CNB' if r==0 or ci==0 else 'CN',8.2)
            yy=y+row_h-13
            for part in parts[:2]:
                c.drawString(x+4,yy,part); yy-=11
            x+=w
    c.setStrokeColor(colors.HexColor('#CADCEB')); c.rect(MARGIN_X,top-row_h*len(rows),CONTENT_W,row_h*len(rows),stroke=1,fill=0)
    doc.y=top-h-10


def amplitude_phase_explainer(doc):
    """Source pages 359-361: amplitude response and constant-delay signal path."""
    h=235
    doc.ensure(h+8)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK)
    c.drawString(MARGIN_X,top-14,'幅频响应与线性相位的作用')
    draw_math_at(c,r'|Y(e^{j\omega})|=|X(e^{j\omega})||H(e^{j\omega})|,\qquad y(n)=x(n-\tau)',
                 MARGIN_X+90,top-48,CONTENT_W-180,30,13,name='amp_phase_relation')
    x=MARGIN_X+65; y=top-112
    labels=[r'x(n)',r'X(e^{j\omega})',r'H(e^{j\omega})',r'Y(e^{j\omega})',r'y(n)']
    widths=[52,82,86,82,52]
    xx=x
    for i,(lab,w) in enumerate(zip(labels,widths)):
        c.setStrokeColor(RED); c.rect(xx,y-19,w,38,stroke=1,fill=0)
        draw_math_at(c,lab,xx+4,y+3,w-8,18,10,name=f'amp_phase_{i}')
        if i<len(labels)-1: arrow(c,xx+w,y,xx+w+28,y,RED,1.0)
        xx+=w+28
    c.setFillColor(RED); c.setFont('CNB',10)
    c.drawString(x+175,y-52,'幅度决定各频率分量的通过比例；线性相位保证恒定群延迟。')
    doc.y=top-h


def linear_phase_four_cases(doc):
    """Source pages 363-366: all four amplitude/phase cases as actual plots."""
    h=500
    doc.ensure(h+8)
    c=doc.c; top=doc.y
    c.setFont('CNB',10); c.setFillColor(BLUE_DARK)
    c.drawString(MARGIN_X,top-14,'四类线性相位 FIR 的振幅响应特征')
    import math
    cases=[('一类：N 奇数，偶对称','LP / HP / BP / BS',False,False,r'H(\omega)=h(M)+2\sum_{n=0}^{M-1}h(n)\cos[\omega(M-n)]'),
           ('二类：N 偶数，偶对称','LP / BP，ω=π 必为零',False,True,r'H(\omega)=2\sum_{n=0}^{M}h(n)\cos[\omega(M+\frac{1}{2}-n)]'),
           ('三类：N 奇数，奇对称','BP，ω=0、π 必为零',True,True,r'H(\omega)=2j\sum_{n=0}^{M-1}h(n)\sin[\omega(M-n)]'),
           ('四类：N 偶数，奇对称','HP / BP，ω=0 必为零',True,False,r'H(\omega)=2j\sum_{n=0}^{M}h(n)\sin[\omega(M+\frac{1}{2}-n)]')]
    for idx,(title,note,zero0,zeropi,formula) in enumerate(cases):
        col=idx%2; row=idx//2
        x=MARGIN_X+col*275; y=top-70-row*220; w=220; hh=95
        c.setFillColor(BLUE_DARK); c.setFont('CNB',10); c.drawString(x,y+32,title)
        arrow(c,x,y-hh,x+w,y-hh,colors.black,0.85); arrow(c,x,y-hh,x,y+6,colors.black,0.85)
        c.setStrokeColor(RED); c.setLineWidth(1.25)
        pts=[]
        for i in range(121):
            t=math.pi*i/120
            if zero0 and zeropi: val=abs(math.sin(t))
            elif zero0: val=abs(math.sin(t/2))
            elif zeropi: val=abs(math.cos(t/2))
            else: val=.35+.55*abs(math.cos(1.5*t))
            pts.append((x+w*i/120,y-hh+75*val))
        p=c.beginPath(); p.moveTo(*pts[0])
        for pt in pts[1:]: p.lineTo(*pt)
        c.drawPath(p,stroke=1,fill=0)
        draw_math_at(c,r'0',x-6,y-hh-10,22,13,8.5,name=f'lp4_0_{idx}')
        draw_math_at(c,r'\pi',x+w-8,y-hh-10,22,13,8.5,name=f'lp4_pi_{idx}')
        c.setFillColor(TEXT); c.setFont('CN',8.5); c.drawString(x,y-hh-28,note)
        draw_math_at(c,formula,x,y-hh-48,w,20,9.2,name=f'lp4_formula_{idx}')
    doc.y=top-h


def build():
    register_fonts()
    doc=Doc(PDF_PATH)
    doc.section='第六章 FIR滤波器设计'
    doc.start()
    doc.h1('第六章 FIR系统的网络结构与滤波器设计')
    doc.p('本章讨论 FIR 数字滤波器的基本网络结构、频率采样结构和线性相位结构。原课件封面和目录转为章节导读，正文按小节连续排版。')
    doc.bullet(['FIR 基本网络结构：直接型、级联型。','FIR 频率采样结构：梳状滤波器、谐振柜及修正方法。','FIR 线性相位结构：单位脉冲响应对称性、四类线性相位条件和可实现滤波器类型。'])

    doc.h2('6.1 FIR 基本网络结构')
    doc.p('FIR 系统的单位脉冲响应 h(n) 只有有限个值不为零，因此 h(n) 是有限长序列。系统因果时，H(z) 在 |z|>0 处收敛，极点全部在 z=0 处。FIR 一定为稳定系统。FIR 结构主要是非递归结构，没有输出到输入的反馈；频率采样结构中虽含反馈支路，但整体仍为非递归系统。')
    draw_formula_block(doc,r'H(z)=\sum_{n=0}^{N-1}h(n)z^{-n}=\frac{\sum_{i=0}^{M}b_iz^{-i}}{1}','fir_hz',fontsize=16,max_h=42)
    draw_formula_block(doc,r'y(n)=x(n)*h(n)=\sum_{m=0}^{N-1}h(m)x(n-m)','fir_diff',fontsize=16,max_h=40)
    fir_tap_diagram(doc,'FIR 直接型结构')
    draw_note(doc,'直接型特点',['结构简单直观，运算速度快；系数就是 h(n) 的序列值。','直接型不能直接控制零点。'])
    cascade_diagram(doc)
    draw_formula_block(doc,r'H(z)=(0.6+0.5z^{-1})(1.6+2z^{-1}+3z^{-2})','cascade_example',fontsize=15,max_h=42)
    fir_direct_example(doc)
    fir_cascade_example(doc)
    draw_note(doc,'级联型特点',['级联型便于按零点成对控制系统零点，但需要较多乘法器；当 H(z) 阶次较高时也不易分解。'])

    doc.h2('6.2 FIR 频率采样结构')
    doc.p('频率采样结构用 H(k) 表示 H(z)，等价于在单位圆上取 N 点频域采样，再通过离散傅里叶反变换得到长度 N 的冲激响应。')
    draw_formula_block(doc,r'H(z)=(1-z^{-N})\frac{1}{N}\sum_{k=0}^{N-1}\frac{H(k)}{1-W_N^kz^{-1}}','freq_sampling_main',fontsize=14,max_h=50)
    freq_sampling_flow(doc)
    comb_and_resonator(doc)
    comb_response_figure(doc)
    frequency_sampling_network(doc)
    doc.h3('例：频率采样结构实现')
    doc.p('已知 FIR 滤波器单位脉冲响应为 h(n)=δ(n)-δ(n-1)+δ(n-4)，取 N=5，要求画出频率采样结构并给出计算公式。')
    draw_formula_block(doc,r'H(k)=\sum_{n=0}^{N-1}h(n)W_N^{kn}=1-e^{-j\frac{2\pi k}{5}}+e^{-j\frac{8\pi k}{5}},\quad k=0,1,2,3,4','freq_sampling_ex',fontsize=13,max_h=45)

    doc.h2('6.3 FIR 线性相位结构')
    doc.p('线性相位系统的频率响应可以写成幅度项乘以线性相位项。幅度为实偶函数或实奇函数，相位是 ω 的线性函数。线性相位和广义线性相位系统也称为常数群延迟系统。')
    draw_formula_block(doc,r'H(e^{j\omega})=A(e^{j\omega})e^{-j\omega\alpha},\qquad \tau=-\frac{d\theta(\omega)}{d\omega}','linear_phase_def',fontsize=15,max_h=42)
    doc.p('线性相位 FIR 的单位脉冲响应具有对称或反对称关系。无论一类还是二类，对称中心都是 (N-1)/2。')
    draw_formula_block(doc,r'h(n)=h(N-1-n),\qquad h(n)=-h(N-1-n)','symmetry',fontsize=15,max_h=42)
    linear_phase_network(doc,'odd')
    linear_phase_network(doc,'even')
    linear_phase_reduction_example(doc)
    draw_linear_phase_critical_page(doc, antisymmetric=False)
    draw_linear_phase_critical_page(doc, antisymmetric=True)
    doc.h3('线性相位 FIR 的四类情况')
    linear_phase_table(doc)
    draw_note(doc,'814 重点提示',['线性相位 FIR 的四类表是设计题高频考点：要同时记住 N 奇偶、h(n) 对称性、H(ω) 对称性以及可实现的滤波器类型。','一类线性相位适用范围最广；二类在 ω=π 处受限；三类在 ω=0 和 π 处受限；四类在 ω=0 处受限。'])

    doc.h2('6.4 线性相位 FIR 滤波器')
    doc.p('FIR 与 IIR 相比，可做到严格线性相位，并且可以具有任意幅度特性。幅频响应决定频率成分通过比例，相频响应决定时延或频率偏移。')
    draw_formula_block(doc,r'H(e^{j\omega})=\pm |H(e^{j\omega})|e^{j\theta(\omega)}=H(\omega)e^{j\theta(\omega)}','fir_phase',fontsize=15,max_h=42)
    draw_formula_block(doc,r'\theta(\omega)=-\tau\omega,\qquad \theta(\omega)=\beta_0-\tau\omega,\ \beta_0=\pm\frac{\pi}{2}','phase_two',fontsize=14,max_h=44)
    doc.p('对称和反对称 h(n) 的振幅响应可用余弦或正弦展开。后续 FIR 设计通常直接套用四类表选择合适结构。')
    amplitude_phase_explainer(doc)
    linear_phase_four_cases(doc)
    draw_note(doc,'四类 FIR 选型与零点约束',[
        '一类：N 为奇数、h(n) 偶对称，ω=0 与 ω=π 均不被强制为零，可实现 LP、HP、BP、BS。',
        '二类：N 为偶数、h(n) 偶对称，ω=π 必为零，可实现 LP、BP，不适合 HP、BS。',
        '三类：N 为奇数、h(n) 奇对称，ω=0 与 ω=π 必为零，只能实现 BP。',
        '四类：N 为偶数、h(n) 奇对称，ω=0 必为零，可实现 HP、BP。'
    ])

    doc.save()
    NOTE_PATH.write_text('# 第十一批校对记录\n\n- 范围：原 PPT 333-366 页。\n- 已覆盖 FIR 特点、系统函数和差分方程、直接型/级联型结构、频率采样结构、修正方法、线性相位定义、对称条件和四类表。\n- 图形均为讲义内手绘复刻，不使用整页源图裁切。\n- 原 PPT 365-366 两张核心设计总表已分别保留为完整 A4 页面，包含勾选表、冲激响应、振幅响应、相位图、系数公式与红色结论。\n- 第三类线性相位 FIR 按原课件更正为只能实现 BP。\n',encoding='utf-8')
    print(PDF_PATH)

if __name__=='__main__':
    build()


