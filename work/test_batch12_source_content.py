from pathlib import Path

from pypdf import PdfReader


SCRIPT = Path(__file__).with_name("make_dsp_batch_367_399_redraw.py").read_text(encoding="utf-8")
PDF = Path(__file__).parents[1] / "outputs" / "DSP讲义重制_第十二批_原PPT367-399页_FIR滤波器设计_手绘复刻版.pdf"


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


def test_batch12_is_expanded_handout_not_five_page_summary():
    assert PDF.exists()
    assert len(PdfReader(str(PDF)).pages) >= 10


def test_source_367_399_groups_have_dedicated_renderers():
    required = (
        "draw_source_367_374",
        "draw_source_375_379",
        "draw_source_380_384",
        "draw_source_385_389",
        "draw_source_390_397",
        "draw_source_398_399",
    )
    for name in required:
        assert f"def {name}" in SCRIPT
        assert f"{name}(doc)" in SCRIPT


def test_all_five_source_window_definitions_are_present():
    for token in (
        "矩形窗",
        "三角窗",
        "汉宁窗(升余弦窗)",
        "海明窗(改进的升余弦窗)",
        "布莱克曼窗",
    ):
        assert token in SCRIPT
    for formula_token in (
        "w(n)=R_N(n)",
        "1-cos",
        "0.54-0.46cos",
        "0.42-0.5cos",
    ):
        assert formula_token in SCRIPT


def test_frequency_sampling_source_constraints_and_steps_are_preserved():
    for token in (
        "一类线性相位",
        "二类线性相位",
        "N为奇数",
        "N为偶数",
        "设计过程",
        "频率响应采样后的幅频图像",
        "写出H(k)的表达式",
    ):
        assert token in SCRIPT


def test_source_chapter_map_is_redrawn_not_replaced_by_three_bullets():
    assert "def fir_chapter_map" in SCRIPT
    assert "fir_chapter_map(doc)" in SCRIPT
