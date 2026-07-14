import importlib.util
import ast
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


def test_direct_ii_general_uses_a_full_page_readable_source_layout():
    module = load_module()
    geometry = module.direct_ii_general_geometry()

    assert geometry['canvas_height'] >= 460
    assert geometry['panel_width'] >= 165
    assert geometry['row_gap'] >= 45
    assert geometry['source_side_labels'] == (
        'x(n-1)', 'x(n-2)', 'y(n-1)', 'y(n-2)', 'w_1', 'w_2'
    )
    assert (
        geometry['right_panel_offset']
        + geometry['panel_width']
        + geometry['arrow_overhang']
        + geometry['output_label_width']
        <= module.CONTENT_W
    )


def test_numeric_direct_i_and_ii_have_one_arrow_per_vertical_stage():
    arrows = load_module().direct_iir_example_arrow_geometry()

    assert arrows['direct_i'] == {
        'feedforward_delay_down': 3,
        'feedback_delay_down': 3,
        'accumulator_up': 3,
    }
    assert arrows['direct_ii'] == {
        'shared_delay_down': 3,
        'feedback_return_up': 3,
        'feedforward_return_up': 3,
    }


def test_direct_ii_section_starts_on_a_fresh_page():
    tree = ast.parse(MODULE.read_text(encoding='utf-8-sig'))
    build = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == 'build'
    )
    source = ast.unparse(build)
    marker = "doc.h2('5.2.3 直接 II 型 IIR 滤波器')"
    marker_index = source.index(marker)
    assert "doc.new_page()" in source[max(0, marker_index - 80):marker_index]
