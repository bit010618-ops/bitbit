from argparse import ArgumentParser
from pathlib import Path

from pdf2image import convert_from_path, pdfinfo_from_path
from PIL import Image, ImageDraw, ImageFont


POPPLER = str(Path(
    r"C:\Users\HP\.cache\codex-runtimes\codex-primary-runtime"
    r"\dependencies\native\poppler\Library\bin"
))


def build_contacts(pdf_paths, output_dir, dpi=80, cols=4, rows=3):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    slots = cols * rows
    created = []

    for batch_index, pdf_path in enumerate(map(Path, pdf_paths), start=1):
        page_count = int(pdfinfo_from_path(pdf_path, poppler_path=POPPLER)["Pages"])
        for start in range(1, page_count + 1, slots):
            end = min(page_count, start + slots - 1)
            pages = convert_from_path(
                pdf_path,
                dpi=dpi,
                first_page=start,
                last_page=end,
                poppler_path=POPPLER,
                fmt="png",
                thread_count=2,
            )
            thumb_w = 300
            thumb_h = round(pages[0].height * thumb_w / pages[0].width)
            label_h = 24
            gap = 10
            sheet = Image.new(
                "RGB",
                (gap + cols * (thumb_w + gap), gap + rows * (thumb_h + label_h + gap)),
                "#d9dde2",
            )
            draw = ImageDraw.Draw(sheet)
            for offset, page in enumerate(pages):
                row, col = divmod(offset, cols)
                x = gap + col * (thumb_w + gap)
                y = gap + row * (thumb_h + label_h + gap)
                thumb = page.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                sheet.paste(thumb, (x, y))
                draw.rectangle((x, y + thumb_h, x + thumb_w, y + thumb_h + label_h), fill="white")
                draw.text(
                    (x + 6, y + thumb_h + 6),
                    f"batch {batch_index} / page {start + offset}",
                    fill="black",
                    font=font,
                )
            target = output_dir / f"batch-{batch_index:02d}_{start:02d}-{end:02d}.jpg"
            sheet.save(target, quality=92)
            created.append(target)
    return created


def main():
    parser = ArgumentParser()
    parser.add_argument("output_dir")
    parser.add_argument("pdfs", nargs="+")
    parser.add_argument("--dpi", type=int, default=80)
    args = parser.parse_args()
    created = build_contacts(args.pdfs, args.output_dir, dpi=args.dpi)
    print(f"created {len(created)} contact sheets")


if __name__ == "__main__":
    main()
