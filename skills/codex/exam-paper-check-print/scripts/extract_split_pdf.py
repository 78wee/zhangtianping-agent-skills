#!/usr/bin/env python3
"""Extract images from a scanned PDF and split landscape spreads into pages."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
    from pypdf import PdfReader
except ModuleNotFoundError as exc:
    sys.exit(
        f"Missing dependency: {exc.name}. In Codex desktop, call load_workspace_dependencies "
        "and run this script with the bundled Python executable documented by your agent client."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="Scanned PDF path")
    parser.add_argument("--out-dir", default="work/exam_pages", help="Output directory")
    parser.add_argument(
        "--layout",
        choices=["auto", "single", "spread"],
        default="auto",
        help="Split mode. auto splits landscape images only.",
    )
    parser.add_argument("--overlap", type=int, default=60, help="Center overlap for spreads")
    parser.add_argument("--margin", type=int, default=60, help="White margin added to pages")
    args = parser.parse_args()

    pdf = Path(args.pdf).expanduser()
    out_dir = Path(args.out_dir)
    image_dir = out_dir / "images"
    page_dir = out_dir / "pages"
    image_dir.mkdir(parents=True, exist_ok=True)
    page_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(pdf))
    print(f"PDF: {pdf}")
    print(f"PDF pages: {len(reader.pages)}")

    page_index = 1
    for pdf_index, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        print(
            f"source page {pdf_index}: text_chars={len(text)} images={len(page.images)} "
            f"mediabox={float(page.mediabox.width):.1f}x{float(page.mediabox.height):.1f}"
        )
        for image_index, image in enumerate(page.images, 1):
            suffix = Path(image.name).suffix or ".img"
            image_path = image_dir / f"pdf{pdf_index:02d}_{image_index}{suffix}"
            image_path.write_bytes(image.data)
            img = Image.open(image_path).convert("L")
            w, h = img.size
            print(f"  image {image_path.name}: {w}x{h}")

            split = args.layout == "spread" or (args.layout == "auto" and w > h * 1.2)
            if split:
                mid = w // 2
                boxes = [
                    (0, 0, min(w, mid + args.overlap), h),
                    (max(0, mid - args.overlap), 0, w, h),
                ]
                for side, box in zip(["L", "R"], boxes):
                    crop = ImageOps.expand(img.crop(box), border=args.margin, fill=255)
                    out = page_dir / f"p{page_index:02d}_{side}.png"
                    crop.save(out)
                    print(f"    page {page_index:02d}_{side}: {crop.size[0]}x{crop.size[1]} {out}")
                    page_index += 1
            else:
                crop = ImageOps.expand(img, border=args.margin, fill=255)
                out = page_dir / f"p{page_index:02d}.png"
                crop.save(out)
                print(f"    page {page_index:02d}: {crop.size[0]}x{crop.size[1]} {out}")
                page_index += 1

    print(f"page images: {page_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
