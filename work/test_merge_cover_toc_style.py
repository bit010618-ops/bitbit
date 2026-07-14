from pathlib import Path
import unittest


MERGE_SOURCE = Path(__file__).with_name("merge_full_handout.py")


class MergeCoverAndTocStyleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = MERGE_SOURCE.read_text(encoding="utf-8")

    def test_merge_adds_a_dedicated_cover_before_directory(self):
        self.assertIn("def make_cover", self.source)
        self.assertIn("writer.insert_page(make_cover(), 0)", self.source)
        self.assertIn("writer.insert_page(make_directory(starts), 1)", self.source)
        cover_pos = self.source.index("writer.insert_page(make_cover(), 0)")
        directory_pos = self.source.index("writer.insert_page(make_directory(starts), 1)")
        self.assertLess(cover_pos, directory_pos)

    def test_cover_and_directory_do_not_use_a_blue_header_band(self):
        self.assertNotIn("c.rect(0,h-34,w,34", self.source)
        self.assertNotIn("#0F5E9C", self.source)

    def test_cover_is_unnumbered_and_directory_starts_at_page_one(self):
        self.assertIn("if physical_index == 0", self.source)
        self.assertIn("printed_page = physical_index", self.source)

    def test_no_black_and_white_derivative_is_generated(self):
        lowered = self.source.lower()
        self.assertNotIn("black_white", lowered)
        self.assertNotIn("grayscale", lowered)
        self.assertNotIn("黑白版", self.source)

    def test_cover_omits_redundant_complete_color_a4_caption(self):
        self.assertNotIn("完整彩色 A4 讲义", self.source)


if __name__ == "__main__":
    unittest.main()
