from pathlib import Path
import sys
import os
import math

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work'
sys.path.insert(0, str(WORK))

MPL_DIR = WORK / 'mplcache'
MPL_DIR.mkdir(parents=True, exist_ok=True)
os.environ['MPLCONFIGDIR'] = str(MPL_DIR)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics

from make_dsp_sample_handout_v2 import (
    BLUE, BLUE_DARK, CONTENT_W, MARGIN_X, MUTED, TEXT, PAGE_H, PAGE_W,
    Doc, register_fonts, wrap, centered_text_baselines, draw_centered_multiline_text,
)

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

OUT_DIR = ROOT / 'outputs'
FORMULA_DIR = WORK / 'formula_cache'
OUT_DIR.mkdir(exist_ok=True)
FORMULA_DIR.mkdir(parents=True, exist_ok=True)
PDF_PATH = OUT_DIR / 'DSP讲义重制_第九批_原PPT266-300页_IIR滤波器设计_手绘复刻版.pdf'
NOTE_PATH = OUT_DIR / 'DSP讲义重制_第九批_原PPT266-300页_IIR滤波器设计_手绘复刻版_校对记录.md'


def direct_structure_source_topology():
    """Source-locked topology for PPT pages 275 and 279.

    Keeping this data separate from drawing coordinates prevents a later visual
    adjustment from silently changing the original direct-form signal paths.
    """
    return {
        'direct_i': {
            'feedforward_delay_side': 'left',
            'feedback_delay_side': 'right',
            'feedforward_coefficients': ('b_0', 'b_1', 'b_2', 'b_M'),
            'feedback_coefficients': ('a_1', 'a_2', 'a_{N-1}', 'a_N'),
            'feedforward_direction': 'right',
            'feedback_direction': 'left',
            'feedback_delay_direction': 'down',
        },
        'direct_ii': {
            'shared_delay_chain': 'center',
            'feedforward_direction': 'right',
            'feedback_direction': 'left',
            'coefficient_pairs': (('-4', '5/4'), ('11', '-3/4'), ('-2', '1/8')),
        },
        'direct_ii_general': {
            'upper_layout': ('direct_i_left', 'merged_direct_ii_right'),
            'lower_layout': 'compact_merged_delay_chain',
            'coefficients': ('a_1', 'a_2', 'b_0', 'b_1', 'b_2'),
        },
    }


def cascade_parallel_source_topology():
    """Non-negotiable network topology taken from PPT pages 284 and 286."""
    return {
        'cascade': {
            'sections': ('first_order', 'second_order'),
            'main_path': 'horizontal',
            'first_order_feedback': ('0.25', '-0.379'),
            'second_order_feedback': ('-0.5', '5.264'),
            'delay_count': (1, 2),
        },
        'parallel': {
            'direct_path_coefficients': ('G_0', 'G_1', 'G_{M-N}'),
            'second_order_sections': ('beta_01', 'beta_11', 'alpha_11', 'alpha_21'),
            'branches': 'vertical_input_output_buses',
            'delay_count': (1, 2),
        },
        'example': {
            'cascade_sections': (('1/4', '1/3'), ('1/2',)),
            'parallel_branches': (('10/3', '1/2'), ('-7/3', '1/4')),
            'layouts': ('cascade_left', 'parallel_right'),
        },
    }


def parallel_iir_layout_geometry():
    return {
        'network_bottom_offset': -261,
        'annotation_offset': -284,
        'annotation_gap_below_network': 23,
    }

RED = colors.HexColor('#E00000')
PURPLE = colors.HexColor('#E000E8')
GRID = colors.HexColor('#B7B7B7')
BLACK = colors.HexColor('#111111')
PALE_BLUE = colors.HexColor('#F4FAFF')
YELLOW = colors.HexColor('#FFF6A6')
CYAN = colors.HexColor('#CFFBFF')


def ratio_tex(value):
    if '/' not in value:
        return value
    sign = '-' if value.startswith('-') else ''
    numerator, denominator = value.removeprefix('-').split('/')
    return rf'{sign}\frac{{{numerator}}}{{{denominator}}}'


def formula_png(name, expr, fontsize=14, color='#111111'):
    safe = ''.join(ch if ch.isalnum() else '_' for ch in name)[:80]
    path = FORMULA_DIR / f'b266_redraw_{safe}.png'
    fig = plt.figure(figsize=(0.01, 0.01), dpi=300)
    fig.patch.set_alpha(0)
    fig.text(0, 0, f'${expr}$', fontsize=fontsize, color=color)
    fig.savefig(path, dpi=300, transparent=True, bbox_inches='tight', pad_inches=0.04)
    plt.close(fig)
    return path


def image_size(path):
    from PIL import Image
    return Image.open(path).size


def draw_math_at(c, expr, x, y, max_w=180, max_h=30, fontsize=14, color='#111111', name='math'):
    path = formula_png(name, expr, fontsize, color)
    iw, ih = image_size(path)
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(path)), x, y - dh / 2, dw, dh, mask='auto')
    return dw, dh


def draw_formula_block(doc, expr, name, max_w=None, max_h=44, fontsize=16, gap=12):
    path = formula_png(name, expr, fontsize)
    iw, ih = image_size(path)
    max_w = max_w or CONTENT_W * 0.92
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    doc.ensure(dh + gap)
    x = MARGIN_X + (CONTENT_W - dw) / 2
    doc.c.drawImage(ImageReader(str(path)), x, doc.y - dh, dw, dh, mask='auto')
    doc.y -= dh + gap


def draw_note(doc, title, lines):
    wrapped = []
    total = 0
    for line in lines:
        ls = wrap(line, CONTENT_W - 24, 'CN', 9.2)
        wrapped.append(ls)
        total += len(ls)
    h = 28 + total * 14 + 10
    doc.ensure(h + 12)
    c = doc.c
    y = doc.y - h
    c.setStrokeColor(colors.HexColor('#A7D5FF'))
    c.setFillColor(PALE_BLUE)
    c.roundRect(MARGIN_X, y, CONTENT_W, h, 4, stroke=1, fill=1)
    c.setFillColor(BLUE_DARK)
    c.setFont('CNB', 10)
    c.drawString(MARGIN_X + 12, y + h - 19, title)
    c.setFillColor(TEXT)
    c.setFont('CN', 9.2)
    yy = y + h - 37
    for ls in wrapped:
        for line in ls:
            c.drawString(MARGIN_X + 12, yy, line)
            yy -= 14
    doc.y = y - 12


def arrow(c, x1, y1, x2, y2, color=BLACK, width=1.2, head=6):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)
    ang = math.atan2(y2 - y1, x2 - x1)
    a1 = ang + math.pi * 0.82
    a2 = ang - math.pi * 0.82
    c.setFillColor(color)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 + head * math.cos(a1), y2 + head * math.sin(a1))
    p.lineTo(x2 + head * math.cos(a2), y2 + head * math.sin(a2))
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def dot(c, x, y, r=3.2, color=RED):
    c.setFillColor(color)
    c.circle(x, y, r, stroke=0, fill=1)


def sum_node(c, x, y, r=13, color=RED):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(1.5)
    c.circle(x, y, r, stroke=1, fill=0)
    c.line(x - r * 0.62, y, x + r * 0.62, y)
    c.line(x, y - r * 0.62, x, y + r * 0.62)
    c.restoreState()


def gain_triangle(c, x, y, w=26, h=22, label='a'):
    c.saveState()
    c.setStrokeColor(RED)
    c.setLineWidth(1.5)
    c.setFillColor(YELLOW)
    p = c.beginPath()
    p.moveTo(x, y - h / 2)
    p.lineTo(x, y + h / 2)
    p.lineTo(x + w, y)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    draw_math_at(c, label, x + w * 0.33, y, max_w=w * 0.45, max_h=h * 0.6, fontsize=14, color='#0052B8', name=f'gain_{label}')
    c.restoreState()


def directional_gain_triangle(c, x, y, direction, w=26, h=22, label='a'):
    """Draw a gain block with the source diagram's signal-flow direction."""
    c.saveState()
    c.setStrokeColor(RED)
    c.setLineWidth(1.5)
    c.setFillColor(YELLOW)
    p = c.beginPath()
    if direction == 'left':
        p.moveTo(x + w, y - h / 2)
        p.lineTo(x + w, y + h / 2)
        p.lineTo(x, y)
    elif direction == 'up':
        p.moveTo(x - w / 2, y - h)
        p.lineTo(x + w / 2, y - h)
        p.lineTo(x, y)
    else:
        p.moveTo(x, y - h / 2)
        p.lineTo(x, y + h / 2)
        p.lineTo(x + w, y)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    if direction == 'left':
        tx, ty = x + w * 0.34, y
    elif direction == 'up':
        tx, ty = x - w * 0.22, y - h * 0.58
    else:
        tx, ty = x + w * 0.33, y
    draw_math_at(c, label, tx, ty, max_w=w * 0.5, max_h=h * 0.58, fontsize=13, color='#0052B8', name=f'gain_{direction}_{label}')
    c.restoreState()


def second_order_source_geometry():
    return {
        'main_sum': (150, 0),
        'feedback_sum': (150, -60),
        'delay_centers': ((220, -48), (220, -102)),
        'a1_direction': 'left',
        'a2_direction': 'up',
        'a1_path': ((220, -60), (198, -60), (172, -60)),
        'a1_triangle_tip_x': 172,
        'feedback_sum_right_x': 159,
        'a2_path': ((220, -112), (150, -112), (150, -70)),
        'flow_feedback_rows': (-40, -82),
        'flow_branch_direction': 'right-to-left',
    }


def delay_box(c, x, y, w=34, h=22, label=r'z^{-1}', stroke=RED):
    c.saveState()
    c.setStrokeColor(stroke)
    c.setFillColor(YELLOW)
    c.setLineWidth(1.4)
    c.rect(x, y - h / 2, w, h, stroke=1, fill=1)
    draw_math_at(c, label, x + 7, y, max_w=w - 10, max_h=h * 0.7, fontsize=13, color='#003C9B', name=f'delay_{x}_{y}')
    c.restoreState()


def dashed_rect(c, x, y, w, h, color=colors.blue):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(1.3)
    c.setDash(4, 3)
    c.rect(x, y, w, h, stroke=1, fill=0)
    c.setDash()
    c.restoreState()


def draw_basic_ops_table(doc):
    h = 168
    doc.ensure(h + 12)
    c = doc.c
    x = MARGIN_X
    y_top = doc.y
    col = [110, 185, 205]
    row_h = 38
    headers = ['', '方框图表示法', '信号流图表示法']
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    # grid
    xx = x
    for w in col:
        c.rect(xx, y_top - row_h * 4, w, row_h * 4, stroke=1, fill=0)
        xx += w
    for i in range(1, 4):
        c.line(x, y_top - row_h * i, x + sum(col), y_top - row_h * i)
    c.line(x + col[0], y_top, x + col[0], y_top - row_h * 4)
    c.line(x + col[0] + col[1], y_top, x + col[0] + col[1], y_top - row_h * 4)
    c.setFont('CNB', 10.5)
    for i, head in enumerate(headers):
        c.drawCentredString(x + sum(col[:i]) + col[i] / 2, y_top - 24, head)
    labels = ['相加', '乘常数', '延时']
    c.setFont('CN', 10.5)
    for r, lab in enumerate(labels):
        cy = y_top - row_h * (r + 1.5)
        c.drawCentredString(x + col[0] / 2, cy - 4, lab)
    # addition row
    cy = y_top - row_h * 1.5
    cx = x + col[0] + col[1] / 2
    arrow(c, cx - 45, cy, cx - 9, cy, RED, 1.5)
    sum_node(c, cx, cy, 12, RED)
    arrow(c, cx + 12, cy, cx + 50, cy, RED, 1.5)
    arrow(c, cx, cy - 30, cx, cy - 13, RED, 1.5)
    cx2 = x + col[0] + col[1] + col[2] / 2
    arrow(c, cx2 - 55, cy, cx2 + 55, cy, RED, 1.5)
    dot(c, cx2, cy, 3.2, RED)
    arrow(c, cx2, cy - 30, cx2, cy - 2, RED, 1.5)
    # gain row
    cy = y_top - row_h * 2.5
    cx = x + col[0] + col[1] / 2
    arrow(c, cx - 50, cy, cx - 16, cy, RED, 1.5)
    gain_triangle(c, cx - 16, cy, 32, 24, 'a')
    arrow(c, cx + 17, cy, cx + 55, cy, RED, 1.5)
    cx2 = x + col[0] + col[1] + col[2] / 2
    arrow(c, cx2 - 55, cy, cx2 + 55, cy, RED, 1.5)
    draw_math_at(c, 'a', cx2 - 5, cy + 12, max_w=18, max_h=14, fontsize=12, color='#0052B8', name='flow_gain_a')
    # delay row
    cy = y_top - row_h * 3.5
    cx = x + col[0] + col[1] / 2
    arrow(c, cx - 50, cy, cx - 20, cy, RED, 1.5)
    delay_box(c, cx - 20, cy, 42, 24)
    arrow(c, cx + 23, cy, cx + 60, cy, RED, 1.5)
    cx2 = x + col[0] + col[1] + col[2] / 2
    arrow(c, cx2 - 55, cy, cx2 + 55, cy, RED, 1.5)
    draw_math_at(c, r'z^{-1}', cx2 - 12, cy + 12, max_w=35, max_h=15, fontsize=12, color='#0052B8', name='flow_delay_z')
    doc.y = y_top - h - 10


def draw_second_order_diagrams(doc):
    geometry = second_order_source_geometry()
    h = 248
    doc.ensure(h + 10)
    c=doc.c; top=doc.y; y=top-72
    c.setFillColor(MUTED); c.setFont('CNB',9.5)
    c.drawCentredString(MARGIN_X+155,y+62,'方框图')
    c.drawCentredString(MARGIN_X+395,y+62,'信号流图')

    # Left: source page 272, including the leftward a1 branch and upward a2 branch.
    x=MARGIN_X+18
    draw_math_at(c,r'x(n)',x,y+12,42,18,13,name='so_x')
    arrow(c,x+42,y,x+82,y,RED,1.3); gain_triangle(c,x+82,y,26,20,r'b_0')
    main_x = x + geometry['main_sum'][0]
    feedback_x = x + geometry['feedback_sum'][0]
    sum_node(c, main_x, y, 10, RED)
    arrow(c,x+108,y,main_x-10,y,RED,1.3)
    arrow(c,main_x+10,y,x+250,y,RED,1.3)
    draw_math_at(c,r'y(n)',x+255,y+12,42,18,13,name='so_y')

    delay_x = x + geometry['delay_centers'][0][0]
    c.setStrokeColor(RED); c.setLineWidth(1.2)
    c.line(delay_x, y, delay_x, y-38)
    c.line(delay_x, y-58, delay_x, y-92)
    delay_box(c, delay_x-17, y-48, 34, 20, r'z^{-1}')
    delay_box(c, delay_x-17, y-102, 34, 20, r'z^{-1}')
    arrow(c, delay_x, y-38, delay_x, y-39, RED, 1.1)
    arrow(c, delay_x, y-92, delay_x, y-93, RED, 1.1)

    feedback_y = y + geometry['feedback_sum'][1]
    sum_node(c, feedback_x, feedback_y, 9, RED)
    # a1: delay output travels right-to-left into the feedback sum.
    c.line(delay_x, feedback_y, x+198, feedback_y)
    directional_gain_triangle(c, x+172, feedback_y, 'left', 26, 20, r'a_1')
    arrow(c, x+172, feedback_y, feedback_x+9, feedback_y, RED, 1.1)
    # a2: bottom delay output turns left, then rises through an upward gain block.
    bottom_y = y-112
    c.line(delay_x, bottom_y, feedback_x, bottom_y)
    directional_gain_triangle(c, feedback_x, y-78, 'up', 24, 20, r'a_2')
    arrow(c, feedback_x, bottom_y, feedback_x, y-98, RED, 1.1)
    arrow(c, feedback_x, y-78, feedback_x, feedback_y-9, RED, 1.1)
    arrow(c, feedback_x, feedback_y+9, main_x, y-10, RED, 1.1)

    # Right: source signal-flow graph, with two right-to-left feedback rows.
    x=MARGIN_X+303
    draw_math_at(c,r'x(n)',x,y+12,42,18,13,name='sf_x')
    arrow(c,x+40,y,x+206,y,RED,1.25)
    for px in [x+56,x+112,x+178,x+206]: dot(c,px,y,2.8,RED)
    draw_math_at(c,r'b_0',x+68,y+15,28,14,11,name='sf_b0')
    draw_math_at(c,r'y(n)',x+210,y+12,42,18,13,name='sf_y')
    arrow(c,x+178,y,x+178,y-40,RED,1.1); draw_math_at(c,r'z^{-1}',x+185,y-20,30,14,10,name='sf_z1')
    dot(c,x+178,y-40,2.7,RED); arrow(c,x+178,y-40,x+112,y-40,RED,1.1); arrow(c,x+112,y-40,x+112,y,RED,1.1)
    draw_math_at(c,r'a_1',x+130,y-27,28,14,11,name='sf_a1')
    arrow(c,x+178,y-40,x+178,y-82,RED,1.1); draw_math_at(c,r'z^{-1}',x+185,y-62,30,14,10,name='sf_z2')
    dot(c,x+178,y-82,2.7,RED); arrow(c,x+178,y-82,x+112,y-82,RED,1.1); arrow(c,x+112,y-82,x+112,y-40,RED,1.1)
    draw_math_at(c,r'a_2',x+130,y-69,28,14,11,name='sf_a2')
    doc.y = top - h


def draw_direct_i_general(doc):
    topology = direct_structure_source_topology()['direct_i']
    h = 210
    doc.ensure(h + 12)
    c = doc.c
    y = doc.y - 55
    x = MARGIN_X + 150
    # equation on right/top
    # explanatory side labels
    c.setFont('CN', 9.2)
    left_lines = ['第一部分是对输入 x(n)', '的 M 节延时链结构，', '抽头加权相加，', '即横向网络。']
    yy = y + 35
    for i, line in enumerate(left_lines):
        c.setFillColor(RED if '横向' in line else TEXT)
        c.drawString(MARGIN_X, yy - i * 14, line)
    right_x = MARGIN_X + 405
    right_lines = ['第二部分是对 y(n)', '的 N 节延时链结构，', '因此是反馈网络。']
    for i, line in enumerate(right_lines):
        c.setFillColor(RED if '反馈' in line else TEXT)
        c.drawString(right_x, yy - i * 14, line)
    c.setFillColor(TEXT)
    # signal-flow center
    arrow(c, x, y + 45, x + 280, y + 45, RED, 1.5)
    draw_math_at(c, r'x(n)', x - 45, y + 57, 45, 22, 13, name='di_x')
    draw_math_at(c, r'y(n)', x + 285, y + 57, 45, 22, 13, name='di_y')
    # two dashed regions
    dashed_rect(c, x + 65, y - 110, 95, 170, colors.blue)
    dashed_rect(c, x + 175, y - 125, 95, 185, colors.blue)
    # left transversal branch
    for k, lab in enumerate(topology['feedforward_coefficients']):
        yy2 = y + 45 - k * 38
        if k == 0:
            dot(c, x + 82, yy2, 3, RED)
            arrow(c, x + 82, yy2, x + 145, yy2, RED, 1.3)
        else:
            dot(c, x + 82, yy2, 3, RED)
            arrow(c, x + 82, yy2, x + 145, yy2, RED, 1.3)
        draw_math_at(c, lab, x + 105, yy2 + 14, 35, 18, 12, name=f'di_{lab}')
        if k < 3:
            arrow(c, x + 82, yy2, x + 82, yy2 - 30, RED, 1.2)
            draw_math_at(c, r'z^{-1}', x + 38, yy2 - 18, 32, 16, 11, name=f'di_zl{k}')
    c.setFont('CNB', 10); c.setFillColor(RED); c.drawString(x + 45, y - 128, '横向网络')
    # center summing vertical
    arrow(c, x + 155, y - 100, x + 155, y + 44, RED, 1.4)
    # right feedback branch
    for k, lab in enumerate(topology['feedback_coefficients']):
        yy2 = y + 10 - k * 38
        dot(c, x + 220, yy2, 3, RED)
        arrow(c, x + 220, yy2, x + 175, yy2, RED, 1.3)
        draw_math_at(c, lab, x + 185, yy2 + 14, 40, 18, 12, name=f'di_{lab}')
        if k < 3:
            arrow(c, x + 220, yy2 + 28, x + 220, yy2 + 2, RED, 1.2)
            draw_math_at(c, r'z^{-1}', x + 232, yy2 + 14, 32, 16, 11, name=f'di_zr{k}')
    c.setFont('CNB', 10); c.setFillColor(RED); c.drawString(x + 178, y - 145, '反馈网络')
    c.setFillColor(TEXT)
    doc.y -= h


def draw_parallel_iir(doc):
    topology = cascade_parallel_source_topology()['parallel']
    h = 338
    doc.ensure(h + 12)
    c = doc.c
    top=doc.y; y=top-38; left=MARGIN_X+82; right=MARGIN_X+430
    c.setStrokeColor(RED); c.setFillColor(RED); c.setLineWidth(1.15)
    arrow(c,MARGIN_X+28,y,left,y,RED,1.15); arrow(c,left,y,right,y,RED,1.15); arrow(c,right,y,right+24,y,RED,1.15)
    draw_math_at(c,r'x(n)',MARGIN_X,y+13,40,16,11,name='parallel_x')
    draw_math_at(c,r'y(n)',right+28,y+13,40,16,11,name='parallel_y')
    dot(c,left,y,2.6,RED); dot(c,right,y,2.6,RED)

    # Upper direct-polynomial branch G0, G1, ..., G_{M-N}.
    direct_left=left+42; direct_right=left+142
    c.line(left,y,left,y-68); c.line(right,y,right,y-68)
    for i,(yy,lab) in enumerate([(y-22,r'G_0'),(y-43,r'G_1'),(y-66,r'G_{M-N}')]):
        c.line(direct_left,yy,direct_right,yy)
        dot(c,direct_left,yy,2.1,RED); dot(c,direct_right,yy,2.1,RED)
        draw_math_at(c,lab,direct_left+36,yy+10,38,14,9.5,name=f'parallel_direct_{i}')
    c.line(direct_left,y,direct_left,y-66); c.line(direct_right,y,direct_right,y-66)
    c.setFont('CNB',9); c.setFillColor(TEXT); c.drawCentredString((direct_left+direct_right)/2,y-56,'...')

    def second_order_branch(base_y, suffix):
        branch_left=left+36; delay_x=left+104; branch_right=right-36
        c.line(left,base_y,branch_left,base_y); c.line(branch_right,base_y,right,base_y)
        c.line(branch_left,base_y,branch_right,base_y)
        dot(c,branch_left,base_y,2.2,RED); dot(c,branch_right,base_y,2.2,RED)
        draw_math_at(c,rf'\beta_{{01{suffix}}}',branch_right-54,base_y+12,48,14,9,name=f'parallel_beta0_{suffix}')
        for j,(alpha,beta) in enumerate([(rf'\alpha_{{11{suffix}}}',rf'\beta_{{11{suffix}}}'),(rf'\alpha_{{21{suffix}}}',r'')]):
            yy=base_y-28*(j+1)
            c.line(branch_left,yy,delay_x,yy); c.line(delay_x,yy,branch_right,yy)
            c.line(branch_left,base_y if j==0 else yy+28,branch_left,yy)
            c.line(delay_x,base_y if j==0 else yy+28,delay_x,yy)
            c.line(branch_right,base_y if j==0 else yy+28,branch_right,yy)
            draw_math_at(c,alpha,branch_left+10,yy+10,42,13,8.5,name=f'parallel_alpha_{suffix}_{j}')
            if beta:
                draw_math_at(c,beta,branch_right-48,yy+10,42,13,8.5,name=f'parallel_beta_{suffix}_{j}')
            draw_math_at(c,r'z^{-1}',delay_x+5,yy+10,30,13,8.5,name=f'parallel_z_{suffix}_{j}')
    c.line(left,y-68,left,y-222); c.line(right,y-68,right,y-222)
    second_order_branch(y-105,'')
    c.setFont('CNB',12); c.setFillColor(TEXT); c.drawCentredString((left+right)/2,y-178,'...')
    second_order_branch(y-205,'L')
    layout = parallel_iir_layout_geometry()
    c.setFillColor(RED); c.setFont('CNB',8.8)
    c.drawCentredString((left+right)/2,y+layout['annotation_offset'],'各支路分别实现，再在输出端相加')
    doc.y -= h


def direct_ii_general_geometry():
    return {
        'canvas_height': 472,
        'panel_width': 176,
        'row_gap': 50,
        'right_panel_offset': 255,
        'arrow_overhang': 26,
        'output_label_width': 42,
        'source_side_labels': ('x(n-1)', 'x(n-2)', 'y(n-1)', 'y(n-2)', 'w_1', 'w_2'),
    }


def draw_direct_ii_general(doc):
    """Recreate the three source networks on PPT 276 at readable A4 scale."""
    geometry = direct_ii_general_geometry()
    h = geometry['canvas_height']
    panel_w = geometry['panel_width']
    row_gap = geometry['row_gap']
    doc.ensure(h + 12)
    c = doc.c
    top = doc.y
    c.setStrokeColor(TEXT)
    c.setFillColor(TEXT)
    c.setFont('CN', 10.5)
    c.drawString(MARGIN_X, top - 16, '设 M=N=2，先交换直接 I 型前向、反馈两部分，再合并公共延时链得到直接 II 型。')

    def dashed_rect(x, y, w, hh):
        c.setDash(4, 3)
        c.rect(x, y - hh, w, hh, stroke=1, fill=0)
        c.setDash()

    def draw_panel(x, y, merged, tag, side_labels=False):
        left_rail = x + 34
        middle = x + panel_w / 2
        right_rail = x + panel_w - 34
        bottom = y - 2 * row_gap
        arrow(c, x - 26, y, x + panel_w + 26, y, TEXT, 1.0)
        dot(c, left_rail, y, 2.4, TEXT)
        dot(c, right_rail, y, 2.4, TEXT)

        if merged:
            dashed_rect(x + 14, y + 17, panel_w / 2 - 14, 2 * row_gap + 34)
            dashed_rect(middle, y + 17, panel_w / 2 - 14, 2 * row_gap + 34)
            c.line(middle, y, middle, bottom)
            draw_math_at(c, r'w_1', middle - 39, y + 13, 34, 15, 10.5, name=f'{tag}_w1')
            draw_math_at(c, r'w_2', middle + 5, y + 13, 34, 15, 10.5, name=f'{tag}_w2')
            draw_math_at(c, r'b_0', right_rail - 15, y + 13, 32, 15, 10.5, name=f'{tag}_b0')
            for index, (a, b) in enumerate(((r'a_1', r'b_1'), (r'a_2', r'b_2')), 1):
                yy = y - index * row_gap
                arrow(c, middle, yy + row_gap - 8, middle, yy + 5, TEXT, 0.9)
                draw_math_at(c, r'z^{-1}', middle + 5, yy + row_gap / 2 - 2, 35, 15, 10, name=f'{tag}_z{index}')
                arrow(c, middle, yy, left_rail, yy, TEXT, 0.9)
                arrow(c, middle, yy, right_rail, yy, TEXT, 0.9)
                dot(c, left_rail, yy, 2.2, TEXT); dot(c, right_rail, yy, 2.2, TEXT)
                draw_math_at(c, a, left_rail + 10, yy + 12, 32, 15, 10.5, name=f'{tag}_a{index}')
                draw_math_at(c, b, right_rail - 43, yy + 12, 32, 15, 10.5, name=f'{tag}_b{index}')
        else:
            dashed_rect(x + 8, y + 17, 66, 2 * row_gap + 34)
            dashed_rect(x + panel_w - 74, y + 17, 66, 2 * row_gap + 34)
            c.line(left_rail, y, left_rail, bottom)
            c.line(right_rail, y, right_rail, bottom)
            draw_math_at(c, r'b_0', middle - 16, y + 13, 32, 15, 10.5, name=f'{tag}_b0')
            for index, (b, a) in enumerate(((r'b_1', r'a_1'), (r'b_2', r'a_2')), 1):
                yy = y - index * row_gap
                arrow(c, left_rail, yy + row_gap - 8, left_rail, yy + 5, TEXT, 0.9)
                arrow(c, right_rail, yy + row_gap - 8, right_rail, yy + 5, TEXT, 0.9)
                draw_math_at(c, r'z^{-1}', left_rail + 5, yy + row_gap / 2 - 2, 35, 15, 10, name=f'{tag}_zl{index}')
                draw_math_at(c, r'z^{-1}', right_rail - 40, yy + row_gap / 2 - 2, 35, 15, 10, name=f'{tag}_zr{index}')
                arrow(c, left_rail, yy, middle, yy, TEXT, 0.9)
                arrow(c, right_rail, yy, middle, yy, TEXT, 0.9)
                dot(c, left_rail, yy, 2.2, TEXT); dot(c, right_rail, yy, 2.2, TEXT)
                draw_math_at(c, b, left_rail + 17, yy + 12, 32, 15, 10.5, name=f'{tag}_b{index}')
                draw_math_at(c, a, middle + 16, yy + 12, 32, 15, 10.5, name=f'{tag}_a{index}')
                if side_labels:
                    draw_math_at(c, rf'x(n-{index})', x - 56, yy + 8, 54, 15, 9.8, name=f'{tag}_xside{index}')
                    draw_math_at(c, rf'y(n-{index})', x + panel_w + 2, yy + 8, 54, 15, 9.8, name=f'{tag}_yside{index}')

        return x - 26, x + panel_w + 26

    upper_y = top - 78
    left_x = MARGIN_X + 58
    right_x = MARGIN_X + geometry['right_panel_offset']
    c.setFillColor(BLUE_DARK); c.setFont('CNB', 10.5)
    c.drawCentredString(left_x + panel_w / 2, top - 42, '直接 I 型')
    c.drawCentredString(right_x + panel_w / 2, top - 42, '交换后的两部分网络')
    c.setFillColor(TEXT)
    left_start, left_end = draw_panel(left_x, upper_y, False, 'd2g_left', side_labels=True)
    right_start, right_end = draw_panel(right_x, upper_y, True, 'd2g_right')
    draw_math_at(c, r'x(n)', left_start - 38, upper_y + 11, 38, 16, 10.5, name='d2g_x_left')
    draw_math_at(c, r'y(n)', left_end + 2, upper_y + 11, 38, 16, 10.5, name='d2g_y_left')
    draw_math_at(c, r'x(n)', right_start - 38, upper_y + 11, 38, 16, 10.5, name='d2g_x_right')
    draw_math_at(c, r'y(n)', right_end + 2, upper_y + 11, 38, 16, 10.5, name='d2g_y_right')

    lower_y = top - 320
    lower_x = MARGIN_X + (CONTENT_W - panel_w) / 2
    c.setFont('CNB', 10.5); c.setFillColor(BLUE_DARK)
    c.drawCentredString(MARGIN_X + CONTENT_W / 2, top - 274, '合并后的直接 II 型网络')
    c.setFillColor(TEXT)
    lower_start, lower_end = draw_panel(lower_x, lower_y, True, 'd2g_lower')
    draw_math_at(c, r'x(n)', lower_start - 38, lower_y + 11, 38, 16, 10.5, name='d2g_x_lower')
    draw_math_at(c, r'y(n)', lower_end + 2, lower_y + 11, 38, 16, 10.5, name='d2g_y_lower')
    doc.y = top - h


def draw_filter_type_plots(doc):
    h = 336
    doc.ensure(h + 10)
    c=doc.c; top=doc.y; x=MARGIN_X+105; w=365; center=x+w/2
    specs=[('模拟低通滤波器','低通'),('模拟高通滤波器','高通'),('模拟带通滤波器','带通'),('模拟带阻滤波器','带阻')]
    for i,(label,kind) in enumerate(specs):
        y=top-44-i*72
        c.setFont('CNB',12); c.setFillColor(TEXT); c.drawString(MARGIN_X,y+43,label[:2])
        c.setFillColor(RED); c.drawString(MARGIN_X+28,y+43,label[2:4])
        c.setFillColor(TEXT); c.drawString(MARGIN_X+56,y+43,label[4:])
        c.setStrokeColor(PURPLE); c.setLineWidth(1.0)
        if i: c.line(MARGIN_X,y+55,MARGIN_X+CONTENT_W,y+55)
        arrow(c,x,y,x+w,y,colors.HexColor('#163DFF'),1.1,5)
        arrow(c,center,y,center,y+39,colors.HexColor('#163DFF'),1.1,5)
        draw_math_at(c,r'|H(j\Omega)|',center+8,y+38,65,17,11,name=f'ideal_h_{kind}')
        draw_math_at(c,r'\Omega(\mathrm{rad/s})',x+w+2,y-1,84,15,10,name=f'ideal_o_{kind}')
        c.setStrokeColor(RED); c.setLineWidth(1.65)
        if kind=='低通':
            pts=[(x,y),(x+w*.30,y),(x+w*.30,y+28),(x+w*.70,y+28),(x+w*.70,y),(x+w,y)]
            labels=[(r'-\Omega_c',x+w*.27),(r'\Omega_c',x+w*.67)]
        elif kind=='高通':
            pts=[(x,y+28),(x+w*.30,y+28),(x+w*.30,y),(x+w*.70,y),(x+w*.70,y+28),(x+w,y+28)]
            labels=[(r'-\Omega_c',x+w*.27),(r'\Omega_c',x+w*.67)]
        elif kind=='带通':
            pts=[(x,y),(x+w*.22,y),(x+w*.22,y+28),(x+w*.36,y+28),(x+w*.36,y),(x+w*.64,y),(x+w*.64,y+28),(x+w*.78,y+28),(x+w*.78,y),(x+w,y)]
            labels=[(r'-\Omega_{c2}',x+w*.18),(r'-\Omega_{c1}',x+w*.32),(r'\Omega_{c1}',x+w*.60),(r'\Omega_{c2}',x+w*.74)]
        else:
            pts=[(x,y+28),(x+w*.22,y+28),(x+w*.22,y),(x+w*.36,y),(x+w*.36,y+28),(x+w*.64,y+28),(x+w*.64,y),(x+w*.78,y),(x+w*.78,y+28),(x+w,y+28)]
            labels=[(r'-\Omega_{c2}',x+w*.18),(r'-\Omega_{c1}',x+w*.32),(r'\Omega_{c1}',x+w*.60),(r'\Omega_{c2}',x+w*.74)]
        for a,b in zip(pts,pts[1:]): c.line(a[0],a[1],b[0],b[1])
        for li,(expr,lx) in enumerate(labels): draw_math_at(c,expr,lx-21,y-11,48,14,9,name=f'ideal_{kind}_{li}')
    doc.y -= h


def filter_design_source_topology():
    return {
        'bridge': {
            'rows': ('continuous', 'discrete'),
            'continuous_transforms': ('LT', 'LT', 'LT'),
            'discrete_transforms': ('ZT', 'ZT', 'ZT'),
            'time_operation': 'convolution',
            'frequency_operation': 'multiplication',
        },
        'digital_ideal_responses': {
            'types': ('lowpass', 'highpass', 'bandpass', 'bandstop'),
            'period': '2pi',
            'repeat_range': (-3, 3),
        },
    }


def draw_digital_filter_type_plots(doc):
    h = 340
    doc.ensure(h + 12)
    c = doc.c
    top = doc.y
    x0 = MARGIN_X + 150
    axis_w = 350
    center = x0 + axis_w / 2
    pi_step = axis_w / 6
    specs = [('数字低通滤波器', 'lowpass'), ('数字高通滤波器', 'highpass'),
             ('数字带通滤波器', 'bandpass'), ('数字带阻滤波器', 'bandstop')]
    for i, (label, kind) in enumerate(specs):
        y = top - 48 - i * 76
        c.setFont('CNB', 12)
        c.setFillColor(TEXT)
        c.drawString(MARGIN_X, y + 42, label[:2])
        c.setFillColor(RED)
        c.drawString(MARGIN_X + 28, y + 42, label[2:4])
        c.setFillColor(TEXT)
        c.drawString(MARGIN_X + 56, y + 42, label[4:])
        if i:
            c.setStrokeColor(PURPLE); c.setLineWidth(1)
            c.line(MARGIN_X, y + 55, MARGIN_X + CONTENT_W, y + 55)
        arrow(c, x0, y, x0 + axis_w, y, colors.HexColor('#163DFF'), 1.1, 5)
        arrow(c, center, y, center, y + 39, colors.HexColor('#163DFF'), 1.1, 5)
        draw_math_at(c, r'|H(e^{j\omega})|', center + 7, y + 38, 74, 17, 11,
                     name=f'digital_ideal_h_{kind}')
        draw_math_at(c, r'\omega(\mathrm{rad})', x0 + axis_w - 8, y - 2, 74, 15, 10,
                     name=f'digital_ideal_axis_{kind}')
        c.setStrokeColor(RED); c.setLineWidth(1.65)
        def response(q):
            phase = ((q + 1) % 2) - 1
            a = abs(phase)
            if kind == 'lowpass': return a <= .28
            if kind == 'highpass': return a >= .28
            if kind == 'bandpass': return .25 <= a <= .55
            return not (.25 <= a <= .55)
        samples = 360
        previous = response(-3)
        px, py = x0, y + (25 if previous else 0)
        for s in range(1, samples + 1):
            q = -3 + 6 * s / samples
            state = response(q)
            nx = x0 + s * axis_w / samples
            ny = y + (25 if state else 0)
            if state != previous:
                c.line(px, py, nx, py)
                c.line(nx, py, nx, ny)
            else:
                c.line(px, py, nx, ny)
            px, py, previous = nx, ny, state
        for k in range(-3, 4):
            tx = center + k * pi_step
            if x0 + 2 <= tx <= x0 + axis_w - 2 and k:
                c.setStrokeColor(colors.HexColor('#163DFF')); c.line(tx, y - 3, tx, y + 3)
                draw_math_at(c, rf'{k}\pi' if abs(k) != 1 else (r'-\pi' if k < 0 else r'\pi'),
                             tx - 18, y - 13, 38, 14, 9, name=f'digital_tick_{kind}_{k}')
        c.setFillColor(RED); c.setFont('CNB', 12)
        c.drawString(x0 - 25, y + 6, '······')
        c.drawString(x0 + axis_w - 5, y + 6, '······')
    doc.y = top - h


def butterworth_indicator_source_geometry():
    return {
        'x_range': (0.0, 3.0),
        'x_ticks': (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0),
        'y_ticks': (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        'cutoffs': {
            'passband': 0.8,
            'three_db': 0.95,
            'stopband': 1.5,
        },
        'levels': {
            'passband': 0.891,
            'three_db': 0.707,
            'stopband': 0.01,
        },
        'cutoff_colors': {
            'passband': '#E60012',
            'three_db': '#0000FF',
            'stopband': '#7B3F98',
        },
    }


def draw_butterworth_response(doc):
    h = 235
    doc.ensure(h + 12)
    c = doc.c
    geometry = butterworth_indicator_source_geometry()
    x_min, x_max = geometry['x_range']
    x = MARGIN_X + 70
    y = doc.y - 170
    w = 360
    hh = 155
    c.setStrokeColor(GRID); c.setLineWidth(0.6)
    for tick in geometry['x_ticks']:
        xx = x + (tick - x_min) / (x_max - x_min) * w
        c.line(xx, y, xx, y + hh)
    for tick in geometry['y_ticks']:
        yy = y + tick * hh
        c.line(x, yy, x + w, yy)
    c.setStrokeColor(BLACK); c.rect(x, y, w, hh, stroke=1, fill=0)
    c.setFillColor(BLACK); c.setFont('CN', 7.5)
    for tick in geometry['x_ticks']:
        xx = x + (tick - x_min) / (x_max - x_min) * w
        label = str(int(tick)) if tick.is_integer() else str(tick)
        c.drawCentredString(xx, y - 9, label)
    for tick in geometry['y_ticks'][1:]:
        yy = y + tick * hh
        label = str(int(tick)) if tick.is_integer() else str(tick)
        c.drawRightString(x - 5, yy - 2.5, label)

    # Sixth-order Butterworth response used by the source indicator plot.
    c.setStrokeColor(RED); c.setLineWidth(1.7)
    prev = None
    for i in range(120):
        t = x_min + i / 119 * (x_max - x_min)
        amp = 1 / math.sqrt(1 + (t / geometry['cutoffs']['three_db']) ** 12)
        px = x + (t - x_min) / (x_max - x_min) * w
        py = y + amp * hh
        if prev: c.line(prev[0], prev[1], px, py)
        prev = (px, py)

    guide_specs = (
        ('passband', '0.891'),
        ('three_db', '0.707'),
        ('stopband', '0.01'),
    )
    c.setDash(4, 3); c.setLineWidth(1.1)
    for key, lab in guide_specs:
        col = colors.HexColor(geometry['cutoff_colors'][key])
        val = geometry['levels'][key]
        cutoff = geometry['cutoffs'][key]
        yy = y + val * hh
        cutoff_x = x + (cutoff - x_min) / (x_max - x_min) * w
        c.setStrokeColor(col); c.line(x - 40, yy, cutoff_x, yy)
        c.setFillColor(colors.white); c.setStrokeColor(col); c.rect(x - 55, yy - 8, 38, 16, stroke=1, fill=1)
        c.setFillColor(BLACK); c.setFont('CN', 8); c.drawCentredString(x - 36, yy - 3, lab)
    c.setDash()

    cutoff_specs = (
        ('passband', r'\Omega_p', -28),
        ('three_db', r'\Omega_c', -18),
        ('stopband', r'\Omega_s', -18),
    )
    for key, lab, label_y_offset in cutoff_specs:
        color_hex = geometry['cutoff_colors'][key]
        col = colors.HexColor(color_hex)
        cutoff = geometry['cutoffs'][key]
        level = geometry['levels'][key]
        xx = x + (cutoff - x_min) / (x_max - x_min) * w
        c.setStrokeColor(col); c.setDash(4, 3)
        c.line(xx, y, xx, y + max(level, 0.2) * hh)
        c.setDash()
        draw_math_at(c, lab, xx - 18, y + label_y_offset, 36, 15, 10.5,
                     color=color_hex, name=f'bw_{key}')
    c.setFillColor(RED); c.setFont('CNB', 16); c.drawString(x + 155, y + 116, '衰减')
    c.setFillColor(colors.white); c.setStrokeColor(colors.HexColor('#7B3F98')); c.rect(x + 190, y + 108, 38, 20, stroke=1, fill=1)
    c.setFillColor(colors.HexColor('#7B3F98')); c.setFont('CNB', 12); c.drawCentredString(x + 209, y + 113, '1dB')
    c.setFillColor(colors.white); c.setStrokeColor(colors.blue); c.rect(x + 190, y + 78, 38, 20, stroke=1, fill=1)
    c.setFillColor(colors.blue); c.setFont('CNB', 12); c.drawCentredString(x + 209, y + 83, '3dB')
    c.setFillColor(RED); c.setFont('CNB', 16); c.drawString(x + 230, y + 25, '衰减')
    c.setFillColor(colors.white); c.setStrokeColor(colors.HexColor('#7B3F98')); c.rect(x + 275, y + 16, 44, 20, stroke=1, fill=1)
    c.setFillColor(colors.HexColor('#7B3F98')); c.setFont('CNB', 12); c.drawCentredString(x + 297, y + 21, '40dB')
    draw_math_at(c, r'|H_a(j\Omega)|', x - 50, y + hh + 8, 80, 20, 12, name='bw_y_label')
    draw_math_at(c, r'\Omega(\mathrm{rad/s})', x + w + 8, y - 3, 72, 18, 11, name='bw_x_label')
    doc.y -= h




def draw_butter_table(doc):
    rows = [
        ('1', r'p+1'),
        ('2', r'p^{2}+1.4142p+1'),
        ('3', r'(p+1)(p^{2}+p+1)'),
        ('4', r'(p^{2}+0.7654p+1)(p^{2}+1.8478p+1)'),
        ('5', r'(p+1)(p^{2}+0.6180p+1)(p^{2}+1.6180p+1)'),
        ('6', r'(p^{2}+0.5176p+1)(p^{2}+1.4142p+1)(p^{2}+1.9319p+1)'),
    ]
    row_h = 34
    h = row_h * (len(rows) + 1) + 8
    doc.ensure(h + 14)
    c = doc.c
    x = MARGIN_X
    y = doc.y
    w1 = 55
    w2 = CONTENT_W - w1
    c.setFillColor(BLUE_DARK)
    c.roundRect(x, y - row_h, CONTENT_W, row_h, 4, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont('CNB', 9)
    c.drawCentredString(x + w1 / 2, y - 21, 'N')
    c.drawCentredString(x + w1 + w2 / 2, y - 21, '归一化巴特沃斯多项式 B(p)')
    yy = y - row_h
    for idx, (n, expr) in enumerate(rows):
        fill = colors.white if idx % 2 == 0 else colors.HexColor('#F4F8FC')
        c.setFillColor(fill)
        c.rect(x, yy - row_h, CONTENT_W, row_h, stroke=0, fill=1)
        c.setStrokeColor(LINE if 'LINE' in globals() else colors.HexColor('#CADCEB'))
        c.line(x, yy - row_h, x + CONTENT_W, yy - row_h)
        c.setFillColor(TEXT)
        c.setFont('CN', 9.5)
        c.drawCentredString(x + w1 / 2, yy - 22, n)
        draw_math_at(c, expr, x + w1 + 10, yy - row_h / 2, max_w=w2 - 20, max_h=22, fontsize=12, name=f'butter_table_{n}')
        yy -= row_h
    c.setStrokeColor(colors.HexColor('#CADCEB'))
    c.rect(x, y - row_h * (len(rows) + 1), CONTENT_W, row_h * (len(rows) + 1), stroke=1, fill=0)
    c.line(x + w1, y, x + w1, y - row_h * (len(rows) + 1))
    doc.y = y - row_h * (len(rows) + 1) - 14

def draw_simple_coeff_grid(doc, title, left_title, right_title, left_vals, right_vals):
    h = 172
    doc.ensure(h + 14)
    c = doc.c
    top = doc.y
    c.setFont('CNB', 10)
    c.setFillColor(BLUE_DARK)
    c.drawString(MARGIN_X, top - 14, title)
    y0 = top - 52
    x0 = MARGIN_X + 70
    for offset, ttl, vals in [(0, left_title, left_vals), (260, right_title, right_vals)]:
        x = x0 + offset
        c.setFont('CNB', 9)
        c.setFillColor(TEXT)
        c.drawCentredString(x + 92, y0 + 48, ttl)
        draw_math_at(c, r'x(n)', x - 45, y0 + 12, 45, 18, 12, name=f'gridx_{offset}')
        draw_math_at(c, r'y(n)', x + 190, y0 + 12, 45, 18, 12, name=f'gridy_{offset}')
        arrow(c, x, y0 + 8, x + 184, y0 + 8, RED, 1.3)
        c.setStrokeColor(RED)
        c.setLineWidth(1.1)
        c.rect(x + 35, y0 - 50, 115, 110, stroke=1, fill=0)
        c.line(x + 92, y0 - 50, x + 92, y0 + 60)
        for k in range(1,4):
            yy = y0 + 60 - k * 27
            c.line(x + 35, yy, x + 150, yy)
        for i, val in enumerate(vals):
            col = 0 if i < 4 else 1
            row = i if i < 4 else i - 4
            xx = x + 48 + col * 56
            yy = y0 + 42 - row * 27
            draw_math_at(c, val, xx, yy, 46, 18, 12, name=f'grid_{offset}_{i}')
        for yy in [y0 + 35, y0 + 8, y0 - 19]:
            draw_math_at(c, r'z^{-1}', x + 8, yy, 32, 16, 10, name=f'zl_{offset}_{yy}')
            draw_math_at(c, r'z^{-1}', x + 154, yy, 32, 16, 10, name=f'zr_{offset}_{yy}')
    doc.y = top - h


def direct_iir_example_arrow_geometry():
    return {
        'direct_i': {
            'feedforward_delay_down': 3,
            'feedback_delay_down': 3,
            'accumulator_up': 3,
        },
        'direct_ii': {
            'shared_delay_down': 3,
            'feedback_return_up': 3,
            'feedforward_return_up': 3,
        },
    }


def draw_direct_ii_examples(doc):
    topology = direct_structure_source_topology()['direct_ii']
    doc.p('直接 II 型例题中，先把 H(z) 写成分母首项为 1 的负幂形式，再把直接 I 型的两条延时链合并。源图中反馈系数的符号需要特别注意。')
    draw_formula_block(doc, r'H(z)=\frac{8-4z^{-1}+11z^{-2}-2z^{-3}}{1-\frac{5}{4}z^{-1}+\frac{3}{4}z^{-2}-\frac{1}{8}z^{-3}}', 'direct2_full_hz', fontsize=16, max_h=54)
    h=230; doc.ensure(h+12); c=doc.c; top=doc.y; y=top-62
    c.setFillColor(BLUE_DARK); c.setFont('CNB',10)
    c.drawCentredString(MARGIN_X+150,top-14,'直接 I 型')
    c.drawCentredString(MARGIN_X+400,top-14,'直接 II 型')

    def as_tex(value):
        if '/' not in value:
            return value
        sign = '-' if value.startswith('-') else ''
        numerator, denominator = value.removeprefix('-').split('/')
        return rf'{sign}\frac{{{numerator}}}{{{denominator}}}'

    coefficient_pairs = tuple((as_tex(b), as_tex(a)) for b, a in topology['coefficient_pairs'])

    def network(x, direct_two=False):
        draw_math_at(c,r'x(n)',x-42,y+12,42,17,12,name=f'd2_x_{direct_two}')
        draw_math_at(c,r'y(n)',x+180,y+12,42,17,12,name=f'd2_y_{direct_two}')
        arrow(c,x,y,x+182,y,RED,1.15)
        dot(c,x+24,y,2.7,RED); dot(c,x+138,y,2.7,RED)
        draw_math_at(c,r'8',x+45,y+13,16,14,11,name=f'd2_b0_{direct_two}')
        left=x+44; right=x+130; middle=x+87

        def vertical_stage_arrows(rail_x, direction):
            levels = [y - 30 * index for index in range(4)]
            for index in range(3):
                upper, lower = levels[index], levels[index + 1]
                if direction == 'down':
                    arrow(c, rail_x, upper, rail_x, lower, RED, 1.0)
                else:
                    arrow(c, rail_x, lower, rail_x, upper, RED, 1.0)

        if direct_two:
            # Direct II shares the delay chain: forward taps to the right, feedback taps to the left.
            vertical_stage_arrows(middle, 'down')
            for i, (bl, al) in enumerate(coefficient_pairs):
                yy=y-30*(i+1); dot(c,middle,yy,2.5,RED)
                draw_math_at(c,r'z^{-1}',middle-16,yy+12,30,13,10,name=f'd2_z_{i}')
                arrow(c,middle,yy,middle+48,yy,RED,1.0); draw_math_at(c,bl,middle+22,yy+11,25,14,10,name=f'd2_b_{i}')
                arrow(c,middle,yy,middle-48,yy,RED,1.0); draw_math_at(c,al,middle-47,yy+11,30,14,9,name=f'd2_a_{i}')
            vertical_stage_arrows(left, 'up')
            vertical_stage_arrows(right, 'up')
        else:
            # Direct I keeps its forward and feedback delay chains separate, as in the source figure.
            vertical_stage_arrows(left, 'down')
            vertical_stage_arrows(right, 'down')
            for i, (bl, al) in enumerate(coefficient_pairs):
                yy=y-30*(i+1)
                draw_math_at(c,r'z^{-1}',left-22,yy+12,30,13,10,name=f'd1_zl_{i}')
                draw_math_at(c,r'z^{-1}',right+2,yy+12,30,13,10,name=f'd1_zr_{i}')
                arrow(c,left,yy,middle,yy,RED,1.0); arrow(c,right,yy,middle,yy,RED,1.0)
                draw_math_at(c,bl,left+26,yy+11,25,14,10,name=f'd1_b_{i}')
                draw_math_at(c,al,middle+20,yy+11,30,14,9,name=f'd1_a_{i}')
            vertical_stage_arrows(middle, 'up')
    network(MARGIN_X+68,False)
    network(MARGIN_X+318,True)
    c.setFillColor(BLUE); c.setFont('CNB',9.5)
    c.drawString(MARGIN_X,top-205,'注意反馈部分系数符号')
    doc.y=top-h
    draw_formula_block(doc, r'H_1(z)=\frac{0.8z^3+2z^2+2z+6}{z^3+4z^2+3z+2},\qquad H_2(z)=\frac{5+2z^{-1}-0.5z^{-2}}{1+3z^{-1}+3z^{-2}+z^{-3}}', 'direct2_hw', fontsize=13, max_h=46)
    draw_note(doc, '直接 II 型注意', ['直接 II 型虽然节省延时单元，但反馈网络与前向网络共用状态变量，系数量化和舍入误差更容易影响极点位置。'])


def draw_cascade_example(doc):
    topology = cascade_parallel_source_topology()['cascade']
    doc.p('级联型先把系统函数分解成一阶或二阶因式，再把各二阶节串联。每个二阶节一般用直接 II 型实现。')
    draw_formula_block(doc, r'H(z)=A\prod_{i=1}^{K}H_i(z),\qquad H_i(z)=\frac{\beta_{0i}+\beta_{1i}z^{-1}+\beta_{2i}z^{-2}}{1-\alpha_{1i}z^{-1}-\alpha_{2i}z^{-2}}', 'cascade_section_formula', fontsize=14, max_h=50)
    h = 150
    doc.ensure(h + 10)
    c = doc.c
    top = doc.y
    y = top - 70
    x = MARGIN_X + 60
    draw_math_at(c, r'x(n)', x - 48, y + 8, 45, 20, 13, name='cas_x')
    for i, label in enumerate([r'H_1(z)', r'H_2(z)', r'\cdots', r'H_K(z)']):
        bx = x + i * 105
        c.setStrokeColor(RED)
        c.setLineWidth(1.2)
        c.rect(bx, y - 18, 62, 36, stroke=1, fill=0)
        draw_math_at(c, label, bx + 8, y, 48, 18, 12, name=f'cas_{i}')
        arrow(c, bx - 36 if i == 0 else bx - 43, y, bx, y, RED, 1.2)
    arrow(c, x + 3 * 105 + 62, y, x + 3 * 105 + 105, y, RED, 1.2)
    draw_math_at(c, r'y(n)', x + 3 * 105 + 110, y + 8, 45, 20, 13, name='cas_y')
    doc.y = top - h
    draw_formula_block(doc, r'H(z)=\frac{8-4z^{-1}+11z^{-2}-2z^{-3}}{1-1.25z^{-1}+0.75z^{-2}-0.125z^{-3}}', 'cascade_ex_h', fontsize=14, max_h=42)
    draw_formula_block(doc, r'H(z)=\frac{(2-0.379z^{-1})(4-1.24z^{-1}+5.264z^{-2})}{(1-0.25z^{-1})(1-z^{-1}+0.5z^{-2})}', 'cascade_ex_factor', fontsize=13, max_h=52)
    h = 154
    doc.ensure(h + 10)
    c = doc.c; top = doc.y; y = top - 40; x = MARGIN_X + 58
    c.setStrokeColor(TEXT); c.setFillColor(TEXT); c.setLineWidth(1.0)
    arrow(c, x, y, x + 430, y, TEXT, 1.0)
    draw_math_at(c, r'x(n)', x - 36, y + 13, 36, 15, 10, name='cascade_source_x')
    draw_math_at(c, r'y(n)', x + 436, y + 13, 36, 15, 10, name='cascade_source_y')

    def section(left, width, levels, feedback):
        right = left + width
        for i in range(levels):
            yy = y - 36 * (i + 1)
            c.line(left, y if i == 0 else yy + 36, left, yy)
            c.line(right, y if i == 0 else yy + 36, right, yy)
            arrow(c, left, yy, right, yy, TEXT, 0.9)
            draw_math_at(c, r'z^{-1}', (left + right) / 2 - 14, yy + 15, 28, 13, 9, name=f'cascade_delay_{left}_{i}')
        c.line(left, y, right, y)

    section(x + 88, 72, topology['delay_count'][0], topology['first_order_feedback'])
    section(x + 272, 88, topology['delay_count'][1], topology['second_order_feedback'])
    draw_math_at(c, r'0.25', x + 92, y - 52, 32, 13, 9.5, name='cascade_a1')
    draw_math_at(c, r'-0.379', x + 132, y - 52, 45, 13, 9.5, name='cascade_b1')
    draw_math_at(c, r'-0.5', x + 282, y - 91, 34, 13, 9.5, name='cascade_a2')
    draw_math_at(c, r'5.264', x + 328, y - 91, 40, 13, 9.5, name='cascade_b2')
    doc.y = top - h


def draw_parallel_example(doc):
    topology = cascade_parallel_source_topology()['example']
    doc.p('并联型把 H(z) 展开成部分分式，各分支输出相加。源课件给出的例题中，分解后各分支可以分别用一阶或二阶结构实现。')
    draw_formula_block(doc, r'H(z)=\sum_{i=1}^{(N+1)/2}\frac{\beta_{0i}+\beta_{1i}z^{-1}}{1-\alpha_{1i}z^{-1}-\alpha_{2i}z^{-2}}+\sum_{i=0}^{M-N}G_i z^{-i}', 'parallel_formula_full', fontsize=13, max_h=56)
    draw_formula_block(doc, r'y(n)=x(n)+\frac{1}{3}x(n-1)+\frac{3}{4}y(n-1)-\frac{1}{8}y(n-2)', 'parallel_diff_eq', fontsize=14, max_h=42)
    draw_formula_block(doc, r'H(z)=\frac{1+\frac{1}{3}z^{-1}}{1-\frac{3}{4}z^{-1}+\frac{1}{8}z^{-2}}=\frac{1+\frac{1}{3}z^{-1}}{(1-\frac{1}{2}z^{-1})(1-\frac{1}{4}z^{-1})}', 'parallel_decomp', fontsize=13, max_h=54)
    h = 210
    doc.ensure(h + 10)
    c = doc.c
    top = doc.y
    c.setStrokeColor(TEXT); c.setFillColor(TEXT); c.setLineWidth(1.0)
    c.setFont('CNB',10); c.drawCentredString(MARGIN_X+145,top-18,'级联实现'); c.drawCentredString(MARGIN_X+405,top-18,'并联实现')

    def first_order_section(x, y, width, feedback, feedforward, name):
        arrow(c,x,y,x+width,y,TEXT,1.0)
        left=x+18; right=x+width-18; lower=y-48
        c.line(left,y,left,lower); c.line(right,y,right,lower)
        arrow(c,right,lower,left,lower,TEXT,0.9)
        draw_math_at(c,r'z^{-1}',right-12,y-23,30,13,8.8,name=f'{name}_z')
        draw_math_at(c,feedback,left+8,lower-12,34,13,9,name=f'{name}_a')
        if feedforward:
            draw_math_at(c,feedforward,right-46,lower-12,38,13,9,name=f'{name}_b')

    # Left: two first-order sections in cascade, matching PPT 287.
    lx=MARGIN_X+34; ly=top-72
    draw_math_at(c,r'x(n)',lx-30,ly+12,34,15,10,name='example_cas_x')
    first_order_section(lx,ly,100,ratio_tex('1/4'),ratio_tex('1/3'),'example_cas_1')
    first_order_section(lx+112,ly,100,ratio_tex('1/2'),'', 'example_cas_2')
    draw_math_at(c,r'y(n)',lx+218,ly+12,34,15,10,name='example_cas_y')

    # Right: two independent first-order branches summed at the output bus.
    rx=MARGIN_X+315; ry=top-58; split=rx+12; merge=rx+180
    draw_math_at(c,r'x(n)',rx-36,ry-28,34,15,10,name='example_par_x')
    c.line(rx,ry-32,split,ry-32); c.line(split,ry,split,ry-96); c.line(merge,ry,merge,ry-96)
    for i,((gain,feedback),yy) in enumerate(zip(topology['parallel_branches'],(ry,ry-82))):
        first_order_section(split,yy,merge-split,ratio_tex(feedback),ratio_tex(gain),f'example_par_{i}')
    arrow(c,merge,ry-32,merge+24,ry-32,TEXT,1.0)
    draw_math_at(c,r'y(n)',merge+28,ry-20,34,15,10,name='example_par_y')
    doc.y = top - h
    draw_note(doc, '结构特点', ['级联型能单独调整各二阶节，便于控制滤波器特性；并联型各支路互不影响，适合部分分式展开后实现。', '源课件强调：级联型常用于零极点配对，并联型各分支可并行实现。'])


def draw_analog_digital_bridge(doc):
    h = 292
    doc.ensure(h + 10)
    c = doc.c
    top = doc.y
    c.setFont('CNB', 11); c.setFillColor(TEXT)
    c.drawString(MARGIN_X, top - 16, '模拟滤波器和数字滤波器')

    left = MARGIN_X + 36
    block_x = left + 62
    block_w = 102
    out_x = block_x + block_w + 180

    def row(y_top, discrete=False):
        time_var = r'x(n)' if discrete else r'x(t)'
        impulse = r'h(n)' if discrete else r'h(t)'
        output = r'y(n)=x(n)*h(n)' if discrete else r'y(t)=x(t)*h(t)'
        freq_in = r'X(z)' if discrete else r'X(s)'
        freq_h = r'H(z)' if discrete else r'H(s)'
        freq_out = r'Y(z)=X(z)\cdot H(z)' if discrete else r'Y(s)=X(s)\cdot H(s)'
        transform = 'ZT' if discrete else 'LT'
        time_y, freq_y = y_top, y_top - 72

        draw_math_at(c, time_var, left - 15, time_y + 8, 52, 19, 13, name=f'bridge_time_in_{discrete}')
        arrow(c, left + 25, time_y, block_x, time_y, RED, 1.3, 6)
        c.setStrokeColor(RED); c.setLineWidth(1.3)
        c.rect(block_x, time_y - 17, block_w, 34, stroke=1, fill=0)
        draw_math_at(c, impulse, block_x + 23, time_y + 10, 60, 22, 14, name=f'bridge_impulse_{discrete}')
        arrow(c, block_x + block_w, time_y, out_x, time_y, RED, 1.3, 6)
        draw_math_at(c, output, block_x + block_w + 12, time_y + 10, 150, 20, 12.5,
                     name=f'bridge_time_out_{discrete}')
        c.setFillColor(TEXT); c.setFont('CNB', 10)
        c.drawString(out_x + 8, time_y - 4, '时域卷积')

        draw_math_at(c, freq_in, left - 15, freq_y + 8, 52, 19, 13, name=f'bridge_freq_in_{discrete}')
        arrow(c, left + 25, freq_y, block_x, freq_y, RED, 1.3, 6)
        c.setStrokeColor(RED); c.rect(block_x, freq_y - 17, block_w, 34, stroke=1, fill=0)
        draw_math_at(c, freq_h, block_x + 23, freq_y + 10, 60, 22, 14, name=f'bridge_transfer_{discrete}')
        arrow(c, block_x + block_w, freq_y, out_x, freq_y, RED, 1.3, 6)
        draw_math_at(c, freq_out, block_x + block_w + 9, freq_y + 10, 170, 20, 12,
                     name=f'bridge_freq_out_{discrete}')
        c.setFillColor(TEXT); c.setFont('CNB', 10)
        c.drawString(out_x + 8, freq_y - 4, '频域相乘')

        for j, xx in enumerate((left + 17, block_x + block_w / 2, block_x + block_w + 65)):
            arrow(c, xx, time_y - 18, xx, freq_y + 18, colors.HexColor('#163DFF'), 1.4, 7)
            c.setFillColor(TEXT); c.setFont('CNB', 9)
            c.drawString(xx + 5, (time_y + freq_y) / 2 - 3, transform)

        right_expr = (r'H(z)|_{z=e^{j\omega}}=H(e^{j\omega})' if discrete
                      else r'H(s)|_{s=j\Omega}=H(j\Omega)')
        draw_math_at(c, right_expr, MARGIN_X + 410, freq_y + 9, 145, 22, 12,
                     name=f'bridge_relation_{discrete}')

    row(top - 58, discrete=False)
    c.setFillColor(TEXT); c.setFont('CNB', 10)
    c.drawString(MARGIN_X + 8, top - 156, '时域离散')
    row(top - 184, discrete=True)
    c.setFont('CNB', 10)
    c.drawString(MARGIN_X + 8, top - 281, '频域周期')
    doc.y = top - h


def draw_butter_tables_full(doc):
    rows = [
        ('1', r'(p+1)'),
        ('2', r'(p^{2}+1.4142p+1)'),
        ('3', r'(p+1)(p^{2}+p+1)'),
        ('4', r'(p^{2}+0.7654p+1)(p^{2}+1.8478p+1)'),
        ('5', r'(p+1)(p^{2}+0.6180p+1)(p^{2}+1.6180p+1)'),
        ('6', r'(p^{2}+0.5176p+1)(p^{2}+1.4142p+1)(p^{2}+1.9319p+1)'),
        ('7', r'(p+1)(p^{2}+0.4450p+1)(p^{2}+1.2470p+1)(p^{2}+1.8019p+1)'),
        ('8', r'(p^{2}+0.3902p+1)(p^{2}+1.1111p+1)(p^{2}+1.6629p+1)(p^{2}+1.9616p+1)'),
        ('9', r'(p+1)(p^{2}+0.3473p+1)(p^{2}+p+1)(p^{2}+1.5321p+1)(p^{2}+1.8794p+1)'),
    ]
    doc.h3('巴特沃斯归一化多项式 B(p) 因式分解表')
    row_h = 34
    h = row_h * (len(rows) + 1) + 8
    doc.ensure(h + 12)
    c = doc.c
    top = doc.y
    x = MARGIN_X
    widths = [46, CONTENT_W - 46]
    c.setFillColor(BLUE_DARK)
    c.rect(x, top - row_h, CONTENT_W, row_h, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont('CNB', 9)
    c.drawCentredString(x + widths[0] / 2, top - 21, 'N')
    c.drawCentredString(x + widths[0] + widths[1] / 2, top - 21, 'B(p)')
    c.setStrokeColor(colors.HexColor('#CADCEB'))
    for i, (n, expr) in enumerate(rows):
        y = top - row_h * (i + 2)
        c.setFillColor(colors.HexColor('#F4F8FB') if i % 2 else colors.white)
        c.rect(x, y, CONTENT_W, row_h, stroke=0, fill=1)
        c.setStrokeColor(colors.HexColor('#CADCEB'))
        c.line(x, y, x + CONTENT_W, y)
        c.line(x + widths[0], y, x + widths[0], y + row_h)
        c.setFillColor(TEXT)
        c.setFont('CN', 9)
        c.drawCentredString(x + widths[0] / 2, y + 12, n)
        draw_math_at(c, expr, x + widths[0] + 8, y + 17, widths[1] - 16, 19, 11, name=f'butter_full_{n}')
    c.rect(x, top - row_h * (len(rows) + 1), CONTENT_W, row_h * (len(rows) + 1), stroke=1, fill=0)
    doc.y = top - h - 8
    doc.h3('巴特沃斯展开式系数表')
    coeffs = [
        ['1','1.0000'],
        ['2','1.0000','1.4142'],
        ['3','1.0000','2.0000','2.0000'],
        ['4','1.0000','2.6131','3.4142','2.6131'],
        ['5','1.0000','3.2361','5.2361','5.2361','3.2361'],
        ['6','1.0000','3.8637','7.4641','9.1416','7.4641','3.8637'],
        ['7','1.0000','4.4940','10.0978','14.5918','14.5918','10.0978','4.4940'],
        ['8','1.0000','5.1258','13.1371','21.8462','25.6884','21.8462','13.1371','5.1258'],
        ['9','1.0000','5.7588','16.5817','31.1634','41.9864','41.9864','31.1634','16.5817','5.7588'],
    ]
    headers=['N','b0','b1','b2','b3','b4','b5','b6','b7','b8']
    row_h=22
    h=row_h*(len(coeffs)+1)+8
    doc.ensure(h+12)
    c=doc.c
    top=doc.y
    colw=CONTENT_W/len(headers)
    c.setFillColor(colors.HexColor('#8B0037'))
    c.rect(MARGIN_X, top-row_h, CONTENT_W, row_h, stroke=0, fill=1)
    c.setFillColor(colors.white); c.setFont('CNB',7.6)
    for i,hh in enumerate(headers): c.drawCentredString(MARGIN_X+i*colw+colw/2, top-15, hh)
    for r,row in enumerate(coeffs):
        y=top-row_h*(r+2)
        c.setFillColor(colors.HexColor('#F6EEF2') if r%2 else colors.white)
        c.rect(MARGIN_X,y,CONTENT_W,row_h,stroke=0,fill=1)
        c.setFillColor(TEXT); c.setFont('CN',6.7)
        for i,val in enumerate(row):
            c.drawCentredString(MARGIN_X+i*colw+colw/2,y+7,val)
    c.setStrokeColor(colors.HexColor('#D8BFCB'))
    c.rect(MARGIN_X,top-row_h*(len(coeffs)+1),CONTENT_W,row_h*(len(coeffs)+1),stroke=1,fill=0)
    doc.y=top-h-8
def build():
    register_fonts()
    doc = Doc(PDF_PATH)
    doc.section = '第五章 IIR滤波器设计'
    doc.start()

    doc.h1('第五章 IIR系统的网络结构与滤波器设计')
    doc.p('本章讨论 IIR 数字滤波器的网络结构及模拟滤波器设计。原课件中的封面和目录页在讲义中转为章节导读，正文内容按知识点连续展开。')
    doc.bullet(['信号流图与数字滤波器结构表示方法。', '直接 I 型、直接 II 型、级联型、并联型 IIR 网络结构。', '模拟滤波器指标、巴特沃斯低通滤波器及其设计表。'])

    doc.h2('5.1 信号流图与数字滤波器')
    doc.p('数字滤波器是输入、输出均为数字信号，并通过数值运算改变输入信号频率成分比例的系统。对 LTI 系统，滤波可以从时域卷积或频域乘积理解。')
    draw_formula_block(doc, r'y(n)=\sum_{m=-\infty}^{\infty}x(m)h(n-m)=F^{-1}\{X(e^{j\omega})H(e^{j\omega})\}', 'lti_filter', fontsize=15, max_h=38)
    doc.p('数字滤波器通常分为经典滤波器和现代滤波器。按冲激响应长度可分为 IIR 和 FIR：IIR 为无限长冲激响应，FIR 为有限长冲激响应。')
    doc.bullet(['IIR：巴特沃斯、切比雪夫、椭圆、贝塞尔等。', 'FIR：窗函数法、频率采样法、等波纹逼近法等。'])
    doc.h3('结构表示方法')
    doc.p('数字滤波器结构常用方框图和信号流图表示。基本运算包括相加、乘以常数和单位延时。')
    draw_basic_ops_table(doc)
    doc.h3('例 1 二阶数字滤波器')
    draw_formula_block(doc, r'y(n)=a_1y(n-1)+a_2y(n-2)+b_0x(n)', 'second_order_eq', fontsize=17, max_h=42)
    draw_second_order_diagrams(doc)
    draw_note(doc, '结构阅读', ['方框图适合看运算步骤，信号流图适合分析网络节点和分支。后续 IIR 结构统一按信号流图理解。'])

    doc.h2('5.2 IIR 基本网络结构')
    doc.p('IIR 滤波器的差分方程代表一种最直接的计算公式，系统函数一般写为有理式。因为存在反馈，稳定 IIR 系统的极点必须在单位圆内。')
    draw_formula_block(doc, r'y(n)=\sum_{i=1}^{N}a_i y(n-i)+\sum_{i=0}^{M}b_i x(n-i)', 'iir_diff', fontsize=17, max_h=42)
    draw_formula_block(doc, r'H(z)=\frac{\sum_{i=0}^{M} b_i z^{-i}}{1-\sum_{i=1}^{N}a_i z^{-i}}', 'iir_hz', fontsize=18, max_h=50)
    doc.h3('5.2.1 IIR 滤波器特点')
    doc.bullet([
        '单位脉冲响应 h(n) 为无限长，n 趋于无穷时仍可能不为零。',
        '系统函数 H(z) 在有限 z 平面内存在极点。',
        '结构上存在输出到输入的反馈，因此属于递归型网络。',
        '因果稳定 IIR 滤波器的全部极点必须位于单位圆内。',
        '基本结构包括直接型、级联型和并联型；实现时需关注系数量化误差和运算舍入误差。',
    ])

    doc.h2('5.2.2 直接 I 型 IIR 滤波器')
    doc.p('直接 I 型按差分方程直接展开：输入端为 M 节延时链的横向网络，输出端为 N 节延时链的反馈网络。')
    draw_direct_i_general(doc)
    draw_note(doc, '直接 I 型特点', [
        '两个网络级联：横向 M 节延时网络实现零点，反馈 N 节延时网络实现极点。',
        '共需 M+N 个延时单元；系数不能直接决定单个零极点，不利于滤波器性能控制。',
        '极点对系数变化过于灵敏，容易出现不稳定或产生较大误差。',
    ])

    doc.new_page()
    doc.h2('5.2.3 直接 II 型 IIR 滤波器')
    doc.p('直接 II 型通过中间变量把直接 I 型前后两个延时链合并，所需延时单元最少，因此也称典范型。')
    draw_direct_ii_general(doc)
    draw_note(doc, '直接 II 型特点', [
        '横向 M 节网络与反馈 N 节网络交换次序并共享延时链。',
        '当 N 不小于 M 时只需 N 个延时单元，所需延时单元最少，故称为典范型。',
        '仍具有直接型的一般缺点：系数变化容易改变零极点位置和滤波特性。',
    ])
    draw_formula_block(doc, r'H(z)=\frac{8-4z^{-1}+11z^{-2}-2z^{-3}}{1-\frac{5}{4}z^{-1}+\frac{3}{4}z^{-2}-\frac{1}{8}z^{-3}}', 'direct2_example', fontsize=16, max_h=54)
    doc.p('例题中先将分母首项归一化为 1，并把系统函数写成 z 的负幂形式，再据此画出直接 I 型和直接 II 型结构。')
    draw_direct_ii_examples(doc)
    draw_note(doc, '归一化', ['画 IIR 结构图前，必须先把 H(z) 化为 z 的负幂有理式，分母首项归一化为 1。'])

    doc.h2('5.2.4 级联型 IIR 数字滤波器')
    doc.p('级联型将系统函数分解为若干一阶或二阶子系统的乘积，每个子系统单独实现后再串联。该结构便于按零极点成对控制滤波器特性。')
    draw_formula_block(doc, r'H(z)=A\prod_{i=1}^{K}H_i(z)', 'cascade_general', fontsize=17, max_h=38)
    draw_cascade_example(doc)
    doc.bullet([
        '每个二阶节可单独控制一对零点或一对极点，便于控制频率响应和调整滤波器。',
        '每个子系统可采用直接 II 型实现；硬件可分时复用同一二阶节，软件可调用同一子函数。',
        '对有限字长的敏感程度通常低于直接型，但不同零极点配对方式仍会影响量化误差和稳定性。',
    ])

    doc.h2('5.2.5 并联型 IIR 数字滤波器结构')
    doc.p('并联型将 H(z) 展开为部分分式，各子系统输出相加。该结构常由部分分式展开直接得到。')
    draw_parallel_iir(doc)
    draw_parallel_example(doc)
    draw_note(doc, '并联型特点', [
        '并联型可以单独调整极点位置，但不能像级联型那样直接控制零点，因此不适合对零点位置精度要求很高的陷波器或窄带带阻滤波器。',
        '各基本网络并联，运算误差互不影响，没有直接型和级联型的误差累积，运算误差较小。',
        '硬件实现时各子系统可以并行实现，速度较快。',
    ])

    doc.h2('5.3 模拟滤波器设计 - 巴特沃斯')
    doc.p('IIR 数字滤波器常由模拟滤波器设计出发，再通过变换得到数字滤波器。本节先整理模拟低通、高通、带通、带阻的典型幅频特性。')
    draw_analog_digital_bridge(doc)
    draw_filter_type_plots(doc)
    draw_digital_filter_type_plots(doc)

    doc.h2('5.3.1 模拟低通滤波器的设计指标及逼近方法')
    doc.p('模拟低通滤波器设计以通带截止频率、阻带截止频率、通带最大衰减和阻带最小衰减为核心指标。')
    draw_butterworth_response(doc)
    draw_formula_block(doc, r'|H_a(j\Omega_c)|=\frac{\sqrt{2}}{2}=0.707,\qquad -20\lg |H_a(j\Omega_c)|=3\mathrm{dB}', 'three_db', fontsize=16, max_h=42)
    draw_formula_block(doc, r'\alpha_p=20\lg\frac{|H_a(j0)|}{|H_a(j\Omega_p)|},\qquad \alpha_s=20\lg\frac{|H_a(j0)|}{|H_a(j\Omega_s)|}', 'attenuation_defs', fontsize=15, max_h=42)

    doc.h2('5.3.2 巴特沃斯低通滤波器的设计方法')
    doc.p('巴特沃斯低通滤波器的幅度平方函数如下。阶数 N 越大，过渡带越窄，幅度响应越接近理想低通。')
    draw_formula_block(doc, r'|H_a(j\Omega)|^2=\frac{1}{1+\left(\frac{\Omega}{\Omega_c}\right)^{2N}}', 'butter_mag', fontsize=18, max_h=48)
    draw_formula_block(doc, r'H_a(s)H_a(-s)=\frac{1}{1+\left(\frac{s}{j\Omega_c}\right)^{2N}}', 'butter_product', fontsize=18, max_h=48)
    doc.p('将幅度平方函数分母写成 s 平面极点形式，取左半平面的 N 个极点构成稳定模拟低通滤波器。')
    draw_formula_block(doc, r's_k=\Omega_c e^{j\left(\frac{\pi}{2}+\frac{(2k+1)\pi}{2N}\right)},\qquad k=0,1,\ldots,2N-1', 'butter_poles', fontsize=15, max_h=46)
    doc.h3('巴特沃斯多项式表')
    draw_butter_tables_full(doc)
    draw_note(doc, '查表使用', ['按阶数 N 选取 B(p)。若截止频率不是 1，应先完成频率归一化，再由归一化低通恢复实际系统函数。', '因式分解形式便于级联实现；展开式便于直接计算系数。'])

    doc.save()
    NOTE_PATH.write_text('# 第九批手绘复刻版校对记录\n\n- 根据用户最新要求，本版不再直接整块裁原图嵌入。\n- 已手绘复刻：基本运算表、二阶方框图/信号流图、直接 I 型结构、并联型结构、模拟滤波器四类响应图、巴特沃斯 3dB 指标图。\n- 保留原则：图形拓扑、颜色、箭头、标签和公式含义按原 PPT；只调整间距以避免重叠。\n- 已补入：直接 II 型例题、级联/并联实现公式与例题、模拟到数字滤波器桥接图、1-9 阶巴特沃斯因式分解表和展开式系数表。\n', encoding='utf-8')


if __name__ == '__main__':
    build()






