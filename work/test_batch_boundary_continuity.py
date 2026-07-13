from pathlib import Path


SAMPLE = Path(__file__).with_name("make_dsp_sample_handout_v2.py").read_text(encoding="utf-8")
BATCH2 = Path(__file__).with_name("make_dsp_batch_016_024.py").read_text(encoding="utf-8")


def test_chapter_three_intro_fills_sample_tail_page():
    assert "def append_chapter3_intro" in SAMPLE
    assert "append_chapter3_intro(doc, f_system_intro, f_super_intro, f_homo_intro, f_linear_intro)" in SAMPLE


def test_batch_two_starts_at_section_31_without_duplicate_intro():
    marker = "# Chapter 3 title and system definition are carried by the sample tail page."
    assert marker in BATCH2
    assert "# Section 3.1 is carried by the sample tail page." in BATCH2
