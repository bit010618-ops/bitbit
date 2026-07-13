# DSP Handout Sample Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a polished A4 portrait PDF sample from the first 15 pages of the DSP courseware.

**Architecture:** Render the original pages for visual reference, manually reconstruct the selected content in a structured Python data model, draw clean diagrams with ReportLab vector primitives, and export a verified PDF plus a separate proofreading record. The handout uses textbook-style layout with sparse key-point notes driven by HuaLi 814 past-paper patterns.

**Tech Stack:** Python, ReportLab, pypdf, Poppler `pdftoppm`/`pdfinfo`, local Windows fonts.

---

### Task 1: Source Review

**Files:**
- Read: `work/pdfs/source_pages/src15-001.png` through `src15-015.png`
- Read: `work/huali814_exam_focus_report.md`

- [ ] Inspect first 15 rendered source pages and identify section titles, diagrams, and formulas.
- [ ] Extract HuaLi 814 sampling-related emphasis from the generated report.
- [ ] Decide which source diagrams can be redrawn as vector figures.

### Task 2: Build PDF Generator

**Files:**
- Create: `work/make_dsp_sample_handout.py`
- Create: `outputs/DSP讲义重制_样章_校对记录.md`
- Output: `outputs/DSP讲义重制_样章_前15页.pdf`

- [ ] Register Chinese fonts from Windows font files.
- [ ] Implement A4 portrait page template with header, footer, section titles, body text, sparse key-point notes, figure captions, and vector diagrams.
- [ ] Encode the first 15 pages of source content as structured handout sections.
- [ ] Add HuaLi 814-oriented notes only where directly relevant, especially sampling, Nyquist recovery, aliasing, and A/D-D/A roles.
- [ ] Generate the sample PDF.

### Task 3: Verify Output

**Files:**
- Read: `outputs/DSP讲义重制_样章_前15页.pdf`
- Create: `work/pdfs/sample_handout_preview/*.png`

- [ ] Run `pdfinfo` to confirm A4 portrait output and page count.
- [ ] Render the generated PDF to PNG.
- [ ] Inspect representative rendered pages for clipped text, bad glyphs, crowded layout, and visible unwanted watermark.
- [ ] If defects are found, adjust `work/make_dsp_sample_handout.py` and regenerate.

### Task 4: Final Delivery

**Files:**
- Deliver: `outputs/DSP讲义重制_样章_前15页.pdf`
- Deliver: `outputs/DSP讲义重制_样章_校对记录.md`

- [ ] Summarize what was generated.
- [ ] Mention any known limitations or places needing user review.
