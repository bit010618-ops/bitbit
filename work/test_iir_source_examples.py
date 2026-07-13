from pathlib import Path


SOURCE = Path(__file__).with_name("make_dsp_batch_301_332_redraw.py").read_text(encoding="utf-8")


def test_source_pages_314_315_bandpass_example_is_retained():
    assert "def analog_bandpass_example" in SOURCE
    assert r"\eta_{s1}=4.15" in SOURCE
    assert r"\eta_{s2}=6" in SOURCE
    assert r"\lambda_{sp1}=1.833" in SOURCE
    assert r"\lambda_{sp2}=-1.874" in SOURCE
    assert r"N=3" in SOURCE


def test_iir_generator_is_valid_python():
    compile(SOURCE.lstrip("\ufeff"), "make_dsp_batch_301_332_redraw.py", "exec")
