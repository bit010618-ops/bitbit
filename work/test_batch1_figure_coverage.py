import ast
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "make_dsp_sample_handout_v2.py"


def function_names_and_calls():
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8-sig"))
    definitions = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    return definitions, calls


class BatchOneFigureCoverageTests(unittest.TestCase):
    def test_all_source_figure_groups_have_dedicated_renderers(self):
        definitions, calls = function_names_and_calls()
        expected = {
            "draw_signal_classification_examples",
            "draw_rect_sequence_example",
            "draw_oscillation_nine",
            "draw_scale_transform_triplet",
        }
        self.assertTrue(expected <= definitions)
        self.assertTrue(expected <= calls)

    def test_original_processing_flow_renderer_is_used(self):
        definitions, calls = function_names_and_calls()
        self.assertIn("draw_flow", definitions)
        self.assertIn("draw_flow", calls)

    def test_batch_output_matches_full_handout_merge_input(self):
        source = SCRIPT.read_text(encoding="utf-8-sig")
        self.assertIn(
            'PDF_PATH = OUT_DIR / "DSP讲义重制_样章_前15页_坐标轴明显加长版.pdf"',
            source,
        )

    def test_oscillation_section_is_not_forced_to_a_new_page(self):
        source = SCRIPT.read_text(encoding="utf-8-sig")
        self.assertNotIn("doc.ensure(410)", source)
        tree = ast.parse(source)
        renderer = next(
            node for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "draw_oscillation_nine"
        )
        renderer_source = ast.get_source_segment(source, renderer)
        self.assertNotIn("doc.ensure(295)", renderer_source)
        self.assertIn("doc.ensure(row_h)", renderer_source)

    def test_example_plot_reserves_room_for_the_source_proportioned_axis(self):
        source = SCRIPT.read_text(encoding="utf-8-sig")
        tree = ast.parse(source)
        renderer = next(
            node for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "draw_example2_plot"
        )
        renderer_source = ast.get_source_segment(source, renderer)
        self.assertIn("doc.ensure(168)", renderer_source)
        self.assertIn("doc.y - 18", renderer_source)
        self.assertIn("150", renderer_source)
        self.assertNotIn("doc.exercise_space(18)", source)
        self.assertIn("draw_formula_plain(doc, f_ex2_given, max_h=62, gap=6)", source)
        self.assertIn("draw_formula_plain(doc, f_ex2_value2, max_h=22, gap=5)", source)


if __name__ == "__main__":
    unittest.main()
