import ast
from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_batch_115_140.py")


def _function_source(name: str) -> str:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8-sig"))
    node = next(
        item
        for item in tree.body
        if isinstance(item, ast.FunctionDef) and item.name == name
    )
    return ast.unparse(node)


def _build_source() -> str:
    return _function_source("build_pdf")


def test_source_page_124_comb_response_zeros_touch_horizontal_axis():
    source = _function_source("draw_comb_diagrams")

    assert "yy = by + 58 * val" in source
    assert "yy = by + 8 + 58 * val" not in source


def test_source_pages_131_132_use_open_circle_for_zero_and_cross_for_pole():
    source = _function_source("draw_unit_and_response")

    assert "c.circle(px, py, 4, stroke=1, fill=0)" in source
    assert "c.line(cx - 4, cy - 4, cx + 4, cy + 4)" in source


def test_notch_unit_circle_keeps_one_outside_and_moves_negative_omega_down():
    source = _function_source("draw_unit_circle")

    assert "c.drawCentredString(cx + r + 3, cy - 12, '1')" in source
    assert "c.drawCentredString(cx + r + 7, cy - 12, '1')" not in source
    assert "label_y = py - 10 if label == '-ω0' else py + 4" in source
    assert "draw_auto_math_text(" in source
    assert "c, px + 5, label_y, label" in source


def test_source_pages_131_132_keep_frequency_guides_and_hz_labels():
    source = _function_source("draw_unit_and_response")

    assert "mid_x = x1 + 100" in source
    assert "x1 + 105" not in source
    assert "c.setDash(2, 2)" in source
    assert "b5_half_sampling_frequency" in source
    assert "b5_sampling_frequency" in source
    assert "'\\\\frac{f_s}{2}', 16" in source
    assert "'f_s', 16" in source
    assert "20 / label_image.height" in source
    assert "x1 + 224" in source
    assert "c.drawCentredString(mid_x, by - 24, 'f_s/2')" not in source
    assert "c.drawCentredString(x1 + 200, by - 24, 'f_s')" not in source
    assert "yy = by + 60 * val" in source
    assert "b5_response_axis_title" in source


def test_source_pages_131_132_keep_each_filter_caption_with_its_figure():
    source = _build_source()

    assert source.count("doc.ensure(180)") >= 2


def test_source_page_133_keeps_allpass_formulas_full_width():
    source = _build_source()

    assert "draw_formula(doc, ap_def, max_h=31)" in source
    assert "draw_formula(doc, ap_general_main, max_h=72)" in source
    assert "draw_formula(doc, ap_general_conditions, max_h=20)" in source
    assert "draw_formula(doc, ap_fact, max_h=40)" in source
    assert "draw_formula(doc, ap_mag, max_h=34)" in source
    assert "draw_formula_rows(doc, [ap_fact, ap_mag]" not in source


def test_source_page_135_enlarges_the_general_allpass_formula_without_extra_emphasis():
    source = _build_source()

    assert "ap_general_main = f('ap_general_main'" in source
    assert "26, '#D71920')" not in source
    assert "全通滤波器的系统函数的一般形式为：" in source
    assert "doc.p('全通滤波器的系统函数的一般形式为：')" in source
