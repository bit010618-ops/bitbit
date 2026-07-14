import ast
import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_sample_handout_v2.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("sample_handout_axis_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _function_node(name: str) -> ast.FunctionDef:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8-sig"))
    return next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == name
    )


def test_source_page_3_discrete_samples_are_preserved():
    node = _function_node("draw_signal_classification_examples")
    dictionaries = [
        ast.literal_eval(item)
        for item in ast.walk(node)
        if isinstance(item, ast.Dict)
    ]

    assert {-2: 0, -1: 0.8, 0: 0.5, 1: 1.5, 2: 0} in dictionaries


def test_source_page_3_vertical_axis_keeps_one_and_two_ticks():
    source = ast.unparse(_function_node("draw_signal_classification_examples"))

    assert "for tick_value in (1, 2)" in source
    assert "c.line(vx, tick_y, vx + 6, tick_y)" in source


def test_source_page_3_vertical_arrow_clears_highest_sample_dot():
    geometry = _load_module().signal_classification_axis_geometry()

    assert geometry["vertical_arrow_headroom"] >= 12
    assert geometry["highest_labeled_tick"] == 2
    source = ast.unparse(_function_node("draw_signal_classification_examples"))
    assert "max(max(sample_values.values()), geometry['highest_labeled_tick'])" in source


def test_source_page_14_scale_transform_base_sequence_is_not_shifted():
    node = _function_node("draw_scale_transform_triplet")
    dictionaries = []
    for item in ast.walk(node):
        if not isinstance(item, ast.Dict):
            continue
        try:
            dictionaries.append(ast.literal_eval(item))
        except ValueError:
            pass

    assert {-3: 3, -2: 2, -1: 4, 0: 2, 1: 2, 2: 3, 3: 1} in dictionaries


def test_source_page_14_only_labels_minus_one_zero_and_one():
    source = ast.unparse(_function_node("draw_scale_transform_triplet"))

    assert "x_tick_labels={-1, 0, 1}" in source
    assert "x_tick_positions={-1, 0, 1}" in source


def test_source_page_16_example_plot_uses_source_axis_geometry():
    source = ast.unparse(_function_node("draw_example2_plot"))

    assert "x_tick_labels={-1, 0, 1}" in source
    assert "x_tick_positions={-1, 0, 1}" in source
    assert "axis_v_min=-3.2" in source
    assert "axis_v_max=6.4" in source
    assert "doc.y - 18" in source
    assert "150" in source
    assert "title_position='axis_top'" in source


def test_all_shared_discrete_axes_keep_arrow_clear_of_highest_sample():
    module = _load_module()
    geometry = module.discrete_axis_geometry()

    assert geometry["minimum_vertical_arrow_clearance"] >= 12

    axis_min, axis_max = module.fit_axis_range_for_clearance(
        value_min=-4.5,
        value_max=5.2,
        sample_max=4,
        plot_span=32,
        minimum_clearance=geometry["minimum_vertical_arrow_clearance"],
    )
    sample_y = (4 - axis_min) / (axis_max - axis_min) * 32

    assert 32 - sample_y >= geometry["minimum_vertical_arrow_clearance"] - 0.01
