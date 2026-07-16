from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "work" / "make_dsp_batch_400_436_redraw.py").read_text(encoding="utf-8-sig")


def test_decimation_restores_source_sampling_theorem_figures():
    assert "def draw_decimation_sampling_theorem_page(doc):" in SOURCE
    assert "f_{s1}=16\\,\\mathrm{kHz}" in SOURCE
    assert "f_{s2}=8\\,\\mathrm{kHz}" in SOURCE
    assert "x_d(n)=x(nM),\\quad M=2" in SOURCE
    assert "draw_decimation_sampling_theorem_page(doc)" in SOURCE


def test_decimation_restores_shift_and_sum_construction():
    assert "def draw_decimation_spectral_construction_page(doc):" in SOURCE
    assert "X_1(e^{j\\omega})" in SOURCE
    assert "X_1(e^{j(\\omega-\\pi)})" in SOURCE
    assert "\\frac{1}{2}\\left[X_1(e^{j\\omega})+X_1(e^{j(\\omega-\\pi)})\\right]" in SOURCE
    assert "draw_decimation_spectral_construction_page(doc)" in SOURCE


def test_interpolation_restores_zero_stuffing_mirror_and_filter_figures():
    assert "def draw_interpolation_sampling_theorem_page(doc):" in SOURCE
    assert "L=2" in SOURCE
    assert "X_p(e^{j\\omega})=X(e^{j2\\omega})" in SOURCE
    assert "H_i(e^{j\\omega})" in SOURCE
    assert "draw_interpolation_sampling_theorem_page(doc)" in SOURCE


def test_spectrum_panel_titles_use_rendered_math_instead_of_raw_latex():
    assert "def _draw_spectrum_title" in SOURCE
    assert "draw_auto_math_text(" in SOURCE
    assert "math_size=10.5" in SOURCE
    assert "_draw_spectrum_title(c, x, y, w, h, title)" in SOURCE


def test_tdm_and_fdm_restore_source_topology_and_signal_paths():
    assert "def draw_tdm_source_topology(doc):" in SOURCE
    assert "def draw_fdm_source_topology(doc):" in SOURCE
    for delay_name in ("tdm_tx_delay_1", "tdm_tx_delay_2", "tdm_rx_delay_1", "tdm_rx_delay_2"):
        assert delay_name in SOURCE
    assert "LP\\ DF" in SOURCE
    assert "BP\\ DF" in SOURCE
    assert "HP\\ DF" in SOURCE
    assert "draw_tdm_source_topology(doc)" in SOURCE
    assert "draw_fdm_source_topology(doc)" in SOURCE
    assert "doc.y = y1 - 65" in SOURCE
    assert "doc.y = 75" in SOURCE


def test_tdm_fdm_geometry_keeps_labels_and_spectra_inside_page():
    assert "def tdm_source_geometry():" in SOURCE
    assert "def fdm_source_geometry():" in SOURCE
    assert "'output_label_end': MARGIN_X + 514" in SOURCE
    assert "'right_spectrum_end': MARGIN_X + 490" in SOURCE
    assert "_delay_mark(c, left_bus - 42" in SOURCE
    assert "_delay_mark(c, right_bus + 8" in SOURCE


def test_m8_decimation_example_preserves_source_window_and_full_impulse_response():
    assert "def draw_decimation_filter_example_page(doc):" in SOURCE
    assert r"w(n)=\left[0.5-0.5\cos\left(\frac{n\pi}{20}\right)\right]R_{41}(n)" in SOURCE
    assert r"h(n)=\frac{\sin\left[\frac{\pi}{8}(n-20)\right]}{\pi(n-20)}" in SOURCE
    assert r"N-1=40" in SOURCE
    assert r"\tau=\frac{N-1}{2}=20" in SOURCE
    assert "draw_decimation_filter_example_page(doc)" in SOURCE


def test_interpolation_piecewise_condition_is_chinese_not_english():
    assert "其余整数 n 处取值均为 0。" in SOURCE
    assert r"\mathrm{else}" not in SOURCE


def test_source_order_filter_cascades_are_drawn_as_two_separate_rows():
    assert "def draw_source_filter_cascade_page(doc):" in SOURCE
    assert "['h_a(n)\\n抗混叠', '↓M\\n抽取']" in SOURCE
    assert "['↑L\\n内插', 'h_i(n)\\n抗镜像']" in SOURCE
    assert "draw_source_filter_cascade_page(doc)" in SOURCE


def test_fractional_conversion_restores_single_stage_multistage_and_dat_example():
    assert "def draw_fractional_conversion_source_page(doc):" in SOURCE
    assert "def draw_multistage_factorization_page(doc):" in SOURCE
    assert "def multistage_source_geometry():" in SOURCE
    assert "'group_count': 2" in SOURCE
    assert "'right_edge': MARGIN_X + 460" in SOURCE
    assert "c.setDash(4, 3)" in SOURCE
    assert r"h(n)=h_i(n)*h_d(n)" in SOURCE
    assert r"H(e^{j\omega})=H_i(e^{j\omega})H_d(e^{j\omega})" in SOURCE
    assert r"\frac{48000}{44100}=\frac{160}{147}" in SOURCE
    assert r"\omega_c=\min\left(\frac{\pi}{L},\frac{\pi}{M}\right)=\frac{\pi}{160}" in SOURCE
    assert "数字录音带（DAT）驱动器的采样频率为 48 kHz" in SOURCE
    assert "draw_fractional_conversion_source_page(doc)" in SOURCE
    assert "draw_multistage_factorization_page(doc)" in SOURCE
    assert "    fractional_conversion_details(doc)" not in SOURCE


def test_up2_filter_down2_example_restores_all_frequency_panels():
    assert "def draw_up2_filter_down2_spectra_page(doc):" in SOURCE
    assert "原信号频谱" in SOURCE
    assert "插零后频谱" in SOURCE
    assert "低通后频谱" in SOURCE
    assert "抽取后频谱" in SOURCE
    assert "draw_up2_filter_down2_spectra_page(doc)" in SOURCE


def test_dat_filter_block_uses_rendered_math_instead_of_raw_formula_text():
    assert "def draw_dat_conversion_chain(doc):" in SOURCE
    assert r"draw_math_at(c, r'H(e^{j\omega})'" in SOURCE
    assert "'H(e^{jω})\\n低通滤波'" not in SOURCE


def test_tdm_fdm_use_source_green_transmission_arrows_and_filtered_bands():
    assert "def _draw_green_transmission_arrow" in SOURCE
    assert "_draw_green_transmission_arrow(c, data_x" in SOURCE
    assert "_draw_green_transmission_arrow(c, bus_x + 78" in SOURCE
    assert "if kind in ('u1', 'u2', 'u3'):" in SOURCE
    assert "c.rect(x, y, w, h" in SOURCE
    assert "block(c, geometry['data_x']" not in SOURCE
    assert "block(c, MARGIN_X + 400" not in SOURCE


def test_tdm_fdm_definition_page_preserves_source_explanations():
    assert "def draw_tdm_fdm_definition_page(doc):" in SOURCE
    assert "通过时间轴的切割" in SOURCE
    assert "总带宽划分成若干个子频带" in SOURCE
    assert "draw_tdm_fdm_definition_page(doc)" in SOURCE
