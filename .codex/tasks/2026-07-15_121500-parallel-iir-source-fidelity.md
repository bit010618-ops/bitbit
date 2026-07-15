# Task: Parallel-IIR source fidelity

## Objective

Rebuild the general parallel-IIR structure so its main path, buses, direct polynomial branch, second-order branches, delay chains, arrows, nodes, omission marks, labels, and proportions match original PPT page 286 / audit image `iir-19.png` without collisions.

## Current Evidence

- Source: `tmp/pdfs/audit_source/iir-19.png`.
- Current mismatching render: `tmp/pdfs/iir_preview/parallel-current-08.png`.
- Root cause: `draw_parallel_iir` models each second-order section as a wide rectangular grid instead of the source's compact central delay chain with left feedback and right feedforward accumulators.

## Completed

- Added topology and geometry regressions for the source bus span, direct polynomial branch, omission rails, section spacing, and vertical ellipses.
- Rebuilt `draw_parallel_iir` to match original PPT page 286 / `tmp/pdfs/audit_source/iir-19.png`.
- Removed the synthetic red annotation that was not present in the source.
- Verified render: `tmp/pdfs/iir_preview/parallel-source-locked-08.png`.
- Targeted result: `17 passed` in `work/test_iir_structure_source_topology.py`.

## Exact Next Action

Continue from the next unverified diagram family in `work/figure_audit_matrix.md`; do not rebuild the stable full-book PDF yet.
