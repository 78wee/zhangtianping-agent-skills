---
name: print-reading-handout
description: Create stable, print-ready A4 reading handouts from selected text, Markdown, pasted prose, or formula-heavy PDFs/screenshots, especially Chinese student feedback,作文批改, teaching notes, AI exam grading exports, tables, quoted examples, and other content the user asks to “打印”, “整理成阅读模式”, “转换成正常阅读模式”, “截图方式打印”, “保留原格式”, “打印出来”, or send through the macOS local/default printer. Use when the user selects this skill for current selected text, or when print quality, pagination, Chinese typography, formula preservation, and repeatable PDF/image-to-CUPS printing matter.
---

# Print Reading Handout

## Workflow

Use this skill when the user wants pasted content, a local text/Markdown file, screenshots, or a PDF formatted as a readable handout and printed through macOS.

Fastest interaction: if the user selected text and invoked this skill with a short command like “打印” or the default skill prompt, treat the selected text as the source content, format it as an A4 handout, and print to the default macOS printer without asking follow-up questions unless the selected content is missing or the printer is unavailable.

Choose the source mode first:

- **Text/Markdown mode**: Use for prose-only material where cleaner typography is more important than preserving exact visual layout.
- **Original-format/screenshot mode**: Prefer this for Gemini/AI exported PDFs, scanned pages, math/physics/chemistry content, formulas, diagrams, handwritten annotations, or whenever the user says “截图方式”, “保留原格式”, or reports that formulas became unreadable. Do not extract and reflow the text in this mode; preserve each source page/screenshot visually and print it fit-to-A4.

1. Create a UTF-8 Markdown/text source file in the current workspace. Clean obvious Markdown artifacts if helpful, but preserve the user's meaning.
2. Run `scripts/make_handout.py` to generate a stable A4 HTML file and PDF using a fixed Chinese-friendly stylesheet.
3. If the user asked to print, pass `--print`; the script sends the PDF to CUPS with `lp -o media=A4 -o fit-to-page`.
4. Check the script output and optionally `file <pdf>` or `lpstat -p -d` / `lpstat -W not-completed -o <printer>` to verify generation and queue status.
5. Tell the user the PDF path, page count if checked, printer/job id if printed, and any print error.

For original-format/screenshot mode, print the existing PDF directly if it is already an A4-friendly export:

```bash
lp -o media=A4 -o fit-to-page "input.pdf"
```

If the source is screenshots/images or the PDF pages need to be wrapped into a new user-facing artifact, create an A4 PDF with one preserved image/page per sheet, then print that PDF with CUPS. Keep the source visual content intact; only add margins, page fitting, and an optional short title page if the user requests it.

## Commands

Generate only:

```bash
python3 "$HOME/.agents/skills/print-reading-handout/scripts/make_handout.py" input.md --title "讲义标题" --out-dir .
```

Generate and print to the default macOS printer:

```bash
python3 "$HOME/.agents/skills/print-reading-handout/scripts/make_handout.py" input.md --title "讲义标题" --out-dir . --print
```

Print to a named printer:

```bash
python3 "$HOME/.agents/skills/print-reading-handout/scripts/make_handout.py" input.md --title "讲义标题" --out-dir . --print --printer PRINTER_NAME
```

## Formatting Rules

- Prefer A4, 18mm x 16mm margins, Chinese serif/sans fallback fonts, 13.2pt body text, and high-contrast restrained colors.
- Preserve headings, ordered lists, unordered lists, blockquotes, and simple Markdown tables.
- For formula-heavy Gemini/AI exports, prefer original-format/screenshot mode over text cleanup so fractions, roots, diagrams, and tables remain readable.
- For student-facing作文批改, soften labels such as “直接可抄” to “可参考仿写” and “万能句式” to “常用句式” when appropriate.
- Use a short, descriptive basename such as `蓄力与绽放作文批改学生版`; avoid overwriting unrelated previous handouts.
- Use `---` in the source as an intentional page break when needed.

## Dependencies

The script expects:

- `python3`
- a Chromium-based browser, preferably `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`, for deterministic HTML-to-PDF rendering
- macOS CUPS `lp` for printing

If Chrome is missing, use another Chromium-based browser supported by the script or fall back to manually creating HTML/PDF with the same CSS and printing the resulting PDF.
