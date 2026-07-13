from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_batch_400_436_redraw.py").read_text(encoding="utf-8")


def test_tdm_has_mux_channel_and_demux_sides():
    assert "TDM 串行通道" in SCRIPT
    assert "tdm_demux" in SCRIPT
    assert "x_{i+1}(n)" in SCRIPT


def test_fdm_keeps_three_distinct_filter_bands():
    for label in ("LP", "BP", "HP"):
        assert repr(label) in SCRIPT or f"'{label}'" in SCRIPT
