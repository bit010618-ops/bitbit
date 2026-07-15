import ast
from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_batch_046_088.py")


def _function_source(name: str) -> str:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8-sig"))
    node = next(
        item
        for item in tree.body
        if isinstance(item, ast.FunctionDef) and item.name == name
    )
    return ast.unparse(node)


def test_source_page_87_uses_blue_axes_and_red_samples():
    source = _function_source("draw_dtft_conj_example_plots")

    assert "SOURCE_AXIS_BLUE" in source
    assert "SOURCE_SAMPLE_RED" in source


def test_source_page_87_keeps_vertical_panel_order():
    source = _function_source("draw_dtft_conj_example_plots")

    assert "top_y = y - index * panel_gap" in source
    assert "doc.y -= panel_gap * 3" in source


def test_source_page_87_odd_component_keeps_origin_sample():
    source = _function_source("draw_dtft_conj_example_plots")

    assert "{-1: -0.5, 0: 0, 1: 0.5}" in source


def test_source_page_87_negative_half_sign_stays_with_fraction():
    source = _function_source("draw_dtft_conj_example_plots")

    assert r"-\\frac{1}{2}" in source
    assert "negative_half_label" in source
    assert "c.drawString(px - 7, py - 3, '-')" not in source


def test_source_page_87_unit_value_sits_clear_of_vertical_stem():
    source = _function_source("draw_dtft_conj_example_plots")

    assert "c.drawString(px + 10, py + 2, '1')" in source
