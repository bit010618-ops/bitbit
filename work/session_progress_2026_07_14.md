# 2026-07-14 Progress

- Added `work/test_latest_user_layout_fixes.py`; observed three expected failures before implementation.
- Rebuilt batches one, two, and five after the targeted fixes.
- Rendered affected batch pages at 180 dpi and visually verified axis clearance, amplitude proportions, formula legibility, and same-page grouping.
- Rebuilt the 109-page complete PDF.
- Updated two stale regressions that encoded superseded geometry requirements.
- Full regression suite result: `151 passed`.

## 2026-07-14 latest discrete-axis correction

- Reworked the `x(1-2n)` plot to use a 150 pt tall drawing area, moved it 18 pt lower, and reserved 168 pt in the page flow.
- Preserved the exact sample values `{-1: 1, 0: 4, 1: -2}` and the source 1:4 amplitude relationship.
- Shifted only the `n=-1` amplitude label `1` by 3 pt to the right so it no longer shares the stem centerline.
- Rebuilt the 109-page complete PDF and visually checked merged page 7.
