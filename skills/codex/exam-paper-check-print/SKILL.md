---
name: exam-paper-check-print
description: Analyze scanned middle-school exam papers or weekend homework PDFs, especially Chinese 初三/中考 math, physics, chemistry, or English papers. Use when Codex needs to OCR a ScanSnap/scanned PDF, split booklet/spread pages, check all questions, connect them to local exam points such as 福建初三/中考考点, produce a Markdown/PDF handout, and optionally print it through macOS.
---

# Exam Paper Check Print

## Workflow

Use this skill for requests like “检查这份试卷”, “结合福建省初三考点分析”, “这个也需要”, or “整理成可以打印的讲义” when a scanned PDF or image-based paper is provided.

1. Inspect the PDF: verify file path, page count, text layer, image count, and whether pages are single pages or two-page spreads. In Codex desktop, call `load_workspace_dependencies` first if you need bundled Python/PDF/image libraries.
2. Extract and split pages with `scripts/extract_split_pdf.py`. Use the bundled workspace Python when system `python3` lacks `Pillow` or `pypdf`. Use `--layout auto` first; if page order is wrong, rerun with explicit ordering or manually rename/crop.
3. OCR the split page images with `scripts/vision_ocr.swift` on macOS. Treat OCR as a draft only, especially for math formulas, diagrams, and handwritten notes.
4. Visually inspect page images and crop hard questions when needed. Use `view_image` for formula-heavy, diagram-heavy, or OCR-uncertain questions.
5. Analyze the paper:
   - Identify subject, title, page order, score structure, and question numbers.
   - Give answer keys or solution points where reliable.
   - Mark any illegible, cropped, or ambiguous formulas explicitly instead of guessing.
   - Connect every section or important question type to 初三/中考考点.
   - Call out visible wrong answers or incomplete work if handwriting is present.
6. Save a Markdown report in the workspace `outputs/` directory using a clear basename such as `数学周末作业_5月31日_检查分析.md`.
7. If the user wants printing or says “也需要” after prior printed reports, use `$print-reading-handout` or its script to generate A4 HTML/PDF and print to the default macOS printer.
8. Verify generation and print status with page count and `lpstat`; report the PDF path, page count, and print job id.

## Report Shape

Prefer this structure:

- Title and short note about source/scan limitations.
- Overall judgement: paper type, difficulty, and local exam alignment.
- Answer/check table for objective questions.
- Section-by-section analysis for fill-in, proof, experiment, calculation, or essay questions.
- Visible correction list.
- Local exam preparation advice.
- Source note: mention relevant curriculum standard when used.

Keep the report honest: if OCR or image quality prevents certainty, write “需看原卷确认” and explain what is unclear.

## Subject Guidance

- Math: visually verify formulas and geometry diagrams; OCR is unreliable for fractions, exponents, roots, and inequalities. Emphasize algebra basics, functions, statistics/probability, geometry proof, circle, similarity, and real-world modeling.
- Physics: verify circuit diagrams, graph axes, units, and handwritten calculations. Emphasize concept choice, experiments, graph reading, mechanics, optics, electricity, and standard formula steps.
- Chemistry: verify chemical formulas, equation coefficients, tables, and lab diagrams. Emphasize substances/changes, elements, acids-bases-salts, experiments, processes, calculations, and evidence language.
- English: if grading essays, use the dedicated English grading skill when applicable; otherwise analyze reading, grammar, writing requirements, and exam skills.

## Useful Commands

Extract and split:

```bash
python3 "$HOME/.agents/skills/exam-paper-check-print/scripts/extract_split_pdf.py" \
  input.pdf --out-dir work/exam_pages --layout auto
```

OCR:

```bash
swift "$HOME/.agents/skills/exam-paper-check-print/scripts/vision_ocr.swift" work/exam_pages/ocr.txt work/exam_pages/pages/*.png
```

Generate and print a handout:

```bash
python3 "$HOME/.agents/skills/print-reading-handout/scripts/make_handout.py" outputs/report.md --title "试卷检查分析" --out-dir outputs --print
```

Check print queue and page count:

```bash
lpstat -p -d
lpstat -W not-completed -o PRINTER_NAME
python3 - <<'PY'
from pypdf import PdfReader
print(len(PdfReader("outputs/report.pdf").pages))
PY
```
