# Task: Direct-I source fidelity

## Objective

Restore the direct-I IIR overview diagram so its topology, omission notation, arrows, labels, frames, and spacing match the original source page without collisions.

## Completed

- Restored both blue dashed network frames.
- Restored four red dotted omission segments: delay and accumulator rails in both feedforward and feedback networks.
- Restored terminal dots and interior main-line arrows while removing synthetic internal node dots.
- Preserved the feedback accumulator rail and the source left-pointing callout arrow.
- Moved network labels below their frames with safe clearance from the following note panel.
- Rebuilt batch 9 and visually compared the result with the original source page.
- Marked `draw_direct_i_general` verified in `work/figure_audit_matrix.md`.

## Verification

- Tests: `14 passed` in `work/test_iir_structure_source_topology.py`.
- Verified preview: `tmp/pdfs/iir_preview/direct-i-source-locked-v2-03.png`.
- Source: `tmp/pdfs/audit_source/iir-10.png`.
- Enlarged source crop: `tmp/pdfs/iir_preview/source-direct-i-crop.png`.

## Remaining

- Continue the next unverified diagram family in `work/figure_audit_matrix.md`.
- Do not replace the stable full-book PDF until the remaining full-book audit passes.

## Exact Next Action

Read `work/figure_audit_matrix.md`, select the next pending diagram, and compare its generated page against the original before making any edit.
