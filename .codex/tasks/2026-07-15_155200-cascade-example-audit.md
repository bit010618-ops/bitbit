# Task: Cascade IIR example source audit

## Objective

Compare the emitted `draw_cascade_example` page against the original DSP PPT/PDF and restore source-faithful topology, arrows, labels, coefficients, proportions, and spacing without collisions.

## Recovery Evidence

- Previous verified unit: direct I/direct II numerical example terminal nodes, commit `a1c12fc`.
- Tests at handoff: `25 passed` in `work/test_iir_structure_source_topology.py`.
- Stable full-book PDF remains unchanged.

## Completed

- Compared current batch page 7 with source `tmp/pdfs/audit_source/iir-18.png`.
- Added failing tests for every omitted section coefficient and source node policy.
- Restored gains `2` and `4`, coefficient pairs `0.25/-0.379`, `1/-1.24`, `-0.5/5.264`, terminal dots, section nodes, and interior arrows.
- Verification: `26 passed`.
- Visual evidence: `tmp/pdfs/iir_preview/cascade-example-source-locked-07.png`.

## Exact Next Action

Commit and push this verified unit, then begin `draw_parallel_example` in a new task file.
