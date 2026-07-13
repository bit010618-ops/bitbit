from pathlib import Path


SOURCE = Path(__file__).with_name("make_dsp_batch_400_436_redraw.py")


def test_multistage_uses_sequential_vertical_flow():
    source = SOURCE.read_text(encoding="utf-8")
    start = source.index("def multistage(doc):")
    end = source.index("\ndef tdm_fdm(doc):", start)
    block = source[start:end]

    assert "top-95" not in block
    assert "doc.y = top - 24" in block
    assert "doc.y -= 18" in block
    assert "h=175" in block
