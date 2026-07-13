from pathlib import Path


SOURCE = Path(__file__).with_name("make_dsp_batch_115_140.py")


def test_ideal_lowpass_example_keeps_all_four_source_inputs():
    text = SOURCE.read_text(encoding="utf-8")
    expected = (
        r"x(n)=\delta(n)+\delta(n-1)",
        r"x(n)=\cos(0.6\pi n)",
        r"x(n)=1+\cos(0.4\pi n)+\delta(n)",
        r"x(n)=5\sin(0.7\pi n)+10e^{j0.2\pi n}",
    )
    for formula in expected:
        assert formula in text


def test_ideal_lowpass_example_keeps_source_solution_steps():
    text = SOURCE.read_text(encoding="utf-8")
    assert r"h(n)=\frac{\sin(0.5\pi n)}{\pi n}" in text
    assert r"y(n)=h(n)+h(n-1)" in text
    assert r"|H(e^{j0.6\pi})|\cos(0.6\pi n)=0" in text
    assert r"5\frac{\sin(0.5\pi n)}{\pi n}+10e^{j0.2\pi n}" in text


def test_impulse_invariance_keeps_reverse_substitution_statement():
    text = SOURCE.read_text(encoding="utf-8")
    assert r"H(s)=H(z)|_{z=e^{sT}}" in text


def test_geometry_section_flows_after_lowpass_example_without_forced_blank_page():
    text = SOURCE.read_text(encoding="utf-8")
    marker = 'note_box(doc, "814 考点提示"'
    start = text.index(marker)
    end = text.index('doc.h2("几何法求频率响应")', start)
    assert "doc.new_page()" not in text[start:end]


def test_second_chapter_homework_from_source_page_141_is_kept_at_chapter_end():
    text = SOURCE.read_text(encoding="utf-8")
    for item in ("8-17", "8-21（2）（4）", "8-37", "2-12", "2-28"):
        assert item in text
    assert 'doc.h2("第二章课后习题")' in text
    assert text.index('doc.h2("本章下半部分导图")') < text.index('doc.h2("第二章课后习题")')
    assert "draw_homework_columns(doc," in text
