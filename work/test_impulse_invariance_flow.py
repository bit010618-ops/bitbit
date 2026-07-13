from pathlib import Path


SOURCE = Path(__file__).with_name("make_dsp_batch_301_332_redraw.py").read_text(encoding="utf-8")


def test_source_page_319_impulse_invariance_flow_is_drawn_and_used():
    assert "def draw_impulse_invariance_flow" in SOURCE
    assert "draw_impulse_invariance_flow(doc)" in SOURCE
    for label in (
        "模拟滤波器\\n传递函数 H(s)",
        "拉氏反变换",
        "模拟滤波器\\n单位脉冲响应 h(t)",
        "时域采样\\nt=nT",
        "数字滤波器\\n单位脉冲响应 h(n)",
        "z 变换",
        "数字滤波器\\n系统函数 H(z)",
        "时域离散",
        "频域周期",
    ):
        assert label in SOURCE


def test_iir_method_intro_uses_prose_instead_of_raw_subscript_markup():
    assert "由模拟系统函数得到数字系统函数" in SOURCE
    assert "设计模拟低通滤波器" in SOURCE
    assert "转换为数字系统函数" in SOURCE
    assert "从而保持时域响应。" in SOURCE
