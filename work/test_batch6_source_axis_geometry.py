import ast
from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_batch_141_184.py")


def _function_source(name: str) -> str:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8-sig"))
    node = next(
        item
        for item in tree.body
        if isinstance(item, ast.FunctionDef) and item.name == name
    )
    return ast.unparse(node)


def test_source_page_145_uses_the_seven_original_signal_shapes():
    source = _function_source("draw_time_frequency_cases")

    for helper in (
        "draw_periodic_triangle_wave",
        "draw_continuous_triangle",
        "draw_one_sided_stem_sequence",
        "draw_periodic_sampled_triangle",
        "draw_sampled_sinc",
        "draw_sinc_curve",
        "draw_periodic_sinc_replicas",
    ):
        assert helper in source

    assert "amp = max(3, 26 - abs(j) * 7)" not in source
    assert "amp = max(2, 28 - abs(j) * 5)" not in source


def test_source_page_145_restores_original_period_and_sampling_labels():
    source = _function_source("draw_time_frequency_cases")

    for label in ("T_1", "\\frac{1}{T_1}", "T_s", "f_s"):
        assert label in source


def test_source_page_145_renders_axis_titles_as_math():
    source = _function_source("draw_time_frequency_cases")

    for expression in (
        "x(t)",
        "x(nT_s)",
        "|X(k/T_1)|",
        "|X(f)|",
        "|X(e^{j\\\\omega})|",
    ):
        assert expression in source

    assert "c.drawString(origin_x + 3, py + ph - 2, y_label)" not in source


def test_source_page_148_uses_periodic_extensions_of_the_same_sequence():
    source = _function_source("draw_dfs_relation_map")

    for helper in (
        "draw_one_period_sequence",
        "draw_periodic_extension_sequence",
        "draw_periodic_frequency_curve",
        "draw_periodic_frequency_samples",
    ):
        assert helper in source

    assert "math.sin(j * math.pi / 7)" not in source
    assert "math.cos((step - 80) * math.pi / 48)" not in source


def test_source_page_148_restores_source_interval_labels():
    source = _function_source("draw_dfs_relation_map")

    for label in ("N-1", "N", "T_0", "T_s", "2\\\\pi f_s"):
        assert label in source


def test_source_page_148_keeps_sampling_note_outside_the_spectrum():
    source = _function_source("draw_dfs_relation_map")

    assert "right_x + 166" in source
    assert "right_x + 108" not in source
    assert source.count("baseline - 20, 'N'") >= 2


def test_source_page_148_enlarges_and_emphasizes_the_relation_map():
    source = _function_source("draw_dfs_relation_map")

    assert "h = 205" in source
    assert "c.setFont('CNB', 9.4)" in source
    assert "note_w = 84" in source
    assert "b6_p148_sampling_relation" in source
    assert "13, color='#D71920'" in source
