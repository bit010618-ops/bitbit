from pathlib import Path

from pypdf import PdfReader, PdfWriter


INPUT = Path(r"C:\Users\HP\Documents\Codex\2026-07-01\zh\outputs\DSP课件_A4讲义版.pdf")
OUT_DIR = Path(r"C:\Users\HP\Documents\Codex\2026-07-01\zh\outputs")
CHUNK_SIZE = 50


def main() -> None:
    reader = PdfReader(str(INPUT))
    total = len(reader.pages)
    for start in range(0, total, CHUNK_SIZE):
        end = min(start + CHUNK_SIZE, total)
        writer = PdfWriter()
        for index in range(start, end):
            writer.add_page(reader.pages[index])
        writer.add_metadata({
            "/Title": f"DSP handout pages {start + 1}-{end}",
            "/Producer": "pypdf",
        })
        out_path = OUT_DIR / f"DSP课件_A4讲义版_分册{start // CHUNK_SIZE + 1:02d}_页{start + 1:03d}-{end:03d}.pdf"
        with out_path.open("wb") as f:
            writer.write(f)
        print(out_path)


if __name__ == "__main__":
    main()
