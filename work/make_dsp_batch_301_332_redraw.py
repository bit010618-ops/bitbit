from pathlib import Path
import sys
from reportlab.lib import colors

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work'
sys.path.insert(0, str(WORK))

from make_dsp_batch_266_300_redraw import (
    BLUE, BLUE_DARK, CONTENT_W, MARGIN_X, TEXT, Doc, register_fonts,
    RED, PURPLE, PALE_BLUE, formula_png, draw_math_at, draw_formula_block,
    draw_note, arrow, wrap, draw_centered_multiline_text
)
from make_dsp_sample_handout_v2 import draw_auto_math_text

OUT_DIR = ROOT / 'outputs'
PDF_PATH = OUT_DIR / 'DSP讲义重制_第十批_原PPT301-332页_IIR设计方法_手绘复刻版.pdf'
NOTE_PATH = OUT_DIR / 'DSP讲义重制_第十批_原PPT301-332页_IIR设计方法_手绘复刻版_校对记录.md'


def draw_curve_pair(doc, title, mode='low_high'):
    h = 160
    doc.ensure(h + 10)
    c = doc.c
    top = doc.y
    draw_auto_math_text(c,MARGIN_X,top-14,title,font='CNB',size=10,color=BLUE_DARK)
    kinds = ['low', 'high'] if mode == 'low_high' else ['band', 'stop']
    for idx, kind in enumerate(kinds):
        x = MARGIN_X + 60 + idx * 250
        y = top - 100
        arrow(c, x, y, x + 180, y, colors.blue, 1.1, 5)
        arrow(c, x, y, x, y + 70, colors.blue, 1.1, 5)
        c.setStrokeColor(RED)
        c.setLineWidth(1.6)
        if kind == 'low':
            c.line(x, y+52, x+70, y+52); c.bezier(x+70,y+52,x+100,y+52,x+112,y+12,x+145,y+12); c.line(x+145,y+12,x+175,y+12)
            c.setFillColor(TEXT); c.setFont('CNB', 13); c.drawString(x+92, y+35, '低通')
        elif kind == 'high':
            c.line(x, y+12, x+55, y+12); c.bezier(x+55,y+12,x+90,y+12,x+105,y+52,x+140,y+52); c.line(x+140,y+52,x+175,y+52)
            c.setFillColor(TEXT); c.setFont('CNB', 13); c.drawString(x+106, y+35, '高通')
        elif kind == 'band':
            c.line(x, y+10, x+45, y+10); c.line(x+45,y+10,x+70,y+52); c.line(x+70,y+52,x+125,y+52); c.line(x+125,y+52,x+150,y+10); c.line(x+150,y+10,x+175,y+10)
            c.setFillColor(TEXT); c.setFont('CNB', 13); c.drawString(x+72, y+62, '带通')
        else:
            c.line(x, y+52, x+45, y+52); c.line(x+45,y+52,x+75,y+10); c.line(x+75,y+10,x+120,y+10); c.line(x+120,y+10,x+150,y+52); c.line(x+150,y+52,x+175,y+52)
            c.setFillColor(TEXT); c.setFont('CNB', 13); c.drawString(x+72, y+62, '带阻')
    doc.y = top - h


def draw_design_flow(doc):
    flow_h = 185
    doc.ensure(flow_h + 55)
    draw_formula_block(
        doc,
        r's=\frac{2}{T}\frac{1-z^{-1}}{1+z^{-1}},\qquad \Omega=\frac{2}{T}\tan\frac{\omega}{2}',
        'flow_bilinear', fontsize=14, max_h=36, gap=10
    )
    c = doc.c
    top = doc.y
    items = ['数字滤波器指标', '模拟低通指标', '设计模拟低通滤波器', '转换为数字系统函数', 'IIR 数字滤波器']
    x = MARGIN_X + 70
    y = top - 38
    for i, item in enumerate(items):
        yy = y - i * 30
        c.setStrokeColor(RED)
        c.rect(x, yy - 11, 180, 22, stroke=1, fill=0)
        draw_centered_multiline_text(c, x + 90, yy, item, 'CNB', 8.8, color=TEXT)
        if i < len(items)-1:
            arrow(c, x+90, yy-11, x+90, yy-24, RED, 1.0, 5)
    doc.y = min(doc.y, top - flow_h)


def draw_impulse_invariance_flow(doc):
    """Source page 319: Laplace/sample/z-transform correspondence."""
    h = 278
    doc.ensure(h + 12)
    c = doc.c
    top = doc.y
    left_x = MARGIN_X + 118
    formula_x = MARGIN_X + 270
    rows = [top - 28, top - 92, top - 160, top - 232]

    labels = [
        "模拟滤波器\n传递函数 H(s)",
        "模拟滤波器\n单位脉冲响应 h(t)",
        "数字滤波器\n单位脉冲响应 h(n)",
        "数字滤波器\n系统函数 H(z)",
    ]
    for y, label in zip(rows, labels):
        draw_centered_multiline_text(c, left_x, y, label, 'CNB', 10.2, leading=14, color=TEXT)

    transitions = ["拉氏反变换", "时域采样\nt=nT", "z 变换"]
    for index, transition in enumerate(transitions):
        start = rows[index] - 24
        end = rows[index + 1] + 24
        arrow(c, left_x, start, left_x, end, BLUE, 1.35, 7)
        draw_centered_multiline_text(
            c, left_x + 52, (start + end) / 2, transition,
            'CNB', 8.8, leading=12, color=TEXT
        )

    arrow(c, MARGIN_X + 22, rows[1] + 12, MARGIN_X + 22, rows[2] - 12, RED, 1.4, 7)
    draw_centered_multiline_text(c, MARGIN_X + 22, rows[1] + 31, "时域离散", 'CNB', 8.6, color=TEXT)
    draw_centered_multiline_text(c, MARGIN_X + 22, rows[2] - 31, "频域周期", 'CNB', 8.6, color=TEXT)

    formulas = [
        (r'H(s)=\sum_{i=1}^{N}\frac{A_i}{s-s_i}', 'impulse_flow_hs', 14.5),
        (r'h(t)=\sum_{i=1}^{N}A_i e^{s_it}u(t)', 'impulse_flow_ht', 14.5),
        (r'h(n)=\sum_{i=1}^{N}T A_i e^{s_inT}u(nT)', 'impulse_flow_hn', 14.0),
        (r'H(z)=\sum_{i=1}^{N}\frac{T A_i}{1-e^{s_iT}z^{-1}}', 'impulse_flow_hz', 14.0),
    ]
    for y, (expr, name, fontsize) in zip(rows, formulas):
        draw_math_at(c, expr, formula_x, y, max_w=220, max_h=34, fontsize=fontsize, name=name)

    for index, transition in enumerate(transitions):
        start = rows[index] - 22
        end = rows[index + 1] + 22
        arrow(c, formula_x + 110, start, formula_x + 110, end, RED, 1.25, 7)
        draw_centered_multiline_text(
            c, formula_x + 155, (start + end) / 2, transition,
            'CNB', 8.6, leading=12, color=TEXT
        )

    doc.y = top - h


def comparison_table(doc):
    rows = [
        ('方法', '优点', '缺点'),
        ('脉冲响应不变法', '时域逼近好；频率关系线性', '存在频谱混叠，不适合高通、带阻'),
        ('双线性变换法', '避免混叠；稳定性映射好', '频率关系非线性，需要预畸变'),
    ]
    h = 108
    doc.ensure(h + 12)
    c = doc.c
    top = doc.y
    col = [110, 180, CONTENT_W - 290]
    row_h = [24, 42, 42]
    y = top
    for r,row in enumerate(rows):
        y -= row_h[r]
        c.setFillColor(BLUE_DARK if r == 0 else (colors.HexColor('#F4F8FB') if r % 2 else colors.white))
        c.rect(MARGIN_X, y, CONTENT_W, row_h[r], stroke=0, fill=1)
        x = MARGIN_X
        for ci,w in enumerate(col):
            c.setStrokeColor(colors.HexColor('#CADCEB'))
            if ci > 0: c.line(x, y, x, y + row_h[r])
            c.setFillColor(colors.white if r == 0 else TEXT)
            c.setFont('CNB' if r == 0 or ci == 0 else 'CN', 8.0)
            parts = wrap(row[ci], w-10, 'CNB' if r == 0 or ci == 0 else 'CN', 8.0)
            yy = y + row_h[r] - 14
            for part in parts:
                c.drawString(x + 6, yy, part)
                yy -= 11
            x += w
    c.setStrokeColor(colors.HexColor('#CADCEB'))
    c.rect(MARGIN_X, top - sum(row_h), CONTENT_W, sum(row_h), stroke=1, fill=0)
    doc.y = top - h - 4


def analog_bandpass_example(doc):
    """Source pages 314-315: normalized low-pass prototype for a band-pass design."""
    doc.h3('例：模拟带通滤波器的频率变换')
    doc.p('原课件给定模拟带通指标，先把通带边缘归一化为 ηl=4、ηu=6，并取中心频率 η0=5，再把两侧阻带频率分别映射到低通原型。')
    draw_formula_block(
        doc,
        r'\eta_{s1}=4.15,\qquad \eta_{s2}=6,\qquad \eta_0=5',
        'analog_bp_etas', fontsize=15, max_h=38
    )
    draw_formula_block(
        doc,
        r'\lambda_{sp1}=\frac{\eta_{s1}^2-\eta_0^2}{\eta_{s1}B}=1.833,\qquad '
        r'\lambda_{sp2}=\frac{\eta_{s2}^2-\eta_0^2}{\eta_{s2}B}=-1.874',
        'analog_bp_lambdas', fontsize=13.5, max_h=50
    )
    draw_formula_block(
        doc,
        r'\lambda_{sp1}=1.833,\qquad \lambda_{sp2}=-1.874',
        'analog_bp_lambda_values', fontsize=15, max_h=34
    )
    doc.p('两侧阻带映射值一般不同，按原课件规则取绝对值较小者作为低通原型的阻带指标，因此取 |λs|=1.833。')
    draw_formula_block(
        doc,
        r'k_{sp}=5.5469,\qquad \lambda_{sp}=1.833,\qquad '
        r'N=\frac{\lg k_{sp}}{\lg\lambda_{sp}}=2.9274\Rightarrow N=3',
        'analog_bp_order', fontsize=14, max_h=44
    )
    draw_formula_block(
        doc,
        r'H_a(s)=\left.H(p)\right|_{p=\frac{s^2+\Omega_0^2}{sB}}',
        'analog_bp_transform', fontsize=16, max_h=38
    )
    draw_note(doc, '带通变换要点', ['先把四个边缘频率映射为低通指标，再设计低通原型。', '带通变换会使系统阶数加倍：三阶低通原型得到六阶带通滤波器。'])


def build():
    register_fonts()
    doc = Doc(PDF_PATH)
    doc.section = '第五章 IIR滤波器设计'
    doc.start()

    doc.h1('第五章 IIR 滤波器设计方法续讲')
    doc.p('本批承接巴特沃斯低通滤波器设计，补全阶数确定、频率归一化、模拟滤波器频带变换，以及由模拟滤波器得到 IIR 数字滤波器的两种常用方法。')

    doc.h2('5.3.2 巴特沃斯低通滤波器的设计方法：阶数确定')
    doc.p('阶数 N 的大小主要影响幅度特性下降的速度，应由技术指标确定。把通带和阻带指标代入巴特沃斯幅度平方函数，可得到阶数和频率参数。')
    draw_formula_block(doc, r'|H_a(j\Omega)|^2=\frac{1}{1+\left(\frac{\Omega}{\Omega_c}\right)^{2N}}', 'b301_mag', fontsize=17, max_h=45)
    draw_formula_block(doc, r'1+\left(\frac{\Omega_p}{\Omega_c}\right)^{2N}=10^{\frac{\alpha_p}{10}},\qquad 1+\left(\frac{\Omega_s}{\Omega_c}\right)^{2N}=10^{\frac{\alpha_s}{10}}', 'b301_subs', fontsize=15, max_h=46)
    draw_formula_block(doc, r'\lambda_{sp}=\frac{\Omega_s}{\Omega_p},\qquad k_{sp}=\sqrt{\frac{10^{\frac{\alpha_s}{10}}-1}{10^{\frac{\alpha_p}{10}}-1}},\qquad N=\frac{\lg k_{sp}}{\lg \lambda_{sp}}', 'b303_n', fontsize=15, max_h=50)
    draw_note(doc, '阶数取整', ['求出的 N 可能是小数，实际滤波器阶数应取大于等于 N 的最小整数。', '若技术指标中没有给出 3 dB 截止频率，可先按通带和阻带指标求出 Ωc。'])
    draw_formula_block(doc, r'\Omega_c=\frac{\Omega_p}{\left(10^{\frac{\alpha_p}{10}}-1\right)^{\frac{1}{2N}}}=\frac{\Omega_s}{\left(10^{\frac{\alpha_s}{10}}-1\right)^{\frac{1}{2N}}}', 'b304_wc', fontsize=14, max_h=48)

    doc.h3('例：按技术指标设计巴特沃斯低通滤波器')
    doc.p('已知通带截止频率 fp=5 kHz，通带最大衰减 αp=2 dB，阻带截止频率 fs=12 kHz，阻带最小衰减 αs=30 dB。')
    draw_formula_block(doc, r'k_{sp}=\sqrt{\frac{10^{\frac{30}{10}}-1}{10^{\frac{2}{10}}-1}}=41.328,\qquad \lambda_{sp}=\frac{\Omega_s}{\Omega_p}=\frac{12}{5}=2.4', 'b307_ksp', fontsize=14, max_h=45)
    draw_formula_block(doc, r'N=\frac{\lg k_{sp}}{\lg\lambda_{sp}}=4.2509\Rightarrow N=5', 'b307_n', fontsize=16, max_h=35)
    draw_formula_block(doc, r'p_k=e^{j\left(\frac{\pi}{2}+\frac{(2k+1)\pi}{2N}\right)},\quad k=0,1,\ldots,N-1', 'b307_pk', fontsize=15, max_h=40)
    doc.p('查表取 N=5 的归一化巴特沃斯多项式，再按 Ωc 去归一化得到实际模拟低通系统函数。')
    draw_formula_block(doc, r'H_a(s)=\frac{\Omega_c^5}{b_0\Omega_c^5+b_1\Omega_c^4s+b_2\Omega_c^3s^2+b_3\Omega_c^2s^3+b_4\Omega_cs^4+s^5}', 'b308_ha', fontsize=13, max_h=48)

    doc.h2('5.3.3 模拟滤波器的频带变换')
    doc.p('原型低通滤波器可以通过频率变量替换得到高通、带通和带阻滤波器。设计步骤是先把目标指标换算为归一化低通指标，求得 H(p)，再代回变换式得到目标模拟滤波器。')
    draw_curve_pair(doc, '低通到高通变换', 'low_high')
    draw_formula_block(doc, r'\lambda=\frac{1}{\eta},\qquad H_a(s)=\left. H(p)\right|_{p=\frac{\Omega_c}{s}}', 'b310_lh', fontsize=16, max_h=40)
    draw_curve_pair(doc, '低通到带通/带阻变换', 'band_stop')
    draw_formula_block(doc, r'\lambda=\frac{\eta^2-\eta_0^2}{\eta B},\qquad B=\eta_u-\eta_l,\qquad \eta_0^2=\eta_l\eta_u', 'b312_band', fontsize=15, max_h=46)
    draw_formula_block(doc, r'H_a(s)=\left. H(p)\right|_{p=\frac{s^2+\Omega_0^2}{sB}},\qquad H_a(s)=\left. H(p)\right|_{p=\frac{sB}{s^2+\Omega_0^2}}', 'b317_transforms', fontsize=13, max_h=54)
    draw_note(doc, '频带变换要点', ['归一化时按原课件规则取绝对值较小的 λs。', '先设计归一化低通 H(p)，再把 p 换成对应的频带变换表达式。'])
    analog_bandpass_example(doc)

    doc.h2('5.4 IIR 数字滤波器设计')
    doc.p('利用模拟滤波器设计数字滤波器，本质是由模拟系统函数得到数字系统函数。常用方法包括脉冲响应不变法和双线性变换法。')
    draw_design_flow(doc)

    doc.h2('5.4.1 脉冲响应不变法')
    doc.p('脉冲响应不变法令数字滤波器的单位脉冲响应等于模拟滤波器冲激响应的抽样值，从而保持时域响应。')
    draw_impulse_invariance_flow(doc)
    draw_note(doc, '脉冲响应不变法特点', ['优点：时域逼近良好；模拟频率 Ω 与数字频率 ω 之间是线性关系，ω=ΩT。', '缺点：存在频谱混叠，只适用于带限模拟滤波器；不适用于高通和带阻滤波器。'])

    doc.h2('5.4.2 双线性变换法')
    doc.p('双线性变换法采用非线性压缩，把整个 jΩ 轴映射到单位圆上，避免频谱混叠。')
    draw_formula_block(doc, r's=c\frac{1-z^{-1}}{1+z^{-1}},\qquad c=\frac{2}{T}', 'bilinear_s', fontsize=16, max_h=42)
    draw_formula_block(doc, r'\Omega=\frac{2}{T}\tan\left(\frac{\omega}{2}\right),\qquad \omega=2\arctan\left(\frac{\Omega T}{2}\right)', 'bilinear_warp', fontsize=16, max_h=44)
    doc.p('由于 Ω 与 ω 之间是非线性关系，设计前必须进行频率预畸变，把数字指标换算成模拟指标。')
    draw_formula_block(doc, r'\Omega_p=\frac{2}{T}\tan\left(\frac{\omega_p}{2}\right),\qquad \Omega_s=\frac{2}{T}\tan\left(\frac{\omega_s}{2}\right)', 'prewarp', fontsize=16, max_h=42)
    doc.h3('例：用双线性变换法设计低通滤波器')
    doc.p('原课件例题把数字通带与阻带截止频率预畸变为模拟指标，再设计巴特沃斯模拟低通，最后代入双线性变换得到 H(z)。')
    draw_formula_block(doc, r'\omega_p=0.2\pi,\ \alpha_p=1\mathrm{dB},\qquad \omega_s=0.3\pi,\ \alpha_s=15\mathrm{dB}', 'bilinear_specs', fontsize=15, max_h=38)
    draw_formula_block(doc, r'\Omega_p=0.65\pi\,\mathrm{rad}\,\mathrm{s}^{-1},\qquad \Omega_s=1.019\pi\,\mathrm{rad}\,\mathrm{s}^{-1}', 'bilinear_prewarp_num', fontsize=15, max_h=38)
    draw_formula_block(doc, r'k_{sp}=\sqrt{\frac{10^{\frac{15}{10}}-1}{10^{\frac{1}{10}}-1}}=10.8751,\qquad N=\frac{\lg k_{sp}}{\lg \lambda_{sp}}=5.3056\Rightarrow N=6', 'bilinear_order', fontsize=14, max_h=50)
    draw_formula_block(doc, r'H(z)=\left. H_a(s)\right|_{s=\frac{2}{T}\frac{1-z^{-1}}{1+z^{-1}}}', 'bilinear_sub', fontsize=16, max_h=40)
    doc.h3('例：H(s) 转 H(z)')
    draw_formula_block(doc, r'H(s)=\frac{2}{s^2+4s+3}=\frac{1}{s+1}-\frac{1}{s+3}', 'hs_to_hz_1', fontsize=15, max_h=42)
    draw_formula_block(doc, r'H(z)=\frac{1}{1-e^{-T}z^{-1}}-\frac{1}{1-e^{-3T}z^{-1}}', 'hs_to_hz_2', fontsize=15, max_h=42)
    comparison_table(doc)

    doc.h2('本章导图与课后题')
    doc.p('本章围绕 IIR 网络结构、模拟滤波器设计和 IIR 数字滤波器设计展开。IIR 结构包括直接 I 型、直接 II 型、级联型、并联型；模拟部分包括巴特沃斯低通与频带变换；数字化包括脉冲响应不变法和双线性变换法。')
    doc.h3('课后习题')
    doc.p('高西全第五章：1、2、3、5、11；高西全第六章：1、3、4、5、9、10、11、12。')
    draw_formula_block(doc, r'y(n)=(a+b)y(n-1)-ab\,y(n-2)+x(n-2)+(a+b)x(n-1)+abx(n)', 'homework_formula', fontsize=13, max_h=34, gap=7)

    doc.save()
    NOTE_PATH.write_text('# 第十批校对记录\n\n- 范围：原 PPT 301-332 页。\n- 已补入巴特沃斯阶数确定、低通到高通/带通/带阻频率变换、脉冲响应不变法、双线性变换法、章节导图与课后题。\n- 图形按源页关系手绘，公式统一渲染；源页水印和横板装饰不进入讲义。\n- 待最终全册回查：逐项比对 301-332 页红色重点与例题数值。\n', encoding='utf-8')
    print(PDF_PATH)


if __name__ == '__main__':
    build()

