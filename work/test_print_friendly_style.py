import inspect
import unittest

from work import make_dsp_sample_handout_v2 as base
from work import make_dsp_batch_016_024 as batch2


class PrintFriendlyStyleTests(unittest.TestCase):
    def test_headers_use_thin_rule_without_color_band(self):
        for method in (base.Doc.header, batch2.BatchDoc.header):
            source = inspect.getsource(method)
            self.assertNotIn("c.rect(0, PAGE_H - 34", source)
            self.assertIn("c.line(MARGIN_X", source)

    def test_added_document_chrome_is_not_blue_filled(self):
        self.assertNotIn("BLUE_DARK", inspect.getsource(base.Doc.table))
        self.assertNotIn("BLUE_LIGHT", inspect.getsource(base.Doc.note))
        self.assertNotIn("PALE", inspect.getsource(base.Doc.formula_box))

    def test_added_bullets_are_black(self):
        self.assertNotIn("setFillColor(BLUE)", inspect.getsource(base.Doc.bullet))
        self.assertNotIn("setFillColor(BLUE)", inspect.getsource(base.Doc.formula_bullets))


if __name__ == "__main__":
    unittest.main()
