import unittest
from pathlib import Path

from work.build_figure_audit_inventory import build_inventory


class FigureAuditInventoryTests(unittest.TestCase):
    def test_inventory_covers_all_handout_batches_and_known_diagrams(self):
        root = Path(__file__).resolve().parents[1]
        rows = build_inventory(root)

        batches = {row["batch"] for row in rows}
        self.assertEqual(batches, set(range(1, 14)))

        names = {row["function"] for row in rows}
        for expected in {
            "draw_flow",
            "draw_example9_block",
            "draw_dtft_mapping",
            "fft_butterfly",
            "draw_parallel_iir",
            "fir_tap_diagram",
            "sampling_structure",
        }:
            self.assertIn(expected, names)

    def test_inventory_rows_have_auditable_fields(self):
        root = Path(__file__).resolve().parents[1]
        rows = build_inventory(root)
        self.assertTrue(rows)
        for row in rows:
            self.assertTrue(row["script"].endswith(".py"))
            self.assertGreater(row["definition_line"], 0)
            self.assertIn(row["status"], {"pending", "verified"})
            self.assertIn("source_page", row)
            self.assertIn("handout_page", row)

    def test_batch_one_source_page_hints_are_recorded(self):
        root = Path(__file__).resolve().parents[1]
        rows = build_inventory(root)
        page_by_name = {row["function"]: row["source_page"] for row in rows if row["batch"] == 1}
        self.assertEqual(page_by_name["draw_signal_classification_examples"], "3")
        self.assertEqual(page_by_name["draw_flow"], "4")
        self.assertEqual(page_by_name["draw_rect_sequence_example"], "7")
        self.assertEqual(page_by_name["draw_oscillation_nine"], "12")
        self.assertEqual(page_by_name["draw_scale_transform_triplet"], "14")

    def test_fft_source_and_handout_page_hints_are_recorded(self):
        root = Path(__file__).resolve().parents[1]
        rows = build_inventory(root)
        fft_rows = {row["function"]: row for row in rows if row["batch"] == 8}
        self.assertEqual(fft_rows["split_flow"]["source_page"], "238, 242")
        self.assertEqual(fft_rows["small_butterfly"]["source_page"], "241, 249")
        self.assertEqual(fft_rows["fft_butterfly"]["source_page"], "245, 251")
        self.assertEqual(fft_rows["split_flow"]["handout_page"], "54")
        self.assertEqual(fft_rows["fft_butterfly"]["handout_page"], "55, 56")


if __name__ == "__main__":
    unittest.main()
