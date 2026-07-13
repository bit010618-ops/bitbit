from pathlib import Path


B3 = Path(__file__).with_name("make_dsp_batch_046_088.py").read_text(encoding="utf-8")
B4 = Path(__file__).with_name("make_dsp_batch_089_112.py").read_text(encoding="utf-8")


def test_chapter_directory_moves_to_previous_tail_page():
    assert "def append_chapter_review" in B3
    assert "append_chapter_review(doc)" in B3


def test_batch4_does_not_repeat_chapter_directory():
    assert "# Chapter review and homework are carried by the previous batch tail page." in B4
