from pathlib import Path


SOURCE = Path(__file__).with_name("make_dsp_batch_228_265_redraw.py").read_text(encoding="utf-8")


def test_dit_complexity_derivation_precedes_flowgraph():
    heading = SOURCE.index("doc.h2('基于时间抽取的基 2 FFT')")
    graph = SOURCE.index("fft_butterfly(doc,'DIT')", heading)
    block = SOURCE[heading:graph]
    assert "每一级包含 N/2 个蝶形" in block
    assert "\\frac{N}{2}\\log_2N" in block
    assert "N\\log_2N" in block


def test_dit_flowgraph_keeps_source_complexity_chain():
    assert r"\frac{N}{2}\times M=\frac{N}{2}\log_2N" in SOURCE
