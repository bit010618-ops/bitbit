from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


INPUT_DIR = Path("tmp/pdfs/source_046_114_contacts")
OUTPUT_DIR = INPUT_DIR / "contacts"
COLS = 4
ROWS = 3
THUMB_W = 360
LABEL_H = 28
GAP = 12


def page_number(path: Path) -> int:
    return int(path.stem.rsplit("-", 1)[-1])


def main() -> None:
    pages = sorted(INPUT_DIR.glob("page-*.png"), key=page_number)
    if not pages:
        raise SystemExit(f"No rendered pages found in {INPUT_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with Image.open(pages[0]) as first:
        thumb_h = round(first.height * THUMB_W / first.width)

    sheet_w = GAP + COLS * (THUMB_W + GAP)
    sheet_h = GAP + ROWS * (thumb_h + LABEL_H + GAP)
    font = ImageFont.load_default()

    batch_size = COLS * ROWS
    for offset in range(0, len(pages), batch_size):
        batch = pages[offset : offset + batch_size]
        sheet = Image.new("RGB", (sheet_w, sheet_h), "#d9dde2")
        draw = ImageDraw.Draw(sheet)
        for index, path in enumerate(batch):
            row, col = divmod(index, COLS)
            x = GAP + col * (THUMB_W + GAP)
            y = GAP + row * (thumb_h + LABEL_H + GAP)
            with Image.open(path) as page:
                thumb = page.convert("RGB").resize((THUMB_W, thumb_h), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x, y))
            number = page_number(path)
            draw.rectangle((x, y + thumb_h, x + THUMB_W, y + thumb_h + LABEL_H), fill="white")
            draw.text((x + 8, y + thumb_h + 7), f"PDF page {number}", fill="black", font=font)

        start = page_number(batch[0])
        end = page_number(batch[-1])
        sheet.save(OUTPUT_DIR / f"contact_{start:02d}_{end:02d}.jpg", quality=92)


if __name__ == "__main__":
    main()
