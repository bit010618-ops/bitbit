# Current DSP Handout Progress

- Active objective: finish the full-book source-faithful diagram audit without collisions.
- Latest verified unit: Butterworth table group.
- Added the original normalized pole-position table while retaining the existing factorization table and expanded-coefficient table.
- The factorization heading now stays with its table on batch page 13.
- Audit matrix: `draw_butter_tables_full` is verified against original PPT pages 297-298.
- Tests: `24 passed` in `work/test_iir_structure_source_topology.py`.
- Latest previews: `tmp/pdfs/iir_preview/butter-pole-table-final-12.png` and `tmp/pdfs/iir_preview/butter-pole-table-final-13.png`.
- Stable full-book PDF remains unchanged.
- Active next item: compare `draw_simple_coeff_grid` with its original PPT page and current batch page.
