# Task: Build chapter-reordered ECUST 814 past-exam PDF

## Objective

Create `output/华理814历年真题_按章节分类完整版.pdf` by directly cropping each original question image from the source past-exam PDF and reordering those unchanged images by the official 814 syllabus chapters and knowledge points. Indexes, CSV files, and frequency statistics are intermediate artifacts only.

## Current state

- Started: 2026-08-26 23:35:52 Asia/Shanghai
- Working directory is not a Git repository; task progress is routed to the designated fallback repository.
- Completed: 2026-08-27 Asia/Shanghai.
- Reused the previously verified 449-unit classification database and mapped every unit to original rendered question imagery.
- Final source coverage: 18 available years, 176 original main questions, 449 classification units, source PDF pages 5-59.
- Generated the required 532-page `output/华理814历年真题_按章节分类完整版.pdf`, the index PDF, database CSV, completeness report, and 14 per-section PDFs.
- Question-image mapping: 168 exact question crops, 179 complete-parent-question crops for classified subquestions, 102 manually verified parent-question crops for source text-layer omissions, and 0 full-page fallback crops.
- Verification: 50 tests passed; 16 PDFs reopened as A4; all 1082 rendered output pages scanned; 449/449 record IDs present; chapter order 1-13 then Appendix A; 0 blank pages; 0 A4-edge overflow pages.
- Final full-PDF SHA-256: `7FAC34ED3FD60845FE3F505E72D1689C8907EF2D17577ADF70D90895A21B57F3`.

## Next action

Deliver the completed files to the user. No implementation work remains.
