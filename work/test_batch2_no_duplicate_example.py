from pathlib import Path


SOURCE = Path(__file__).with_name("make_dsp_batch_016_024.py")


def test_batch2_starts_with_chapter_three_without_repeating_example_two():
    source = SOURCE.read_text(encoding="utf-8")

    assert 'doc.section = "3. 时域离散系统"' in source
    assert '# Section 3.1 is carried by the sample tail page.' in source
    assert 'doc.h2("3.2 时不变（考点）")' in source
    assert 'doc.h2("2.4 序列的变换：例 2")' not in source
    # The helper may remain available, but build_pdf must not call it.
    assert source.count("draw_example2_plot(doc)") == 1
