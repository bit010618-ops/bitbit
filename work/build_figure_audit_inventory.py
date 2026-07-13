from __future__ import annotations

import ast
from pathlib import Path


BATCH_SCRIPTS = {
    1: "make_dsp_sample_handout_v2.py",
    2: "make_dsp_batch_016_024.py",
    3: "make_dsp_batch_046_088.py",
    4: "make_dsp_batch_089_112.py",
    5: "make_dsp_batch_115_140.py",
    6: "make_dsp_batch_141_184.py",
    7: "make_dsp_batch_185_227.py",
    8: "make_dsp_batch_228_265_redraw.py",
    9: "make_dsp_batch_266_300_redraw.py",
    10: "make_dsp_batch_301_332_redraw.py",
    11: "make_dsp_batch_333_366_redraw.py",
    12: "make_dsp_batch_367_399_redraw.py",
    13: "make_dsp_batch_400_436_redraw.py",
}

EXCLUDED_PREFIXES = (
    "draw_formula",
    "draw_math",
    "draw_note",
    "draw_text",
    "draw_paragraph",
    "draw_heading",
    "draw_red_text",
    "draw_img",
)

SOURCE_PAGE_HINTS = {
    (1, "draw_signal_classification_examples"): "3",
    (1, "draw_flow"): "4",
    (1, "draw_discrete_axes_plot"): "6, 7, 12, 14, 16",
    (1, "draw_rect_sequence_example"): "7",
    (1, "draw_oscillation_nine"): "12",
    (1, "draw_scale_transform_triplet"): "14",
    (1, "draw_example2_plot"): "16",
    (8, "split_flow"): "238, 242",
    (8, "small_butterfly"): "241, 249",
    (8, "fft_butterfly"): "245, 251",
}

HANDOUT_PAGE_HINTS = {
    (8, "split_flow"): "54",
    (8, "small_butterfly"): "54",
    (8, "fft_butterfly"): "55, 56",
}


def _is_figure_function(name: str) -> bool:
    if name.startswith(EXCLUDED_PREFIXES):
        return False
    return (
        name.startswith("draw_")
        or name.endswith(("diagram", "plot", "flow", "structure"))
        or "butterfly" in name
        or any(
            token in name
            for token in (
                "system_chain",
                "spectrum_axis",
                "freq_replicas",
                "filter_cascade",
                "lm_conversion",
                "multistage",
                "tdm_fdm",
            )
        )
    )


def build_inventory(root: Path) -> list[dict]:
    work = root / "work"
    rows: list[dict] = []
    for batch, filename in BATCH_SCRIPTS.items():
        path = work / filename
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not _is_figure_function(node.name):
                continue
            rows.append(
                {
                    "batch": batch,
                    "script": filename,
                    "function": node.name,
                    "definition_line": node.lineno,
                    "source_page": SOURCE_PAGE_HINTS.get((batch, node.name), ""),
                    "handout_page": HANDOUT_PAGE_HINTS.get((batch, node.name), ""),
                    "status": "pending",
                    "difference": "待逐图对照",
                }
            )
    return rows


def write_markdown(root: Path, rows: list[dict]) -> Path:
    output = root / "work" / "figure_audit_matrix.md"
    lines = [
        "# 全书图形逐图对照矩阵",
        "",
        "验收规则：图形内部只允许整体等比缩放；拓扑、连线起点/拐点/终点、箭头、节点、标签和相对比例必须与原 PDF 一致。",
        "",
        "| 批次 | 脚本 | 绘图函数 | 定义行 | 原课件页 | 讲义页 | 状态 | 差异记录 |",
        "|---:|---|---|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {batch} | {script} | `{function}` | {definition_line} | {source_page} | {handout_page} | {status} | {difference} |".format(
                **row
            )
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    inventory = build_inventory(project_root)
    path = write_markdown(project_root, inventory)
    print(f"{len(inventory)} figure functions -> {path}")
