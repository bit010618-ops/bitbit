from pathlib import Path
import sys


WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(WORK))

from make_dsp_sample_handout_v2 import Doc, auto_math_runs, register_fonts


def _doc(tmp_path):
    register_fonts()
    doc = Doc(tmp_path / "spacing.pdf")
    doc.start()
    doc.y = 700
    return doc


def test_rich_paragraph_advances_by_full_leading_plus_gap(tmp_path):
    doc = _doc(tmp_path)
    start = doc.y
    doc.rich_p(auto_math_runs("采样频率满足 f_s > 2f_m。"), size=9.8, leading=16)
    assert start - doc.y >= 20


def test_rich_bullets_keep_full_item_leading_and_gap(tmp_path):
    doc = _doc(tmp_path)
    start = doc.y
    items = [
        auto_math_runs("翻转：x[-n] 是 x[n] 关于 n=0 的镜像。"),
        auto_math_runs("抽取：x[Mn] 表示时间轴压缩。"),
    ]
    doc.rich_bullet(items, size=9.4, leading=15)
    assert start - doc.y >= 36


def test_rich_heading_advances_by_full_line_height(tmp_path):
    doc = _doc(tmp_path)
    start = doc.y
    doc.rich_h3(auto_math_runs("例：求 R_4(n) 的 DFS"))
    assert start - doc.y >= 17
