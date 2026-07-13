import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name('make_dsp_sample_handout_v2.py')
spec = importlib.util.spec_from_file_location('sample_handout', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_origin_tick_is_offset_from_both_axes():
    geometry = module.discrete_axis_label_geometry()
    origin = geometry['origin_tick']
    assert 4 <= origin['x_offset'] <= 7
    assert origin['anchor'] == 'left'
    assert origin['y_offset'] <= -14
    assert geometry['regular_tick']['y_offset'] <= -13
    assert geometry['positive_zero_sample_value']['x_offset'] <= -6
