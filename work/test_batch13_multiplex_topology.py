from pathlib import Path


SCRIPT = Path(__file__).with_name("make_dsp_batch_400_436_redraw.py").read_text(encoding="utf-8")


def test_tdm_has_source_transmit_and_receive_delay_chains():
    assert "def draw_tdm_source_topology(doc):" in SCRIPT
    for delay_name in ("tdm_tx_delay_1", "tdm_tx_delay_2", "tdm_rx_delay_1", "tdm_rx_delay_2"):
        assert delay_name in SCRIPT
    assert "fr'x_{subscript}(n)'" in SCRIPT


def test_fdm_keeps_three_distinct_filter_bands():
    for label in (r"\mathrm{LP\ DF}", r"\mathrm{BP\ DF}", r"\mathrm{HP\ DF}"):
        assert label in SCRIPT
