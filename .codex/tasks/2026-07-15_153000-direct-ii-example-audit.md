# Task: Direct-II example source audit

## Objective

Continue the full-book source-faithfulness audit from the next diagram that is actually emitted by the batch-9 generator. Compare `draw_direct_ii_examples` against the original DSP PPT/PDF and restore every topology, arrow, label, coefficient, and spacing detail without collisions.

## Recovery Evidence

- Previous verified unit: Butterworth source pole table, commit `1725620`.
- `draw_simple_coeff_grid` is defined but has no call site in `build()` and therefore does not correspond to a current PDF page.
- Stable full-book PDF remains unchanged.

## Completed

- Marked unused `draw_simple_coeff_grid` as not applicable.
- Confirmed source mismatch on the direct I/direct II example top signal lines.
- Added a failing policy test, restored source terminal dots and interior arrows, and kept the internal coefficient topology unchanged.
- Verification: `25 passed`.
- Visual evidence: `tmp/pdfs/iir_preview/direct-example-source-locked-05.png`, compared with `tmp/pdfs/audit_source/iir-14.png`.

## Exact Next Action

Commit and push this verified unit, then start a new task file for `draw_cascade_example`.
