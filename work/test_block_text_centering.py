from make_dsp_batch_266_300_redraw import centered_text_baselines
from make_dsp_sample_handout_v2 import register_fonts
from reportlab.pdfbase import pdfmetrics


def _visual_group_center(baselines, font_name, font_size, leading):
    ascent = pdfmetrics.getAscent(font_name) * font_size / 1000
    descent = pdfmetrics.getDescent(font_name) * font_size / 1000
    top = baselines[0] + ascent
    bottom = baselines[-1] + descent
    return (top + bottom) / 2


def test_single_line_text_is_visually_centered():
    register_fonts()
    baselines = centered_text_baselines("CNB", 9.2, 100, 1)
    assert abs(_visual_group_center(baselines, "CNB", 9.2, 12.4) - 100) < 0.01


def test_multiline_text_group_is_visually_centered():
    register_fonts()
    baselines = centered_text_baselines("CNB", 9.2, 100, 2, leading=13)
    assert abs(_visual_group_center(baselines, "CNB", 9.2, 13) - 100) < 0.01
