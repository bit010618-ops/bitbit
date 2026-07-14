import ast
import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_batch_185_227.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("batch7_axis_test", SCRIPT)
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


def test_source_page_219_restores_omega_and_pi_labels():
    source = _function_source("build")

    assert "x_tick_labels={-1: '-\\\\omega_0', 1: '\\\\omega_0'}" in source
    assert "sample_value_labels={-1: '\\\\pi', 1: '\\\\pi'}" in source
    assert "title_position='axis_top'" in source


def test_stem_plot_supports_rendered_source_labels():
    source = _function_source("draw_stem_plot")

    assert "x_tick_labels=None" in source
    assert "sample_value_labels=None" in source
    assert "title_position='below'" in source
    assert "b185_x_tick" in source
    assert "b185_sample_value" in source


def test_all_batch7_stem_axes_keep_arrow_clear_of_highest_dot():
    geometry = _load_module().stem_plot_axis_geometry()

    assert geometry["vertical_arrow_headroom"] >= 12
