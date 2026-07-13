from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_batch_367_399_redraw.py").read_text(encoding="utf-8")


def test_source_classification_example_is_preserved():
    assert "def linear_phase_classification_example" in SCRIPT
    assert "linear_phase_classification_example(doc)" in SCRIPT


def test_all_four_ideal_impulse_responses_are_preserved():
    assert "def ideal_impulse_responses" in SCRIPT
    assert "ideal_impulse_responses(doc)" in SCRIPT
    for token in ("低通", "高通", "带通", "带阻"):
        assert token in SCRIPT


def test_source_homework_numbers_are_preserved():
    for token in ("13-14", "15", "17", "18"):
        assert token in SCRIPT
