from audit_content_coverage import normalize_text, coverage_ratio, missing_fragments


def test_normalize_text_removes_layout_noise_but_keeps_math_tokens():
    assert normalize_text(" H(z) = 1 - z^{-N} \n 频率响应 ") == "h(z)=1-z^{-n}频率响应"


def test_coverage_ratio_counts_source_character_recall():
    source = "系统频率响应与零极点几何关系"
    handout = "频率响应和零极点关系"
    ratio = coverage_ratio(source, handout)
    assert 0.55 < ratio < 0.9


def test_empty_source_text_is_not_reported_as_full_coverage():
    assert coverage_ratio("", "讲义中有很多文字") == 0.0


def test_missing_fragments_returns_uncovered_source_windows():
    source = "共轭极点成对出现，幅度响应取决于向量长度，系统稳定要求极点位于单位圆内。"
    handout = "系统稳定要求极点位于单位圆内。"
    missing = missing_fragments(source, handout, window=8)
    assert any("共轭极点" in item for item in missing)
    assert any("向量长度" in item for item in missing)
