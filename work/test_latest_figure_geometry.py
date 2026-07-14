import importlib.util
from pathlib import Path


ROOT = Path(__file__).parent


def load(name):
    path = ROOT / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_comb_response_zeros_touch_horizontal_axis():
    module = load('make_dsp_batch_333_366_redraw.py')
    geometry = module.comb_response_geometry()
    assert geometry['curve_baseline_offset'] == 0
    assert geometry['zero_y'] == geometry['axis_y']
    points = module.comb_response_points(width=205, height=68, lobes=8)
    for index in range(9):
        expected_x = 205 * index / 8
        matching = [y for x, y in points if abs(x - expected_x) < 1e-9]
        assert matching == [0]


def test_feedback_arrows_land_once_on_distinct_summer_points():
    module = load('make_dsp_batch_016_024.py')
    geometry = module.system_block_arrow_geometry()
    for key in ('example9', 'example10'):
        item = geometry[key]
        assert item['arrow_count_at_diagonal_entry'] == 1
        assert item['endpoint_on_circumference'] is True
        assert item['diagonal_endpoint'] != item['bottom_endpoint']


def test_tdm_rate_labels_are_centered_in_every_block():
    module = load('make_dsp_batch_400_436_redraw.py')
    geometry = module.tdm_rate_block_geometry()
    assert geometry['input_label_center_x'] == geometry['input_block_center_x']
    assert geometry['output_label_center_x'] == geometry['output_block_center_x']
    assert geometry['label_center_y'] == geometry['block_center_y']
