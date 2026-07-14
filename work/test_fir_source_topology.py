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


def test_linear_phase_fir_filter_types_match_source_pages_365_366():
    rows = module.linear_phase_fir_source_table()

    assert rows['type_i']['filters'] == ('LP', 'HP', 'BP', 'BS')
    assert rows['type_ii']['filters'] == ('LP', 'BP')
    assert rows['type_iii']['filters'] == ('BP',)
    assert rows['type_iv']['filters'] == ('HP', 'BP')
    assert rows['type_ii']['forced_zeros'] == ('pi',)
    assert rows['type_iii']['forced_zeros'] == ('0', 'pi')
    assert rows['type_iv']['forced_zeros'] == ('0',)
    assert rows['type_i']['coefficient_domain'] == 'other_n'
    assert rows['type_ii']['plot_annotation'] == 'H(pi)=0'
    assert rows['type_iii']['plot_annotation'] == 'H(0)=H(pi)=0'
    assert rows['type_iv']['plot_annotation'] == 'H(0)=0'


def test_source_pages_365_366_are_preserved_as_two_complete_pages():
    contract = module.linear_phase_critical_pages_contract()

    assert contract['page_count'] == 2
    assert contract['shared_blocks'] == (
        'importance_banner',
        'symmetry_definition',
        'phase_equation',
        'phase_plot',
        'odd_n_checklist',
        'odd_n_impulse_plot',
        'odd_n_amplitude_plot',
        'odd_n_coefficient_formula',
        'odd_n_symmetry_conclusion',
        'even_n_checklist',
        'even_n_impulse_plot',
        'even_n_amplitude_plot',
        'even_n_coefficient_formula',
        'even_n_symmetry_conclusion',
    )
    assert contract['pages'] == ('type_i_and_ii', 'type_iii_and_iv')
