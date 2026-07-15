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


def test_direct_i_general_keeps_arrows_frames_and_side_text_separate():
    module = load_module()
    geometry = module.direct_i_general_geometry()

    assert geometry['feedback_arrow_end'] - geometry['feedback_frame_left'] >= 12
    assert geometry['feedforward_frame_right'] - geometry['accumulator_x'] >= 10
    assert geometry['right_text_x'] - geometry['feedback_frame_right'] >= 12
    assert geometry['main_line_end'] < geometry['right_text_x']


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


def test_two_numeric_examples_from_source_page_281_are_fully_preserved():
    module = load_module()
    examples = module.direct_form_numeric_examples_source_topology()

    assert examples == (
        {
            'name': 'H_1',
            'direct_i': {
                'input_gain': '3',
                'output_gain': '0.8',
                'feedforward': ('2', '2', '6'),
                'feedback': ('-4', '-3', '-2'),
                'feedforward_delays': 3,
                'feedback_delays': 3,
            },
            'direct_ii': {
                'input_gain': '0.8',
                'output_gain': '3',
                'left_coefficients': ('-4', '-3', '-2'),
                'right_coefficients': ('2', '2', '6'),
                'shared_delays': 3,
            },
        },
        {
            'name': 'H_2',
            'direct_i': {
                'input_gain': '-5',
                'output_gain': '',
                'feedforward': ('2', '-0.5'),
                'feedback': ('-3', '-3', '-1'),
                'feedforward_delays': 2,
                'feedback_delays': 3,
            },
            'direct_ii': {
                'input_gain': '-5',
                'output_gain': '',
                'left_coefficients': ('-3', '-3', '-1'),
                'right_coefficients': ('2', '-0.5'),
                'shared_delays': 3,
            },
        },
    )


def test_source_page_281_four_networks_are_drawn_after_their_formulas():
    source = MODULE.read_text(encoding='utf-8-sig')
    formula_index = source.index("'direct2_hw'")
    draw_index = source.index('draw_direct_form_numeric_examples(doc)', formula_index)
    cascade_index = source.index("doc.h2('5.2.4 级联型 IIR 数字滤波器')", draw_index)

    assert formula_index < draw_index < cascade_index


def test_second_source_example_keeps_the_negative_five_numerator():
    source = MODULE.read_text(encoding='utf-8-sig')
    assert r'H_2(z)=\frac{-5+2z^{-1}-0.5z^{-2}}' in source


def test_numeric_network_delay_labels_only_mark_actual_delay_chains():
    policy = load_module().direct_form_numeric_delay_label_policy()

    assert policy == {
        'direct_i': ('feedforward_down', 'feedback_down'),
        'direct_ii': ('shared_down',),
    }


def test_h2_direct_ii_right_return_stops_after_its_two_coefficients():
    module = load_module()
    example = module.direct_form_numeric_examples_source_topology()[1]['direct_ii']
    geometry = module.direct_form_numeric_branch_geometry(example)

    assert len(example['right_coefficients']) == 2
    assert example['shared_delays'] == 3
    assert geometry['right_return_stages'] == 2
    assert geometry['right_return_stages'] < geometry['shared_delay_stages']


def test_numeric_panels_do_not_add_titles_missing_from_the_source_slide():
    geometry = load_module().direct_form_numeric_layout_geometry()

    assert geometry['draw_panel_titles'] is False


def test_direct_i_overview_keeps_output_frame_and_explanation_separate():
    geometry = load_module().direct_i_general_geometry()

    assert geometry['feedforward_frame_right'] < geometry['feedback_frame_left']
    assert geometry['feedback_frame_right'] + 20 <= geometry['main_line_end']
    assert geometry['feedback_frame_right'] + 8 <= geometry['output_label_x']
    assert geometry['output_label_x'] + 28 <= geometry['right_text_x']
    assert -110 + geometry['feedforward_frame_height'] - 45 >= 30
    assert -125 + geometry['feedback_frame_height'] - 45 >= 30


def test_direct_i_feedback_coefficients_join_an_upward_accumulator_rail():
    module = load_module()
    geometry = module.direct_i_general_geometry()
    policy = module.direct_i_general_connection_policy()

    assert geometry['feedback_accumulator_x'] < geometry['feedback_rail_x']
    assert policy['feedback'] == (
        'delay_down',
        'coefficient_left',
        'accumulator_up',
    )
    assert policy['callout'] == ('right_text_to_feedback_frame', 'left')


def test_direct_i_overview_preserves_source_omission_segments_and_terminals():
    module = load_module()
    policy = module.direct_i_general_connection_policy()
    geometry = module.direct_i_general_geometry()

    assert policy['main_line'] == ('terminal_dots', 'interior_arrows')
    assert policy['junctions'] == 'no_internal_dots'
    assert policy['feedforward_omission'] == (
        'delay_chain_dashed',
        'accumulator_dashed',
    )
    assert policy['feedback_omission'] == (
        'delay_chain_dashed',
        'accumulator_dashed',
    )
    assert geometry['feedforward_omission_after_index'] == 2
    assert geometry['feedback_omission_after_index'] == 1
    assert (
        geometry['feedforward_frame_bottom'] - geometry['feedforward_label_y_offset']
        >= 12
    )
    assert (
        geometry['feedback_frame_bottom'] - geometry['feedback_label_y_offset']
        >= 12
    )
    assert geometry['block_height'] >= -geometry['feedback_label_y_offset'] + 30
