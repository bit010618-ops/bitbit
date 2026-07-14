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


def test_butterworth_indicator_plot_uses_source_axis_coordinates():
    geometry = module.butterworth_indicator_source_geometry()

    assert geometry['x_range'] == (0.0, 3.0)
    assert geometry['x_ticks'] == (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
    assert geometry['y_ticks'] == (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
    assert geometry['cutoffs'] == {
        'passband': 0.8,
        'three_db': 0.95,
        'stopband': 1.5,
    }
    assert geometry['levels'] == {
        'passband': 0.891,
        'three_db': 0.707,
        'stopband': 0.01,
    }
    assert geometry['cutoff_colors'] == {
        'passband': '#E60012',
        'three_db': '#0000FF',
        'stopband': '#7B3F98',
    }
