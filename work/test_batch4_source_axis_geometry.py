import ast
import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_batch_089_112.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("batch4_axis_test", SCRIPT)
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


def test_source_page_98_impulse_spectra_keep_vertical_axis():
    source = _function_source("draw_impulse_spectrum")

    assert "axis_top = y + geometry['axis_height']" in source
    assert "b4_impulse_axis_title" in source


def test_source_page_98_arrow_clears_impulse_dot():
    geometry = _load_module().impulse_spectrum_axis_geometry()

    assert geometry["axis_height"] - geometry["sample_height"] >= 12
