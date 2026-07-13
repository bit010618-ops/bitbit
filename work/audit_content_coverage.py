from __future__ import annotations

import argparse
import json
import re
from difflib import SequenceMatcher
from pathlib import Path

import pdfplumber


NOISE_RE = re.compile(r"[\s\u3000]+")
PUNCT_RE = re.compile(r"[，。；：、！？,.!?;:·•]+")


def normalize_text(text: str) -> str:
    text = NOISE_RE.sub("", text or "").lower()
    return PUNCT_RE.sub("", text)


def coverage_ratio(source: str, handout: str) -> float:
    source_norm = normalize_text(source)
    handout_norm = normalize_text(handout)
    if not source_norm:
        return 0.0
    blocks = SequenceMatcher(None, source_norm, handout_norm, autojunk=False).get_matching_blocks()
    return sum(block.size for block in blocks) / len(source_norm)


def missing_fragments(source: str, handout: str, window: int = 18) -> list[str]:
    source_norm = normalize_text(source)
    handout_norm = normalize_text(handout)
    if not source_norm or window <= 0:
        return []
    missing: list[str] = []
    stride = max(1, window // 2)
    for start in range(0, max(1, len(source_norm) - window + 1), stride):
        fragment = source_norm[start : start + window]
        if len(fragment) < window // 2 or fragment in handout_norm:
            continue
        if missing and fragment[: stride] in missing[-1]:
            missing[-1] += fragment[stride:]
        else:
            missing.append(fragment)
    return missing


def extract_pages(path: Path, first: int = 1, last: int | None = None) -> list[str]:
    with pdfplumber.open(path) as pdf:
        stop = min(last or len(pdf.pages), len(pdf.pages))
        return [(pdf.pages[index].extract_text() or "") for index in range(first - 1, stop)]


def audit(source_pdf: Path, handout_pdf: Path, first: int, last: int) -> dict:
    source_pages = extract_pages(source_pdf, first, last)
    handout_text = "\n".join(extract_pages(handout_pdf))
    rows = []
    for page_number, source_text in enumerate(source_pages, first):
        source_chars = len(normalize_text(source_text))
        rows.append(
            {
                "source_page": page_number,
                "source_chars": source_chars,
                "status": "text-audited" if source_chars else "visual-audit-required",
                "coverage": round(coverage_ratio(source_text, handout_text), 4),
                "missing": missing_fragments(source_text, handout_text)[:12],
            }
        )
    return {
        "source": str(source_pdf),
        "handout": str(handout_pdf),
        "range": [first, last],
        "pages": rows,
        "mean_coverage": round(sum(row["coverage"] for row in rows) / max(1, len(rows)), 4),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_pdf", type=Path)
    parser.add_argument("handout_pdf", type=Path)
    parser.add_argument("--first", type=int, required=True)
    parser.add_argument("--last", type=int, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.source_pdf, args.handout_pdf, args.first, args.last)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
