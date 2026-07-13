from pathlib import Path


SOURCE = Path(__file__).with_name("make_dsp_batch_333_366_redraw.py").read_text(encoding="utf-8")


def test_source_pages_356_357_linear_phase_reduction_example_is_preserved():
    assert "def linear_phase_reduction_example" in SOURCE
    assert "linear_phase_reduction_example(doc)" in SOURCE
    assert r"\frac{1}{10}(1+0.9z^{-1}+2.1z^{-2}+0.9z^{-3}+z^{-4})" in SOURCE
    assert "直接型结构" in SOURCE
    assert "线性相位结构" in SOURCE
    assert r"h(n)=\{1,0.9,2.1,0.9,1\}" in SOURCE
    assert "linear_direct_input_arrow" in SOURCE
    assert "linear_sym_input_arrow" in SOURCE
