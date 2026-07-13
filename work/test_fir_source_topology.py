import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name('make_dsp_batch_333_366_redraw.py')
spec = importlib.util.spec_from_file_location('fir_redraw', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_fir_source_topology_preserves_folded_and_sampling_networks():
    topology = module.fir_source_topology()

    odd = topology['linear_phase']['odd_n']
    even = topology['linear_phase']['even_n']
    assert odd['rails'] == ('forward_delay_chain', 'reverse_delay_chain', 'output_bus')
    assert even['rails'] == ('forward_delay_chain', 'reverse_delay_chain', 'output_bus')
    assert odd['paired_fold_branches'] is True
    assert even['paired_fold_branches'] is True
    assert odd['center_tap'] is True
    assert even['terminal_delay'] is True

    sampling = topology['frequency_sampling']
    assert sampling['comb'] == '1-z^-N'
    assert sampling['branches'] == ('H(0)', 'H(1)', '...', 'H(N-1)')
    assert sampling['branch_elements'] == ('W_N^-k', 'z^-1')
    assert sampling['output_gain'] == '1/N'
