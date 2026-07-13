from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_batch_333_366_redraw.py").read_text(encoding="utf-8")


def test_source_example_structures_are_drawn():
    assert "def fir_direct_example" in SCRIPT
    assert "def fir_cascade_example" in SCRIPT
    assert "fir_direct_example(doc)" in SCRIPT
    assert "fir_cascade_example(doc)" in SCRIPT


def test_comb_response_and_four_linear_phase_cases_are_drawn():
    assert "def comb_response_figure" in SCRIPT
    assert "def linear_phase_four_cases" in SCRIPT
    assert "comb_response_figure(doc)" in SCRIPT
    assert "linear_phase_four_cases(doc)" in SCRIPT


def test_linear_phase_explanatory_figures_are_drawn():
    assert "def amplitude_phase_explainer" in SCRIPT
    assert "amplitude_phase_explainer(doc)" in SCRIPT
