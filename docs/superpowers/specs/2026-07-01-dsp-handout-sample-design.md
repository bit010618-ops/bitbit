# DSP Handout Redesign Sample - Design Spec

## Goal

Create a polished A4 portrait handout sample from the first 15 pages of the DSP courseware. The sample validates the redesign workflow before converting the full courseware.

## Source And Scope

- Source file: `C:\Users\HP\Desktop\DPS课件\DSP课件.pdf`
- Exam reference: `C:\Users\HP\Desktop\讲义、做题本\华理814真题.pdf`
- Sample range: first 15 PPT/PDF pages
- Output PDF: `outputs/DSP讲义重制_样章_前15页.pdf`
- Separate proofreading record: `outputs/DSP讲义重制_样章_校对记录.md`

The source PDF has no usable text layer, so the sample will be rebuilt from rendered page images plus manual/OCR-assisted transcription.

## Final Visual Direction

Use the refined selected direction:

- Main style: B, textbook-style handout.
- Add from A only where helpful: slightly more visible key-point emphasis.
- Do not put examples/exercises in heavy bordered boxes by default.
- Do not include routine "易错提醒" modules by default.
- Do not use visible correction-note boxes inside the handout body.
- Add exam-oriented reminders only when supported by the HuaLi 814 past-paper reference.

## Layout Rules

- A4 portrait pages.
- Clean white background.
- Blue section hierarchy.
- Two-column layouts when text and diagrams benefit from side-by-side reading.
- Header left: `DSP 基础讲义`.
- Header right: current chapter or section name.
- Footer center: page number.
- Body text: readable handout size, not PPT-scale display text.
- Key points: light blue callout boxes, used sparingly.
- Examples/exercises: normal subsection text with clear numbering, not large boxed blocks.
- Exam-oriented reminders: only include when tied to repeated HuaLi 814 question patterns; blend them into the explanation or use a small inline note, not a fixed "易错提醒" module.
- Figures: captioned as `图 1-x`.
- Original PPT watermark and decorative background should be removed or strongly weakened.

## Content Treatment

- Keep the subject matter and order of the original PPT content.
- Rewrite PPT bullet language into continuous handout language when needed.
- Preserve formulas and technical definitions carefully.
- Redraw simple diagrams and flowcharts where feasible.
- For complex or low-quality source diagrams, use cleaned cropped figures.
- Do not add visible "校对备注" callouts to the handout pages.
- Do not add routine "易错提醒" blocks unless the source content clearly needs one.
- For sample pages around 1.1-1.2, prioritize HuaLi 814-linked reminders about sampling, Nyquist recovery, aliasing, A/D and D/A roles, and digital-vs-analog frequency mapping.

## Error Correction Policy

- Fix obvious typos, inconsistent symbols, mismatched numbering, and grammar issues directly.
- Standardize common DSP notation, for example `x[n]` for discrete sequences and `x(t)` for continuous-time signals.
- Do not silently invent uncertain technical corrections.
- Record uncertain or nontrivial edits only in the separate proofreading record, not inside the handout PDF.

## Exam Reference Policy

- Use the HuaLi 814 past-paper PDF as a guide for emphasis, not as copied exercise content.
- Past-paper-driven notes should be short and practical, for example "814 often asks for the minimum sampling frequency or whether aliasing occurs."
- Do not insert long past-paper questions into the handout unless the user later asks for a dedicated exercise section.
- Keep the sample handout clean; the exam reference should shape wording and emphasis, not make the page crowded.

## Deliverables

1. `DSP讲义重制_样章_前15页.pdf`
2. `DSP讲义重制_样章_校对记录.md`
3. Rendered PNG previews used for visual verification under `work/pdfs/`

## Verification

- Render the final sample PDF to PNG.
- Inspect representative pages for clipped text, bad line breaks, unreadable formulas, leftover heavy watermarks, and page number/header consistency.
- Confirm the PDF opens and reports A4 portrait page dimensions.

## Known Constraints

- The source is image-like, so OCR may make mistakes.
- Math formulas and graph labels require manual checking.
- This sample validates the workflow; full-course conversion should only begin after user review.
