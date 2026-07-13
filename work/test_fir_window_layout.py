import unittest

from work.make_dsp_batch_367_399_redraw import CONTENT_W, _window_effect_layout


class FirWindowLayoutTests(unittest.TestCase):
    def test_three_frequency_axes_and_omega_labels_fit_content_width(self):
        layout = _window_effect_layout()
        right_edge = layout['offsets'][-1] + layout['width'] + layout['label_allowance']
        self.assertLessEqual(right_edge, CONTENT_W)


if __name__ == '__main__':
    unittest.main()
