from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(name: str) -> str:
    return (ROOT / "work" / name).read_text(encoding="utf-8-sig")


def test_geometric_frequency_response_formulas_are_print_legible():
    text = source("make_dsp_batch_115_140.py")
    assert 'geom_mag = f("geom_mag", r"|H(e^{j\\omega})|=A\\frac{\\prod_{r=1}^{N}A_r}{\\prod_{k=1}^{M}B_k}", 24)' in text
    assert 'geom_phase = f("geom_phase", r"\\theta(\\omega)=\\sum_{r=1}^{N}\\alpha_r-\\sum_{k=1}^{M}\\beta_k", 19)' in text
    assert "doc.ensure(90)" in text
    assert "draw_formula(doc, geom_mag, max_h=44, gap=5)" in text
    assert "draw_formula(doc, geom_phase, max_h=34, gap=5)" in text


def test_signal_classification_vertical_axis_stops_above_body_copy():
    text = source("make_dsp_sample_handout_v2.py")
    assert '"vertical_negative_tail": 24.0' in text
    assert "_axis_arrow(c, vx, base - geometry[\"vertical_negative_tail\"], vx, vertical_top)" in text


def test_example2_plot_has_source_proportions_and_longer_vertical_axis():
    for filename in ("make_dsp_sample_handout_v2.py", "make_dsp_batch_016_024.py"):
        text = source(filename)
        assert "doc.ensure(168)" in text
        assert "doc.y - 18," in text
        assert "300," in text
        assert "150," in text
        assert "axis_v_min=-3.2," in text
        assert "axis_v_max=6.4," in text
        assert "value_label_offsets={-1: (13, 0)}," in text
        assert "doc.y -= 168" in text
