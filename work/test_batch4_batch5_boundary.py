from pathlib import Path


B4 = Path(__file__).with_name("make_dsp_batch_089_112.py").read_text(encoding="utf-8")
B5 = Path(__file__).with_name("make_dsp_batch_115_140.py").read_text(encoding="utf-8")


def test_sinusoidal_steady_state_fills_batch4_tail():
    assert "2.4.4 系统的频率响应：正弦稳态" in B4
    assert "sinusoidal steady-state section is carried by the previous batch tail page" in B5


def test_batch5_starts_with_source_example_four():
    start = B5.index("doc.header()")
    first_heading = B5.index("doc.h2", start)
    assert 'doc.h2("例 4  理想低通频率响应")' in B5[first_heading:first_heading+80]
