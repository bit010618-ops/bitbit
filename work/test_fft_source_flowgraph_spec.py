import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("make_dsp_batch_228_265_redraw.py")


def load_module():
    spec = importlib.util.spec_from_file_location("fft_redraw", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_dit_stage_pairings_match_source_slide_245():
    module = load_module()
    graph = module._fft_graph_spec("DIT")

    assert graph["input_order"] == [0, 4, 2, 6, 1, 5, 3, 7]
    assert graph["output_order"] == list(range(8))
    assert graph["stage_pairs"] == [
        [(0, 1), (2, 3), (4, 5), (6, 7)],
        [(0, 2), (1, 3), (4, 6), (5, 7)],
        [(0, 4), (1, 5), (2, 6), (3, 7)],
    ]
    assert graph["stage_exponents"] == [
        [0, 0, 0, 0],
        [0, 2, 0, 2],
        [0, 1, 2, 3],
    ]
    assert graph["title_banner"] == "pink"
    assert graph["stage_fill"] == "green"
    assert graph["stage_count_badge"] == r"M=\log_2N"


def test_dif_stage_pairings_match_source_slide_251():
    module = load_module()
    graph = module._fft_graph_spec("DIF")

    assert graph["input_order"] == list(range(8))
    assert graph["output_order"] == [0, 4, 2, 6, 1, 5, 3, 7]
    assert graph["stage_pairs"] == [
        [(0, 4), (1, 5), (2, 6), (3, 7)],
        [(0, 2), (1, 3), (4, 6), (5, 7)],
        [(0, 1), (2, 3), (4, 5), (6, 7)],
    ]
    assert graph["stage_exponents"] == [
        [0, 1, 2, 3],
        [0, 2, 0, 2],
        [0, 0, 0, 0],
    ]
    assert graph["title_banner"] == "pink"
    assert graph["outer_frame"] == "green"


def test_ifft_uses_source_negative_twiddles_and_final_scaling():
    module = load_module()
    graph = module._fft_graph_spec("IFFT")

    assert graph["stage_pairs"] == module._fft_graph_spec("DIF")["stage_pairs"]
    assert graph["stage_exponents"] == [
        [0, -1, -2, -3],
        [0, -2, 0, -2],
        [0, 0, 0, 0],
    ]
    assert graph["output_scale"] == ["1/N"] * 8


def test_build_draws_a_dedicated_ifft_flowgraph():
    source = MODULE_PATH.read_text(encoding="utf-8")

    dif_section = source.index("doc.h2('基于频率抽取的基 2 FFT')")
    ifft_section = source.index("doc.h2('4.3 快速傅里叶反变换 IFFT')")
    dif_call = source.index("fft_butterfly(doc,'DIF')", dif_section)
    ifft_call = source.index("fft_butterfly(doc,'IFFT')", ifft_section)

    assert dif_section < dif_call < ifft_section < ifft_call


def test_dif_source_caption_is_not_duplicated_below_the_graph():
    source = MODULE_PATH.read_text(encoding="utf-8")

    assert source.count('频率抽取法和时间抽取法总的计算量相同') == 1


def test_twiddle_symbol_matches_each_source_flowgraph():
    module = load_module()

    assert module._twiddle_tex('DIT', 3) == r'W_8^{3}'
    assert module._twiddle_tex('DIF', 2) == r'W_N^{2}'
    assert module._twiddle_tex('IFFT', -2) == r'W_N^{-2}'
