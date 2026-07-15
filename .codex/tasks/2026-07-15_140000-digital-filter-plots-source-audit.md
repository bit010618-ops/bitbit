# Task: Digital filter plots source audit

## Objective

Compare `draw_digital_filter_type_plots` against original PPT page 290 / `tmp/pdfs/audit_source/iir-26.png`, preserving periodic repetitions, cutoff labels, omission marks, colors, and spacing.

## Recovery Evidence

- Previous verified item: analog ideal filter plots, commit `5875e63`.
- Current tests: `19 passed`.
- Stable full-book PDF remains unchanged.

## Exact Next Action

Completed. Source `iir-26.png` and batch-9 page 11 were compared at full resolution.

## Verified Result

- Restored `omega = Omega T` and `周期延拓`.
- Restored low/high cutoff labels and band-pass/band-stop `omega_c1`, `omega_c2` labels.
- Restored source-specific outer pi labels, including `-3pi` and `3pi` where present.
- Structural tests: `20 passed`.
- Visual evidence: `tmp/pdfs/iir_preview/digital-filter-source-candidate-11.png`.
- Stable full-book PDF remains unchanged.
