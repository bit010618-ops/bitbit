import importlib.util
from pathlib import Path


MODULE = Path(__file__).with_name('make_dsp_batch_266_300_redraw.py')


def load_module():
    spec = importlib.util.spec_from_file_location('iir_redraw', MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cascade_and_parallel_examples_keep_source_networks():
    spec = load_module().cascade_parallel_source_topology()

    assert spec['cascade'] == {
        'sections': ('first_order', 'second_order'),
        'main_path': 'horizontal',
        'section_main_gains': ('2', '4'),
        'first_order_pairs': (('0.25', '-0.379'),),
        'second_order_pairs': (('1', '-1.24'), ('-0.5', '5.264')),
        'delay_count': (1, 2),
        'main_line_policy': ('terminal_dots', 'interior_arrows'),
        'section_junctions': 'source_nodes',
    }
    assert spec['parallel'] == {
        'direct_path_coefficients': ('G_0', 'G_1', 'G_{M-N}'),
        'second_order_sections': ('beta_01', 'beta_11', 'alpha_11', 'alpha_21'),
        'branches': 'vertical_input_output_buses',
        'delay_count': (1, 2),
    }
    assert spec['example'] == {
        'cascade_sections': (('1/4', '1/3'), ('1/2',)),
        'parallel_branches': (('10/3', '1/2'), ('-7/3', '1/4')),
        'layouts': ('cascade_left', 'parallel_right'),
    }


def test_ratio_tex_renders_fraction_coefficients():
    module = load_module()
    assert module.ratio_tex('1/4') == r'\frac{1}{4}'
    assert module.ratio_tex('-7/3') == r'-\frac{7}{3}'


def test_parallel_annotation_clears_last_branch():
    layout = load_module().parallel_iir_layout_geometry()
    assert layout['annotation_gap_below_network'] >= 16
