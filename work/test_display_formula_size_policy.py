from pathlib import Path
import sys


WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(WORK))

from make_dsp_sample_handout_v2 import normalize_display_formula_height


def test_small_display_formula_uses_printable_baseline_height():
    assert normalize_display_formula_height(20) == 28


def test_normal_display_formula_keeps_requested_height():
    assert normalize_display_formula_height(34) == 34


def test_dense_display_formula_keeps_larger_requested_height():
    assert normalize_display_formula_height(48) == 48
