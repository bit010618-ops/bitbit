from pathlib import Path


SOURCE = Path(__file__).with_name("make_dsp_batch_141_184.py")


def test_four_time_frequency_cases_from_source_page_145_are_drawn():
    text = SOURCE.read_text(encoding="utf-8")
    assert "def draw_time_frequency_cases" in text
    start = text.index("def draw_transform_review")
    end = text.index("def draw_dfs_section", start)
    assert "draw_time_frequency_cases(doc)" in text[start:end]


def test_dfs_dtft_relation_map_from_source_page_148_is_drawn():
    text = SOURCE.read_text(encoding="utf-8")
    assert "def draw_dfs_relation_map" in text
    start = text.index("def draw_dfs_section")
    end = text.index("def draw_dft_definition_examples", start)
    assert "draw_dfs_relation_map(doc)" in text[start:end]


def test_chapter_page_has_no_build_process_subtitle():
    text = SOURCE.read_text(encoding="utf-8")
    assert 'doc.h1("第三章 离散傅里叶变换")' in text
    assert "原 PPT 141-184 页内容重排" not in text
