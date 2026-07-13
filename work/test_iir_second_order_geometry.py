from pathlib import Path
import importlib.util


MODULE_PATH = Path(__file__).with_name("make_dsp_batch_266_300_redraw.py")


def load_module():
    spec = importlib.util.spec_from_file_location("batch9_second_order", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_second_order_block_uses_source_feedback_geometry():
    geometry = load_module().second_order_source_geometry()
    assert geometry["main_sum"] == (150, 0)
    assert geometry["feedback_sum"] == (150, -60)
    assert geometry["delay_centers"] == ((220, -48), (220, -102))
    assert geometry["a1_direction"] == "left"
    assert geometry["a2_direction"] == "up"
    assert geometry["a1_path"] == ((220, -60), (198, -60), (172, -60))
    assert geometry["a2_path"] == ((220, -112), (150, -112), (150, -70))


def test_second_order_signal_flow_keeps_two_leftward_feedback_branches():
    geometry = load_module().second_order_source_geometry()
    assert geometry["flow_feedback_rows"] == (-40, -82)
    assert geometry["flow_branch_direction"] == "right-to-left"


def test_a1_gain_has_clear_space_before_feedback_summer():
    geometry = load_module().second_order_source_geometry()
    assert geometry["a1_triangle_tip_x"] - geometry["feedback_sum_right_x"] >= 12
