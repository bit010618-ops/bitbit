# Task: Filter type plots source audit

## Objective

Locate and compare `draw_filter_type_plots` with its original PPT page, then correct only confirmed topology, label, axis, or spacing mismatches.

## Recovery Evidence

- Previous verified item: `draw_direct_ii_general`, commit `561cdba`.
- Stable full-book PDF remains unchanged.

## Exact Next Action

Completed: source PPT page 289 was compared with batch-9 page 10. Restored the omitted low-pass/high-pass stopband/passband callouts and infinity arrows. Structural tests: `19 passed`. Verified preview: `tmp/pdfs/iir_preview/analog-filter-source-candidate-10.png`.
