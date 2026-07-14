from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_batch_367_399_redraw.py")


def test_ideal_filter_explanations_use_latex_subscripts():
    source = SCRIPT.read_text(encoding="utf-8")
    assert "def red_filter_relation" in source
    assert "red_filter_relation(doc, '带通滤波器', '低通滤波器', '-', '低通滤波器', 'source377_relation')" in source
    assert "red_filter_relation(doc, '带阻滤波器', '高通滤波器', '+', '低通滤波器', 'source378_relation')" in source
    assert "r'\\omega_2'" in source
    assert "r'\\omega_1'" in source
