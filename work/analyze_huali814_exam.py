from collections import Counter
from pathlib import Path
import re

from pypdf import PdfReader


SOURCE = Path(r"C:\Users\HP\Desktop\讲义、做题本\华理814真题.pdf")
OUT_TEXT = Path("work/huali814_exam_text.txt")
OUT_REPORT = Path("work/huali814_exam_focus_report.md")

KEYWORDS = [
    "采样", "抽样", "量化", "编码", "A/D", "D/A", "模拟信号", "数字信号",
    "离散", "序列", "差分方程", "系统函数", "单位冲激", "卷积", "傅里叶",
    "z变换", "拉普拉斯", "DFT", "FFT", "滤波器", "频率响应", "稳定",
    "因果", "极点", "零点", "冲激响应", "系统框图",
]


def clean_text(text: str) -> str:
    text = text.encode("utf-8", "replace").decode("utf-8")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main() -> None:
    reader = PdfReader(str(SOURCE))
    pages = []
    for idx, page in enumerate(reader.pages, start=1):
        text = clean_text(page.extract_text() or "")
        pages.append((idx, text))

    OUT_TEXT.write_text(
        "\n\n".join(f"--- PAGE {idx} ---\n{text}" for idx, text in pages),
        encoding="utf-8",
    )

    counts = Counter()
    examples = {kw: [] for kw in KEYWORDS}
    for idx, text in pages:
        compact = text.replace("\n", " ")
        for kw in KEYWORDS:
            n = compact.count(kw)
            if n:
                counts[kw] += n
                if len(examples[kw]) < 5:
                    pos = compact.find(kw)
                    start = max(0, pos - 80)
                    end = min(len(compact), pos + 140)
                    examples[kw].append((idx, compact[start:end]))

    lines = ["# 华理814真题考点轻量索引", ""]
    lines.append(f"- Pages: {len(reader.pages)}")
    lines.append("")
    lines.append("## Keyword Counts")
    for kw, count in counts.most_common():
        lines.append(f"- {kw}: {count}")
    lines.append("")
    lines.append("## Examples")
    for kw, count in counts.most_common():
        lines.append(f"### {kw} ({count})")
        for page, snippet in examples[kw]:
            lines.append(f"- p.{page}: {snippet}")
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT_REPORT)
    print(OUT_TEXT)


if __name__ == "__main__":
    main()
