"""Find source-like mathematics drawn as ordinary text in DSP generators."""

from __future__ import annotations

import argparse
import ast
import re
from dataclasses import dataclass
from pathlib import Path


ACTIVE_GENERATORS = (
    "make_dsp_sample_handout_v2.py",
    "make_dsp_batch_016_024.py",
    "make_dsp_batch_046_088.py",
    "make_dsp_batch_089_112.py",
    "make_dsp_batch_115_140.py",
    "make_dsp_batch_141_184.py",
    "make_dsp_batch_185_227.py",
    "make_dsp_batch_228_265_redraw.py",
    "make_dsp_batch_266_300_redraw.py",
    "make_dsp_batch_301_332_redraw.py",
    "make_dsp_batch_333_366_redraw.py",
    "make_dsp_batch_367_399_redraw.py",
    "make_dsp_batch_400_436_redraw.py",
)

TEXT_CALLS = {
    "h1",
    "h2",
    "h3",
    "p",
    "bullet",
    "note",
    "table",
    "drawString",
    "drawCentredString",
    "drawRightString",
    "draw_centered_multiline_text",
    "draw_section_box",
    "draw_small_tag",
    "draw_red_text",
    "red_line",
    "draw_auto_math_text",
}

RICH_TEXT_CALLS = {
    "rich_p",
    "rich_h2",
    "rich_bullet",
    "draw_rich_section_box",
    "draw_rich_text",
    "draw_rich_red_text",
}

MATH_RENDER_CALLS = {
    "formula_png",
    "f",
    "draw_formula_block",
    "draw_math_at",
    "draw_math_label",
    "math_label",
    "piecewise_png",
    "piecewise3_png",
    "piecewise3_cn_png",
    "draw_piecewise2",
    "delay_box",
    "directional_gain_triangle",
    "gain_triangle",
    "first_order_section",
}

AUTO_RENDER_TEXT_CALLS = {
    "draw_red_text",
    "h2",
    "h3",
    "p",
    "bullet",
    "note",
    "table",
    "draw_auto_math_text",
    "draw_centered_multiline_text",
    "red_line",
    "mini_axis",
    "_stem_envelope",
    "_triangle_spectrum",
    "triangle_spectrum",
    "_fdm_mini_spectrum",
    "_figure_page",
    "formula_bullets",
    "sequence_block",
    "draw_note",
    "draw_small_table",
    "system_chain",
    "draw_stem_plot",
    "draw_pipeline",
    "draw_two_col",
    "draw_blue_note",
    "draw_discrete_axes_plot",
    "para_red",
    "draw_unit_circle",
    "draw_stem",
    "draw_curve_pair",
}

# Calls whose string literals are control data, cache keys, paths, report text,
# or other non-page-output values.  They must not be treated as visible labels.
NON_TEXT_CALLS = {
    "Path",
    "compile",
    "draw_panel",
    "draw_unit_and_response",
    "enumerate",
    "_delay_mark",
    "join",
    "replace",
    "rfind",
    "ratio_tex",
    "set",
    "split",
    "sub",
    "truetype",
    "write_text",
}

_ALLOWED_SLASH_TOKENS = (
    "A/D", "D/A", "DFT/IDFT", "DFS/DFT", "IIR/FIR",
    "DFT/FFT", "DIT/DIF", "LP / HP / BP / BS", "LP / BP", "HP / BP",
    "带通/带阻",
)
_MATH_FUNCTION_RE = re.compile(
    r"(?<![A-Za-z])(?:DTFT|IDFT|DFT|DFS|Re|Im|sin|cos|tan|"
    r"[xyzXYZHWRG]|[xXyYhHrR]_[A-Za-z0-9{}]+|[δθωΩτ])\s*\("
)
_SUBSCRIPT_RE = re.compile(r"(?:[A-Za-z]|[α-ωΑ-Ω])_[A-Za-z0-9{]")
_RELATION_RE = re.compile(r"(?:<=|>=|!=|=|<|>|≤|≥|≠|≈|∈|⇒|⇔)")
_SET_RE = re.compile(r"\{[^{}]+(?:,[^{}]+)+\}")
_PDF_RAW_LATEX_RE = re.compile(
    r"(?:\\(?:frac|sum|prod|sqrt|omega|Omega|pi|theta|tau|delta|lambda|"
    r"mathrm|left|right|leq|geq|ne|approx|in|Rightarrow|Leftrightarrow)\b|\^\{)"
)
_PDF_RAW_SUBSCRIPT_RE = re.compile(r"(?:[A-Za-z]|[α-ωΑ-Ω])_[A-Za-z0-9{]")


def classify_plain_text_math(text: str) -> set[str]:
    """Return reasons why *text* contains math that should be rendered."""

    reasons: set[str] = set()
    if "^" in text:
        reasons.add("caret")
    if "\\" in text:
        reasons.add("latex_command")
    if _SUBSCRIPT_RE.search(text):
        reasons.add("subscript")
    if _MATH_FUNCTION_RE.search(text):
        reasons.add("math_function")
    if _RELATION_RE.search(text):
        reasons.add("relation")
    if _SET_RE.search(text):
        reasons.add("set_literal")

    slash_probe = text
    for token in _ALLOWED_SLASH_TOKENS:
        slash_probe = slash_probe.replace(token, "")
    if "/" in slash_probe:
        reasons.add("slash_division")
    return reasons


def classify_pdf_source_text(text: str) -> set[str]:
    """Return strong signs that source notation survived into PDF text."""

    reasons: set[str] = set()
    if _PDF_RAW_LATEX_RE.search(text):
        reasons.add("raw_latex")
    if _PDF_RAW_SUBSCRIPT_RE.search(text):
        reasons.add("raw_subscript")
    slash_probe = text
    for token in _ALLOWED_SLASH_TOKENS:
        slash_probe = slash_probe.replace(token, "")
    slash_probe = re.sub(r"https?://\S+", "", slash_probe)
    if re.search(r"(?:[A-Za-z0-9α-ωΑ-Ω)\]])\s*/\s*(?:[A-Za-z0-9α-ωΑ-Ω(\[])", slash_probe):
        reasons.add("slash_division")
    return reasons


def _call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Attribute):
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return ""


def _string_literals(node: ast.AST):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        yield node.value
        return
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        for child in node.elts:
            yield from _string_literals(child)
    elif isinstance(node, ast.Dict):
        for child in node.values:
            yield from _string_literals(child)


def _rich_text_literals(node: ast.AST):
    if isinstance(node, (ast.Tuple, ast.List)) and len(node.elts) >= 2:
        kind = node.elts[0]
        value = node.elts[1]
        if isinstance(kind, ast.Constant):
            if kind.value == "math":
                return
            if (
                kind.value == "text"
                and isinstance(value, ast.Constant)
                and isinstance(value.value, str)
            ):
                yield value.value
                return
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        yield node.value
        return
    for child in ast.iter_child_nodes(node):
        yield from _rich_text_literals(child)


def _math_literals(node: ast.AST):
    """Yield literal expressions that are sent to a mathematics renderer."""

    if isinstance(node, (ast.Tuple, ast.List)) and len(node.elts) >= 2:
        kind = node.elts[0]
        value = node.elts[1]
        if (
            isinstance(kind, ast.Constant)
            and kind.value == "math"
            and isinstance(value, ast.Constant)
            and isinstance(value.value, str)
        ):
            yield value.value
            return
    for child in ast.iter_child_nodes(node):
        yield from _math_literals(child)


def _auto_rendered_text_literals(node: ast.AST):
    """Yield only text fragments left unrendered by Doc's automatic math parser."""

    from make_dsp_sample_handout_v2 import auto_math_runs

    for text in _string_literals(node):
        for kind, value in auto_math_runs(text):
            if kind == "text":
                yield value


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    call: str
    reasons: tuple[str, ...]
    text: str


def scan_source(path: Path) -> list[Finding]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    findings: list[Finding] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        if name in MATH_RENDER_CALLS or name in NON_TEXT_CALLS:
            continue
        for arg in (*node.args, *(kw.value for kw in node.keywords)):
            if name in RICH_TEXT_CALLS:
                strings = _rich_text_literals(arg)
            elif name in AUTO_RENDER_TEXT_CALLS:
                strings = _auto_rendered_text_literals(arg)
            else:
                strings = _string_literals(arg)
            for text in strings:
                reasons = classify_plain_text_math(text)
                if reasons:
                    findings.append(
                        Finding(
                            path=path,
                            line=getattr(node, "lineno", 0),
                            call=name,
                            reasons=tuple(sorted(reasons)),
                            text=" ".join(text.split()),
                        )
                    )
    return findings


def scan_math_rendering_slashes(path: Path) -> list[Finding]:
    """Find slash notation that would remain a slash after math rendering."""

    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    findings: list[Finding] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        arguments = (*node.args, *(kw.value for kw in node.keywords))
        strings: list[str] = []
        if name in MATH_RENDER_CALLS:
            for arg in arguments:
                strings.extend(_string_literals(arg))
        elif name in RICH_TEXT_CALLS:
            for arg in arguments:
                strings.extend(_math_literals(arg))
        else:
            continue
        for value in strings:
            if "/" not in value:
                continue
            findings.append(
                Finding(
                    path=path,
                    line=getattr(node, "lineno", 0),
                    call=name,
                    reasons=("math_slash_division",),
                    text=" ".join(value.split()),
                )
            )
    return findings


def scan_active_generators(work_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    for filename in ACTIVE_GENERATORS:
        path = work_dir / filename
        if path.exists():
            findings.extend(scan_source(path))
            findings.extend(scan_math_rendering_slashes(path))
    return sorted(findings, key=lambda item: (str(item.path), item.line, item.text))


def scan_pdf_text(path: Path) -> list[Finding]:
    """Scan extractable PDF text for source-like mathematics."""

    from pypdf import PdfReader

    findings: list[Finding] = []
    for page_number, page in enumerate(PdfReader(str(path)).pages, start=1):
        for line in (page.extract_text() or "").splitlines():
            reasons = classify_pdf_source_text(line)
            if reasons:
                findings.append(
                    Finding(
                        path=path,
                        line=page_number,
                        call="pdf_text",
                        reasons=tuple(sorted(reasons)),
                        text=" ".join(line.split()),
                    )
                )
    return findings


def write_markdown_report(findings: list[Finding], output: Path, root: Path) -> None:
    lines = [
        "# Plain-text mathematics audit",
        "",
        f"Findings: **{len(findings)}**",
        "",
        "| File | Line | Call | Reasons | Text |",
        "|---|---:|---|---|---|",
    ]
    for item in findings:
        try:
            shown_path = item.path.relative_to(root)
        except ValueError:
            shown_path = item.path
        text = item.text.replace("|", "\\|").replace("`", "\\`")
        lines.append(
            f"| `{shown_path}` | {item.line} | `{item.call}` | "
            f"{', '.join(item.reasons)} | `{text}` |"
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pdf", type=Path, action="append", default=[])
    args = parser.parse_args()
    findings = scan_active_generators(args.work_dir)
    for pdf_path in args.pdf:
        findings.extend(scan_pdf_text(pdf_path))
    if args.output:
        write_markdown_report(findings, args.output, args.work_dir.parent)
    print(f"plain-text math findings: {len(findings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
