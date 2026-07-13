import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name('make_dsp_batch_266_300_redraw.py')
spec = importlib.util.spec_from_file_location('iir_redraw', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_filter_design_source_topology_matches_ppt():
    topology = module.filter_design_source_topology()

    assert topology['bridge']['rows'] == ('continuous', 'discrete')
    assert topology['bridge']['continuous_transforms'] == ('LT', 'LT', 'LT')
    assert topology['bridge']['discrete_transforms'] == ('ZT', 'ZT', 'ZT')
    assert topology['bridge']['time_operation'] == 'convolution'
    assert topology['bridge']['frequency_operation'] == 'multiplication'

    digital = topology['digital_ideal_responses']
    assert digital['types'] == ('lowpass', 'highpass', 'bandpass', 'bandstop')
    assert digital['period'] == '2pi'
    assert digital['repeat_range'] == (-3, 3)
