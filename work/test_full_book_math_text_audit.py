from pathlib import Path

from audit_math_rendering import (
    classify_pdf_source_text,
    classify_plain_text_math,
    scan_math_rendering_slashes,
    scan_source,
)
from make_dsp_sample_handout_v2 import (
    Doc,
    _matplotlib_color,
    _normalize_math_expr,
    auto_math_runs,
    draw_auto_math_block,
    draw_auto_math_text,
    draw_centered_multiline_text,
    register_fonts,
)


register_fonts()


def test_normalize_math_keeps_greek_command_separate_from_following_variable():
    assert _normalize_math_expr("Ω = ωT") == r"\Omega = \omega T"


def test_auto_math_runs_keeps_complete_complex_exponential_with_plus_minus():
    runs = auto_math_runs("零点 0.5e^{±jπ/4} 关于单位圆成对出现。")
    assert ("math", r"0.5e^{\pm \frac{j\pi}{4}}") in runs


def test_detects_source_like_math_beyond_reported_examples():
    cases = {
        "X(e^{jω})": {"caret", "math_function"},
        "R_4(n)": {"subscript", "math_function"},
        "x(n)={1,2,3,4}": {"math_function", "relation", "set_literal"},
        "H(z) 在 ω=0、π 处为零": {"math_function", "relation"},
        "θ_k=-(N-1)πk/N": {"subscript", "relation", "slash_division"},
        "0<=n<=2": {"relation"},
        "f_s ≥ 2f_m": {"subscript", "relation"},
    }
    for text, expected in cases.items():
        assert expected <= classify_plain_text_math(text), text


def test_detects_every_mathematical_slash_as_division():
    for text in (
        "ω/(2π)=k/N",
        "N/2 个蝶形",
        "1/N",
        "(N-1)/2",
        "3/4",
        "π/M",
    ):
        assert "slash_division" in classify_plain_text_math(text), text


def test_pdf_text_scanner_rejects_source_notation_and_math_slashes():
    assert "raw_latex" in classify_pdf_source_text(r"X(e^{j\omega})")
    assert "raw_subscript" in classify_pdf_source_text("R_4(n)")
    assert "slash_division" in classify_pdf_source_text("ω/(2π)=k/N")


def test_pdf_text_scanner_allows_nondivision_names():
    for text in (
        "A/D 转换", "D/A 转换", "DFT/IDFT", "DFS/DFT", "IIR/FIR",
        "DFT/FFT", "DIT/DIF", "LP / HP / BP / BS", "LP / BP", "HP / BP",
    ):
        assert "slash_division" not in classify_pdf_source_text(text)


def test_does_not_treat_converter_or_algorithm_acronyms_as_division():
    for text in (
        "A/D 转换", "D/A 转换", "DFT/IDFT", "DFS/DFT", "IIR/FIR",
        "DFT/FFT", "DIT/DIF", "LP / HP / BP / BS", "LP / BP", "HP / BP",
    ):
        assert "slash_division" not in classify_plain_text_math(text), text


def test_auto_math_runs_extracts_reported_examples_and_renders_subscripts():
    runs = auto_math_runs(
        "DTFT 频谱记为 X(e^{jω})，矩形序列为 R_4(n)。"
    )

    math = [value for kind, value in runs if kind == "math"]
    assert r"X(e^{j\omega})" in math
    assert r"R_{4}(n)" in math


def test_auto_math_runs_converts_every_division_to_stacked_fraction():
    samples = {
        "ω/(2π)=k/N": (r"\frac{\omega}{2\pi}", r"\frac{k}{N}"),
        "N/2 个蝶形": (r"\frac{N}{2}",),
        "输出端乘以 1/N。": (r"\frac{1}{N}",),
        "τ=(N-1)/2=5/2": (r"\frac{N-1}{2}", r"\frac{5}{2}"),
        "截止频率为 π/M": (r"\frac{\pi}{M}",),
        "48/32=3/2": (r"\frac{48}{32}", r"\frac{3}{2}"),
    }
    for source, expected in samples.items():
        runs = auto_math_runs(source)
        math = [value for kind, value in runs if kind == "math"]
        joined = " ".join(math)
        assert all(fragment in joined for fragment in expected), (source, runs)
        assert "/" not in joined, (source, runs)


def test_auto_math_runs_preserves_nondivision_slash_names_as_text():
    source = "A/D、D/A 与 DFT/IDFT 是名称，不是除法。"
    runs = auto_math_runs(source)

    assert "".join(value for kind, value in runs if kind == "text") == source
    assert not [value for kind, value in runs if kind == "math"]


def test_plain_paragraph_delegates_formula_fragments_to_rich_renderer(tmp_path):
    doc = Doc(tmp_path / "paragraph.pdf")
    captured = []
    doc.rich_p = lambda runs, size=9.8, leading=16: captured.append(runs)

    doc.p("采样关系为 ω/(2π)=k/N。")

    assert captured
    assert any(kind == "math" and r"\frac" in value for kind, value in captured[0])


def test_plain_bullets_delegate_formula_fragments_to_rich_renderer(tmp_path):
    doc = Doc(tmp_path / "bullets.pdf")
    captured = []
    doc.rich_bullet = lambda items, size=9.4, leading=15: captured.extend(items)

    doc.bullet(["输出端乘以 1/N。", "普通说明。"])

    assert any(kind == "math" and value == r"\frac{1}{N}" for kind, value in captured[0])


def test_plain_heading_delegates_formula_fragments_to_rich_renderer(tmp_path):
    doc = Doc(tmp_path / "heading.pdf")
    captured = []
    doc.rich_h2 = lambda runs: captured.append(runs)

    doc.h2("例 1 求 R_4(n) 的 DFS")

    assert any(kind == "math" and value == r"R_{4}(n)" for kind, value in captured[0])


def test_plain_subheading_delegates_formula_fragments_to_rich_renderer(tmp_path):
    doc = Doc(tmp_path / "subheading.pdf")
    captured = []
    doc.rich_h3 = lambda runs: captured.append(runs)

    doc.h3("频域判断：H(z) 的极点")

    assert any(kind == "math" and value == r"H(z)" for kind, value in captured[0])


def test_note_delegates_formula_fragments_to_rich_renderer(tmp_path):
    doc = Doc(tmp_path / "note.pdf")
    captured = []
    doc.rich_note = lambda title_runs, body_runs, compact=False: captured.append(
        (title_runs, body_runs)
    )

    doc.note("考点", "当 n<0 时，输出为 1/N。")

    assert any(kind == "math" and value == r"n<0" for kind, value in captured[0][1])
    assert any(kind == "math" and value == r"\frac{1}{N}" for kind, value in captured[0][1])


def test_plain_chinese_prose_is_not_flagged():
    assert classify_plain_text_math("讲义重排时保留原页含义和全部教学内容。") == set()


def test_reportlab_hex_color_is_normalized_for_matplotlib():
    assert _matplotlib_color("0x1f2933") == "#1f2933"
    assert _matplotlib_color("#d71920") == "#d71920"


def test_scanner_accepts_utf8_bom_generators(tmp_path):
    source = tmp_path / "bom_generator.py"
    source.write_text('c.drawString(0, 0, "采样关系为 ω/(2π)=k/N。")\n', encoding="utf-8-sig")

    findings = scan_source(source)

    assert len(findings) == 1
    assert "slash_division" in findings[0].reasons


def test_scanner_ignores_math_that_plain_doc_methods_auto_render(tmp_path):
    source = tmp_path / "auto_rendered_generator.py"
    source.write_text(
        '\n'.join(
            [
                'doc.p("采样关系为 ω/(2π)=k/N。")',
                'doc.h2("例 1 求 R_4(n) 的 DFS")',
                'doc.h3("频域判断：H(z) 的极点")',
                'doc.bullet(["输出端乘以 1/N。"] )',
                'doc.note("考点", "当 n<0 时，输出为 1/N。")',
            ]
        ),
        encoding="utf-8",
    )

    assert scan_source(source) == []


def test_scanner_still_flags_direct_canvas_math(tmp_path):
    source = tmp_path / "direct_canvas_generator.py"
    source.write_text(
        'c.drawString(0, 0, "ω/(2π)=k/N")\n',
        encoding="utf-8",
    )

    findings = scan_source(source)

    assert len(findings) == 1
    assert findings[0].call == "drawString"
    assert "slash_division" in findings[0].reasons


def test_scanner_flags_math_passed_to_custom_plot_helpers(tmp_path):
    source = tmp_path / "custom_plot_labels.py"
    source.write_text(
        '\n'.join(
            [
                'mini_axis(c, 0, 0, "|H_d(e^{jω})|")',
                'spectrum_axis(c, 0, 0, "π/2")',
                'triangle_spectrum(c, 0, 0, "输入频谱 X(e^{jω})")',
            ]
        ),
        encoding="utf-8",
    )

    findings = scan_source(source)

    assert len(findings) == 1
    assert findings[0].call == "spectrum_axis"


def test_scanner_ignores_coordinate_dictionary_keys(tmp_path):
    source = tmp_path / "coordinate_keys.py"
    source.write_text(
        'c.drawString(x + offset["x_offset"], y + offset["y_offset"], "0")\n',
        encoding="utf-8",
    )

    assert scan_source(source) == []


class _CanvasProbe:
    def __init__(self):
        self.strings = []
        self.images = []

    def setFillColor(self, color):
        pass

    def setFont(self, font, size):
        pass

    def drawString(self, x, y, text):
        self.strings.append((x, y, text))

    def drawImage(self, image, x, y, width, height, mask=None):
        self.images.append((x, y, width, height, mask))


def test_direct_canvas_auto_math_renderer_renders_formula_and_fraction():
    canvas = _CanvasProbe()

    width = draw_auto_math_text(
        canvas,
        100,
        200,
        "采样关系 ω/(2π)=k/N。",
        font="CN",
        size=10,
    )

    assert width > 0
    assert canvas.images
    assert "/" not in "".join(text for _, _, text in canvas.strings)


def test_wrapped_canvas_auto_math_renderer_renders_and_wraps_formula():
    canvas = _CanvasProbe()

    bottom = draw_auto_math_block(
        canvas,
        20,
        200,
        "采样关系为 ω/(2π)=k/N，且输出端乘以 1/N。",
        width=120,
        font="CN",
        size=10,
        leading=16,
    )

    assert bottom < 184
    assert canvas.images
    assert "/" not in "".join(text for _, _, text in canvas.strings)
    assert len({round(y, 2) for _, y, _ in canvas.strings}) >= 2


def test_centered_multiline_canvas_renderer_uses_rendered_math():
    canvas = _CanvasProbe()

    draw_centered_multiline_text(
        canvas,
        120,
        160,
        "N≥M\nω/(2π)=k/N",
        "CNB",
        10,
        leading=15,
    )

    assert canvas.images
    assert "/" not in "".join(text for _, _, text in canvas.strings)


def test_scanner_treats_direct_canvas_auto_math_renderer_as_rendered(tmp_path):
    source = tmp_path / "auto_canvas.py"
    source.write_text(
        'draw_auto_math_text(c, 0, 0, "ω/(2π)=k/N")\n',
        encoding="utf-8",
    )

    assert scan_source(source) == []


def test_scanner_treats_auto_math_red_wrappers_as_rendered(tmp_path):
    source = tmp_path / "auto_red_wrappers.py"
    source.write_text(
        '\n'.join(
            [
                'red_line(doc, "截止频率为 π/M，且 L/M=3/2。")',
                'draw_red_text(doc, "群延迟 τ=(N-1)/2。")',
            ]
        ),
        encoding="utf-8",
    )

    assert scan_source(source) == []


def test_scanner_treats_centered_multiline_renderer_as_rendered(tmp_path):
    source = tmp_path / "auto_centered_multiline.py"
    source.write_text(
        'draw_centered_multiline_text(c, 0, 0, "N≥M\\nω/(2π)=k/N")\n',
        encoding="utf-8",
    )

    assert scan_source(source) == []


def test_scanner_treats_formula_aware_table_cells_as_rendered(tmp_path):
    source = tmp_path / "auto_table.py"
    source.write_text(
        'doc.table(["序列"], [["矩形序列 R_N[n]，长度 N/2"]], [120])\n',
        encoding="utf-8",
    )

    assert scan_source(source) == []


def test_scanner_checks_rich_text_runs_but_ignores_math_runs(tmp_path):
    source = tmp_path / "rich_generator.py"
    source.write_text(
        'doc.rich_p([("text", "采样关系 ω/(2π)"), '
        '("math", r"\\frac{\\omega}{2\\pi}")])\n',
        encoding="utf-8",
    )

    findings = scan_source(source)

    assert len(findings) == 1
    assert findings[0].text == "采样关系 ω/(2π)"


def test_scanner_checks_untagged_strings_inside_rich_calls(tmp_path):
    source = tmp_path / "rich_bullets.py"
    source.write_text(
        'doc.rich_bullet([["普通说明"], ["仍有 k/N"]])\n',
        encoding="utf-8",
    )

    findings = scan_source(source)

    assert len(findings) == 1
    assert findings[0].text == "仍有 k/N"


def test_scanner_rejects_slash_notation_inside_rendered_math(tmp_path):
    source = tmp_path / "rendered_math_slashes.py"
    source.write_text(
        '\n'.join(
            [
                'formula_png("a", r"X(e^{j\\omega/2})", 14)',
                'draw_formula_block(doc, r"N/2", "b")',
                'doc.rich_p([("math", r"k/N")])',
            ]
        ),
        encoding="utf-8",
    )

    findings = scan_math_rendering_slashes(source)

    assert len(findings) == 3
    assert all(item.reasons == ("math_slash_division",) for item in findings)


def test_scanner_accepts_stacked_fractions_inside_rendered_math(tmp_path):
    source = tmp_path / "rendered_math_fractions.py"
    source.write_text(
        'formula_png("a", r"X(e^{j\\frac{\\omega}{2}})", 14)\n',
        encoding="utf-8",
    )

    assert scan_math_rendering_slashes(source) == []


def test_scanner_treats_ratio_tex_as_fraction_transformer(tmp_path):
    source = tmp_path / "ratio_transform.py"
    source.write_text('ratio_tex("1/3")\n', encoding="utf-8")

    assert scan_source(source) == []
    assert scan_math_rendering_slashes(source) == []


def test_batch_141_184_has_no_plain_text_mathematics():
    path = Path(__file__).with_name("make_dsp_batch_141_184.py")

    assert scan_source(path) == []


def _function_source(path, start_name, end_name):
    source = path.read_text(encoding="utf-8-sig")
    start = source.index(f"def {start_name}")
    end = source.index(f"def {end_name}", start)
    return source[start:end]


def test_strip_mapping_renders_pi_over_t_as_math():
    path = Path(__file__).with_name("make_dsp_batch_115_140.py")
    body = _function_source(path, "draw_strip_mapping", "draw_filter_map")

    assert "draw_auto_math_text" in body
    assert 'drawString(x0 + 8, yy, lab)' not in body


def test_fir_custom_axes_and_labels_use_auto_math_renderer():
    path = Path(__file__).with_name("make_dsp_batch_367_399_redraw.py")
    mini_axis = _function_source(path, "mini_axis", "linear_phase_classification_example")
    window_diagrams = _function_source(path, "draw_window_six_diagrams", "draw_gibbs_page")
    chapter_map = _function_source(path, "fir_chapter_map", "draw_source_367_374")

    assert mini_axis.count("draw_auto_math_text") >= 2
    assert "drawString(x+10,y+h*0.55+11,title)" not in mini_axis
    assert "drawCentredString(xx,y-12,lab)" not in mini_axis
    assert window_diagrams.count("draw_auto_math_text") >= 2
    assert "drawString(x0 + 4, cy + 51, lt)" not in window_diagrams
    assert "drawString(rx + 4, cy + 51, rt)" not in window_diagrams
    assert "draw_auto_math_text" in chapter_map
    assert "drawCentredString(bx,yy,item)" not in chapter_map


def test_multirate_custom_plot_helpers_use_auto_math_renderer():
    path = Path(__file__).with_name("make_dsp_batch_400_436_redraw.py")
    spectrum_axis = _function_source(path, "spectrum_axis", "freq_replicas")
    stem = _function_source(path, "_stem_envelope", "_draw_spectrum_title")
    title = _function_source(path, "_draw_spectrum_title", "_triangle_spectrum")
    triangle = _function_source(path, "_triangle_spectrum", "draw_decimation_sampling_theorem_page")
    exercise_triangle = _function_source(path, "triangle_spectrum", "draw_up2_filter_down2_spectra_page")

    assert "draw_auto_math_text" in spectrum_axis
    assert "drawCentredString(xx,y-12,txt)" not in spectrum_axis
    assert "draw_auto_math_text" in stem
    assert "drawString(x + 3, y + h + 14, label)" not in stem
    assert "draw_auto_math_text" in title
    assert "draw_auto_math_text" in triangle
    assert "drawCentredString(x + w / 2 + rel * w, y - 12, text)" not in triangle
    assert exercise_triangle.count("draw_auto_math_text") >= 3


def test_fft_sequence_blocks_render_every_entry_as_math():
    path = Path(__file__).with_name("make_dsp_batch_228_265_redraw.py")
    body = _function_source(path, "sequence_block", "two_col_table")

    assert body.count("draw_auto_math_text") >= 2
    assert "drawCentredString(x+w/2,top-i*step,item)" not in body
    assert "drawCentredString(x+w/2,y+h/2+11,title)" not in body


def test_dft_pipeline_and_stem_titles_use_auto_math_renderer():
    path = Path(__file__).with_name("make_dsp_batch_185_227.py")
    pipeline = _function_source(path, "draw_pipeline", "stem_plot_axis_geometry")
    stem = _function_source(path, "draw_stem_plot", "draw_small_table")

    assert "draw_auto_math_text" in pipeline
    assert "drawCentredString(x + w / 2, y + 11, label)" not in pipeline
    assert "draw_auto_math_text" in stem
    assert 'if "\\\\" in title or "^" in title:' not in stem


def test_multirate_system_blocks_render_labels_as_math():
    path = Path(__file__).with_name("make_dsp_batch_400_436_redraw.py")
    body = _function_source(path, "block", "tdm_rate_block_geometry")
    chain = _function_source(path, "system_chain", "draw_dat_conversion_chain")

    assert "draw_centered_multiline_text" in body
    assert "draw_auto_math_text" in chain
    assert "drawString(MARGIN_X,top-6,title)" not in chain


def test_custom_note_and_table_helpers_render_inline_math():
    batch7 = Path(__file__).with_name("make_dsp_batch_185_227.py")
    blue_note = _function_source(batch7, "draw_blue_note", "draw_two_col")
    two_col = _function_source(batch7, "draw_two_col", "draw_pipeline")
    table = _function_source(batch7, "draw_small_table", "draw_bullet_list")
    batch9 = Path(__file__).with_name("make_dsp_batch_266_300_redraw.py")
    note = _function_source(batch9, "draw_note", "arrow")

    assert "draw_auto_math_text" in blue_note
    assert "draw_auto_math_block" in blue_note
    assert "draw_auto_math_text" in two_col
    assert "draw_auto_math_block" in two_col
    assert table.count("draw_auto_math_text") >= 2
    assert "drawAuto" not in table
    assert "draw_auto_math_text" in note
    assert "draw_auto_math_block" in note


def test_discrete_axis_and_unit_circle_labels_render_as_math():
    sample = Path(__file__).with_name("make_dsp_sample_handout_v2.py")
    axes = _function_source(sample, "draw_discrete_axes_plot", "draw_example2_plot")
    batch5 = Path(__file__).with_name("make_dsp_batch_115_140.py")
    circle = _function_source(batch5, "draw_unit_circle", "draw_unit_and_response")

    assert "draw_auto_math_text" in axes
    assert "drawCentredString(x + w / 2, y - h - 8, title)" not in axes
    assert circle.count("draw_auto_math_text") >= 2
    assert "drawCentredString(cx, cy - r - 28, caption)" not in circle


def test_colored_emphasis_paragraph_renders_inline_math():
    path = Path(__file__).with_name("make_dsp_batch_115_140.py")
    body = _function_source(path, "para_red", "note_box")

    assert "draw_auto_math_text" in body
    assert "for ch in text:" not in body
