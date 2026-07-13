import unittest
import inspect

from work.make_dsp_batch_228_265_redraw import (
    CONTENT_W,
    _convolution_layout,
    _stage_twiddle_exponents,
    convolution_fft,
)


class FftTwiddleLayoutTests(unittest.TestCase):
    def test_dit_stage_exponents_match_source_diagram(self):
        self.assertEqual(_stage_twiddle_exponents("DIT", 0), [0, 0, 0, 0])
        self.assertEqual(_stage_twiddle_exponents("DIT", 1), [0, 2, 0, 2])
        self.assertEqual(_stage_twiddle_exponents("DIT", 2), [0, 1, 2, 3])

    def test_dif_stage_exponents_match_source_diagram(self):
        self.assertEqual(_stage_twiddle_exponents("DIF", 0), [0, 1, 2, 3])
        # Source slide 251 reads top-to-bottom by row-pair:
        # (0,2)->0, (1,3)->2, (4,6)->0, (5,7)->2.
        self.assertEqual(_stage_twiddle_exponents("DIF", 1), [0, 2, 0, 2])
        self.assertEqual(_stage_twiddle_exponents("DIF", 2), [0, 0, 0, 0])

    def test_linear_convolution_renderer_does_not_repeat_section_heading(self):
        source = inspect.getsource(convolution_fft)
        self.assertNotIn("'FFT 法实现线性卷积'", source)
        flow_advance = source.index("doc.y=top-125")
        formula = source.index("draw_formula_block")
        self.assertLess(flow_advance, formula)

    def test_linear_convolution_flow_stays_inside_content_width(self):
        layout = _convolution_layout()
        self.assertLessEqual(layout["right_edge"], CONTENT_W)


if __name__ == "__main__":
    unittest.main()
