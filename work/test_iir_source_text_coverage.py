from pathlib import Path


SOURCE = Path(__file__).with_name("make_dsp_batch_266_300_redraw.py")


def test_iir_characteristics_from_source_page_273_are_preserved():
    text = SOURCE.read_text(encoding="utf-8")
    assert "5.2.1 IIR 滤波器特点" in text
    for phrase in ("单位脉冲响应 h(n) 为无限长", "结构上存在输出到输入的反馈", "全部极点必须位于单位圆内"):
        assert phrase in text


def test_direct_i_and_ii_characteristics_from_source_page_277_are_preserved():
    text = SOURCE.read_text(encoding="utf-8")
    for phrase in ("M+N 个延时单元", "极点对系数变化过于灵敏", "只需 N 个延时单元", "称为典范型"):
        assert phrase in text


def test_cascade_parallel_comparison_from_source_page_288_is_preserved():
    text = SOURCE.read_text(encoding="utf-8")
    for phrase in ("单独控制一对零点或一对极点", "不能像级联型那样直接控制零点", "运算误差互不影响", "各子系统可以并行实现"):
        assert phrase in text
