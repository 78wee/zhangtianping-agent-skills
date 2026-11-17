#!/usr/bin/env python3
"""Create a stable A4 reading handout from Markdown/plain text and optionally print it."""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


CSS = r"""
@page {
  size: A4;
  margin: 18mm 16mm;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  color: #1f2933;
  background: #fff;
  font-family: "PingFang SC", "Songti SC", "STSong", "Noto Serif CJK SC", serif;
  font-size: 13.2pt;
  line-height: 1.72;
}

main {
  max-width: 780px;
  margin: 0 auto;
}

h1,
h2,
h3,
h4 {
  margin: 0;
  color: #111827;
  line-height: 1.35;
  break-after: avoid;
}

h1 {
  padding-bottom: 10px;
  border-bottom: 2px solid #111827;
  font-size: 21pt;
  text-align: center;
  letter-spacing: 0;
}

h2 {
  margin-top: 22px;
  padding: 7px 10px;
  border-left: 5px solid #2f5d7c;
  background: #eef5f8;
  font-size: 16.5pt;
}

h3 {
  margin-top: 16px;
  font-size: 14.3pt;
}

h4 {
  margin-top: 12px;
  font-size: 13.6pt;
}

p {
  margin: 8px 0;
  text-align: justify;
}

ul,
ol {
  margin: 8px 0 8px 24px;
  padding: 0;
}

li {
  margin: 5px 0;
}

blockquote {
  margin: 10px 0;
  padding: 10px 13px;
  border-left: 4px solid #708090;
  background: #fbfbfc;
}

table {
  width: 100%;
  margin: 12px 0;
  border-collapse: collapse;
  font-size: 11pt;
  line-height: 1.5;
}

th,
td {
  padding: 8px 9px;
  border: 1px solid #b8c2cc;
  vertical-align: top;
  text-align: left;
}

th {
  background: #e7edf3;
  font-weight: 700;
}

tr {
  break-inside: avoid;
}

.score,
.note {
  margin: 10px 0;
  padding: 10px 13px;
  border: 1px solid #d7dce2;
  background: #fbfbfc;
}

.score {
  border-color: #d9bd65;
  background: #fff8dc;
  font-weight: 700;
  font-size: 15pt;
}

.page-break {
  break-before: page;
}

@media print {
  body {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}
"""


def slugify(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|]+", "", value).strip()
    return value or "reading-handout"


def inline_markup(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = text.replace(" -&gt; ", " → ")
    text = text.replace("\\rightarrow", "→")
    return text


def is_ordered_item(line: str) -> re.Match[str] | None:
    return re.match(r"^\s*(\d+)[.)、]\s+(.+)$", line)


def is_unordered_item(line: str) -> re.Match[str] | None:
    return re.match(r"^\s*[-*]\s+(.+)$", line)


def flush_paragraph(parts: list[str], out: list[str]) -> None:
    if parts:
        out.append(f"<p>{inline_markup(' '.join(parts))}</p>")
        parts.clear()


def flush_list(list_type: str | None, out: list[str]) -> None:
    if list_type:
        out.append(f"</{list_type}>")


def markdown_to_html(markdown: str, title: str) -> str:
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None
    table_rows: list[list[str]] = []

    def flush_table() -> None:
        nonlocal table_rows
        if not table_rows:
            return
        out.append("<table>")
        for index, row in enumerate(table_rows):
            tag = "th" if index == 0 else "td"
            cells = "".join(f"<{tag}>{inline_markup(cell.strip())}</{tag}>" for cell in row)
            out.append(f"<tr>{cells}</tr>")
        out.append("</table>")
        table_rows = []

    out.append(f"<h1>{inline_markup(title)}</h1>")

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph(paragraph, out)
            flush_list(list_type, out)
            list_type = None
            flush_table()
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph(paragraph, out)
            flush_list(list_type, out)
            list_type = None
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
                continue
            table_rows.append(cells)
            continue
        flush_table()

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph(paragraph, out)
            flush_list(list_type, out)
            list_type = None
            level = len(heading.group(1))
            if level == 1 and not out[1:]:
                continue
            out.append(f"<h{level}>{inline_markup(heading.group(2))}</h{level}>")
            continue

        if stripped == "---":
            flush_paragraph(paragraph, out)
            flush_list(list_type, out)
            list_type = None
            out.append('<div class="page-break"></div>')
            continue

        quote = re.match(r"^>\s?(.+)$", stripped)
        if quote:
            flush_paragraph(paragraph, out)
            flush_list(list_type, out)
            list_type = None
            out.append(f"<blockquote><p>{inline_markup(quote.group(1))}</p></blockquote>")
            continue

        ordered = is_ordered_item(stripped)
        unordered = is_unordered_item(stripped)
        if ordered or unordered:
            flush_paragraph(paragraph, out)
            needed = "ol" if ordered else "ul"
            if list_type != needed:
                flush_list(list_type, out)
                out.append(f"<{needed}>")
                list_type = needed
            item = ordered.group(2) if ordered else unordered.group(1)
            out.append(f"<li>{inline_markup(item)}</li>")
            continue

        flush_list(list_type, out)
        list_type = None
        paragraph.append(stripped)

    flush_paragraph(paragraph, out)
    flush_list(list_type, out)
    flush_table()
    return "\n".join(out)


def find_chrome() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    for binary in ("google-chrome", "chromium", "chromium-browser", "msedge"):
        found = shutil.which(binary)
        if found:
            return found
    raise RuntimeError("No Chromium-based browser found for stable HTML-to-PDF rendering.")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, capture_output=True)


def render_pdf(html_path: Path, pdf_path: Path) -> None:
    chrome = find_chrome()
    run([
        chrome,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ])
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"PDF was not created correctly: {pdf_path}")


def print_pdf(pdf_path: Path, printer: str | None) -> str:
    command = ["lp"]
    if printer:
        command.extend(["-d", printer])
    command.extend(["-o", "media=A4", "-o", "fit-to-page", str(pdf_path)])
    result = run(command)
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Markdown or plain-text input file.")
    parser.add_argument("--title", help="Document title. Defaults to first H1 or filename.")
    parser.add_argument("--out-dir", type=Path, default=Path.cwd(), help="Output directory.")
    parser.add_argument("--basename", help="Output basename without extension.")
    parser.add_argument("--print", action="store_true", help="Send generated PDF to macOS CUPS via lp.")
    parser.add_argument("--printer", help="Printer name. Defaults to the system default destination.")
    args = parser.parse_args()

    source = args.input.read_text(encoding="utf-8")
    first_h1 = re.search(r"^#\s+(.+)$", source, flags=re.MULTILINE)
    title = args.title or (first_h1.group(1).strip() if first_h1 else args.input.stem)
    basename = slugify(args.basename or title)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    body_html = markdown_to_html(source, title)
    html_path = args.out_dir / f"{basename}.html"
    pdf_path = args.out_dir / f"{basename}.pdf"
    html_doc = (
        "<!doctype html>\n<html lang=\"zh-CN\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        f"<title>{inline_markup(title)}</title>\n"
        f"<style>{CSS}</style>\n"
        "</head>\n<body>\n<main>\n"
        f"{body_html}\n"
        "</main>\n</body>\n</html>\n"
    )
    html_path.write_text(html_doc, encoding="utf-8")
    render_pdf(html_path, pdf_path)

    print(f"HTML: {html_path}")
    print(f"PDF: {pdf_path}")
    if args.print:
        print(print_pdf(pdf_path, args.printer))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr or exc.stdout or str(exc))
        raise SystemExit(exc.returncode)
    except Exception as exc:
        sys.stderr.write(f"{exc}\n")
        raise SystemExit(1)
