import importlib.util
from pathlib import Path


MODULE = Path(__file__).with_name('make_dsp_batch_016_024.py')


def load_module():
    spec = importlib.util.spec_from_file_location('system_blocks', MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_example_9_and_10_preserve_source_branch_geometry():
    spec = load_module().system_block_source_geometry()

    assert spec['example9']['delay_orientation'] == 'vertical_stack'
    assert spec['example9']['gain_2_return'] == ('inter_delay_node', 'horizontal_left', 'diagonal_to_summer_right')
    assert spec['example9']['gain_2_arrow_endpoint'] == 'summer_lower_right_circumference'
    assert spec['example9']['gain_minus_1_return'] == ('second_delay_output', 'horizontal_left', 'vertical_to_summer_bottom')
    assert spec['example10']['delay_orientation'] == 'horizontal_chain'
    assert spec['example10']['output_minus_2_return'] == ('first_delay_output', 'vertical_up', 'summer_bottom')
    assert spec['example10']['input_minus_2_return'] == ('first_delay_output', 'extend_right', 'vertical_down', 'horizontal_left', 'diagonal_to_input_summer')
    assert spec['example10']['feedback_tap'] == 'post_delay_right_extension'
    assert spec['example10']['gain_3_return'] == ('second_delay_output', 'vertical_down', 'horizontal_left', 'summer_bottom')
