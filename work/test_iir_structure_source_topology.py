import importlib.util
from pathlib import Path


MODULE = Path(__file__).with_name('make_dsp_batch_266_300_redraw.py')


def load_module():
    spec = importlib.util.spec_from_file_location('iir_redraw', MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_direct_i_and_direct_ii_follow_the_source_network_topology():
    spec = load_module().direct_structure_source_topology()

    assert spec['direct_i'] == {
        'feedforward_delay_side': 'left',
        'feedback_delay_side': 'right',
        'feedforward_coefficients': ('b_0', 'b_1', 'b_2', 'b_M'),
        'feedback_coefficients': ('a_1', 'a_2', 'a_{N-1}', 'a_N'),
        'feedforward_direction': 'right',
        'feedback_direction': 'left',
        'feedback_delay_direction': 'down',
    }
    assert spec['direct_ii'] == {
        'shared_delay_chain': 'center',
        'feedforward_direction': 'right',
        'feedback_direction': 'left',
        'coefficient_pairs': (('-4', '5/4'), ('11', '-3/4'), ('-2', '1/8')),
    }
    assert spec['direct_ii_general'] == {
        'upper_layout': ('direct_i_left', 'merged_direct_ii_right'),
        'lower_layout': 'compact_merged_delay_chain',
        'coefficients': ('a_1', 'a_2', 'b_0', 'b_1', 'b_2'),
    }
