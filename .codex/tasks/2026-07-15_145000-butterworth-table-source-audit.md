# Task: Butterworth table source audit

## Objective

Add the original Butterworth normalized pole-position table while retaining the existing factorization and expanded-coefficient tables. Preserve all source entries, headers, colors, formulas, and spacing without collisions.

## Recovery Evidence

- Previous verified item: Butterworth response indicator graph, commit `4a75b8f`.
- Current tests: `24 passed`.
- Stable full-book PDF remains unchanged.

## Completed

- Added the original 1-9 order Butterworth normalized pole-position table with the diagonal corner header and all five pole columns.
- Retained the existing factorization table and expanded-coefficient table.
- Fixed Matplotlib formula colors so PDF generation succeeds.
- Kept the factorization heading and table on the same page.
- Verified previews: `tmp/pdfs/iir_preview/butter-pole-table-final-12.png` and `tmp/pdfs/iir_preview/butter-pole-table-final-13.png`.

## Exact Next Action

Commit and push this verified work unit, then continue with the next pending audit-matrix item.
