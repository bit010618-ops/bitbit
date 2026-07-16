# Full-book math rendering and fraction audit

## Objective

Audit the complete DSP handout and all batch generators so that every mathematical expression is rendered as mathematics, never left as source-like plain text, and every mathematical division or ratio uses a stacked fraction rather than `/`.

## User clarifications

- The examples `X(e^{jω})`, `ω/(2π)`, and `R_4(n)` are only examples, not the complete search scope.
- All mathematical objects are covered: subscripts, superscripts, exponents, roots, sums, limits, intervals, transforms, complex exponentials, piecewise definitions, ratios, and formula fragments embedded in Chinese prose.
- The existing added Butterworth factorization table must remain; the original source table is added in addition to it.

## Verification strategy

1. Build a reproducible source scanner over every active handout generator.
2. Build a PDF-text scanner over every batch PDF and the stable full-book PDF.
3. Add failing tests for known raw-formula and slash-division defects.
4. Fix one batch at a time, regenerate affected PDFs, render affected pages, and visually inspect them.
5. Update checkpoint and push each verified batch; replace the stable full-book PDF only after the global audit is clean.

## Current state

- Previous cascade-IIR unit committed as `ee421d4` and pushed to `origin/main`.
- All 13 active generators have been audited and regenerated, and the stable full-book PDF has been replaced only after candidate verification.
- Source scanner result: `0` findings.
- Batch PDF text scanner result: `0` findings across 117 generated content pages.
- Targeted batch audit tests: `44 passed`; merge and full-book audit tests: `50 passed`.
- High-risk visual contact sheets for batches 5, 7, 8, 9, 10, and 13 were inspected without finding new clipping, overlap, or source-like formula text.
- Temporary and stable full-book PDFs are identical by SHA-256, A4, and 119 pages.
- Stable full-book source audit: `0` findings; PDF-text audit: `0` findings.
- Full-book PDF regression: `4 passed`.
- Full project regression: `236 passed`.
- Six stale tests were updated to reflect the verified implementation: rendered spectrum titles, rendered unit-circle labels, image-rendered FFT sequence labels, enriched cascade source topology, and nested stacked fractions in the decimation derivation.
- No generator or PDF content changed during the full regression pass.
- Final visual evidence: `tmp/pdfs/math_audit/candidate_pages/contact-1.png` through `contact-5.png`.

## Exact next action

Commit and push the regression-test and checkpoint updates, then close the full-book math-rendering audit.
