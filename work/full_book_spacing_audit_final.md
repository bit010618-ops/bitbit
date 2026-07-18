# Full-book spacing and formula-size audit

Audit date: 2026-07-18

## Scope

- Complete 119-page A4 handout.
- Body paragraphs, bullet lists, explanatory notes, tables, formulas, and chapter transitions.
- Same-level display formulas use a common printable baseline height.
- Dense multi-level fractions, products, sums, and superscript-heavy formulas may exceed the baseline only when needed for print legibility.
- Original red, bold, and emphasized source content remains emphasized.

## Implemented policy

- Shared rich-text helpers now reserve explicit vertical leading for headings, paragraphs, and bullet rows.
- Display-formula helpers enforce a 28 pt minimum rendered height across the active generators.
- Existing larger formula requests remain only on genuinely dense formula groups, including the Butterworth tables, Parseval identity, periodic convolution, and FIR frequency-sampling formulas.
- Content was reflowed rather than deleted or compressed; chapter starts remain on fresh pages.

## Automated verification

- Full project suite: `246 passed`.
- Stable PDF regression: `4 passed`.
- Stable mathematical-text scan: `0 findings`.
- Candidate and stable PDF SHA-256: `EF4B400AC3182BAD903492B57235ED6746A7D815F5F193A2A1634B95175CFE69`.
- Stable PDF: 119 A4 pages, 15,659,492 bytes.

## Visual verification

- All 119 pages were reviewed through ten contact sheets in `tmp/pdfs/spacing_audit/candidate_contacts/`.
- High-resolution checks were completed for pages 3, 6, 18, 24, 36, 40, 45, 70, 96, 102, and 118.
- The ten geometry-audit hits on pages 3, 6, 24, 40, 102, and 118 were confirmed as diagram/axis boundary contacts rather than body-text overlap.
- No clipped formula, raw formula source, bullet collision, paragraph collision, new blank page, or chapter-start regression was found.

## Final artifact

`outputs/华理814DSP讲义_完整彩色A4版.pdf`
