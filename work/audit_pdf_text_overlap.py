from __future__ import annotations

import argparse
from pathlib import Path

import pdfplumber


LINE_TOLERANCE = 2.5
MIN_VERTICAL_OVERLAP = 0.6
MIN_HORIZONTAL_OVERLAP = 10.0


def _lines(words):
    lines = []
    for word in sorted(words, key=lambda item: (item["bottom"], item["x0"])):
        line = next(
            (
                candidate
                for candidate in lines
                if abs(candidate["bottom"] - word["bottom"]) <= LINE_TOLERANCE
            ),
            None,
        )
        if line is None:
            line = {
                "words": [],
                "x0": word["x0"],
                "x1": word["x1"],
                "top": word["top"],
                "bottom": word["bottom"],
            }
            lines.append(line)
        line["words"].append(word)
        line["x0"] = min(line["x0"], word["x0"])
        line["x1"] = max(line["x1"], word["x1"])
        line["top"] = min(line["top"], word["top"])
        line["bottom"] = max(line["bottom"], word["bottom"])
    for line in lines:
        line["text"] = " ".join(
            word["text"] for word in sorted(line["words"], key=lambda item: item["x0"])
        )
    return sorted(lines, key=lambda item: item["top"])


def _overlap_amount(first, second):
    vertical = min(first["bottom"], second["bottom"]) - max(first["top"], second["top"])
    horizontal = min(first["x1"], second["x1"]) - max(first["x0"], second["x0"])
    return vertical, horizontal


def find_text_overlaps(path):
    findings = []
    with pdfplumber.open(path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            lines = _lines(page.extract_words(use_text_flow=False, keep_blank_chars=False))
            for index, first in enumerate(lines):
                for second in lines[index + 1 :]:
                    if second["top"] >= first["bottom"]:
                        break
                    vertical, horizontal = _overlap_amount(first, second)
                    if vertical < MIN_VERTICAL_OVERLAP or horizontal < MIN_HORIZONTAL_OVERLAP:
                        continue
                    findings.append(
                        {
                            "page": page_number,
                            "vertical_overlap": round(vertical, 2),
                            "horizontal_overlap": round(horizontal, 2),
                            "first": first["text"],
                            "second": second["text"],
                            "bbox": (
                                round(min(first["x0"], second["x0"]), 2),
                                round(min(first["top"], second["top"]), 2),
                                round(max(first["x1"], second["x1"]), 2),
                                round(max(first["bottom"], second["bottom"]), 2),
                            ),
                        }
                    )
    return findings


def write_report(paths, report_path):
    rows = ["# Full-book text-overlap audit", ""]
    total = 0
    for path in paths:
        findings = find_text_overlaps(path)
        total += len(findings)
        rows.extend([f"## {Path(path).name}", "", f"Findings: {len(findings)}", ""])
        for finding in findings:
            rows.append(
                f"- Page {finding['page']}, overlap {finding['vertical_overlap']} pt: "
                f"`{finding['first']}` / `{finding['second']}`"
            )
        rows.append("")
    rows.insert(2, f"Total findings: {total}")
    Path(report_path).write_text("\n".join(rows), encoding="utf-8")
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", nargs="+")
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    total = write_report(args.pdf, args.report)
    print(f"findings={total}")


if __name__ == "__main__":
    main()
