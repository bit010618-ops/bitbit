import ast
import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_batch_016_024.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("batch2_axis_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _function_source(name: str) -> str:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8-sig"))
    node = next(
        item
        for item in tree.body
        if isinstance(item, ast.FunctionDef) and item.name == name
    )
    return ast.unparse(node)


def test_source_page_25_small_axes_do_not_add_generic_ticks_or_value_labels():
    source = _function_source("draw_small_axis")

    assert "draw_discrete_axes_plot" not in source
    assert "for idx, value in enumerate(values)" in source


def test_source_page_25_right_plot_has_one_single_amplitude_label():
    source = _function_source("draw_small_axis")

    assert "c.drawString(x0 + 8, sample_top - 3, label_right)" in source


def test_source_page_25_right_sequence_extends_left_of_vertical_axis():
    source = _function_source("draw_ex4_plots")

    assert "direction=-1" in source


def test_source_page_25_small_axes_keep_arrow_clear_of_highest_dot():
    geometry = _load_module().small_axis_geometry()

    assert geometry["vertical_arrow_headroom"] >= 12
