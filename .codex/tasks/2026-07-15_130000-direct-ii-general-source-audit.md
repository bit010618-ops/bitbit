# Task: Direct-II general source audit

## Objective

Verify and, only if needed, correct `draw_direct_ii_general` against original PPT page 276 / `tmp/pdfs/audit_source/iir-11.png`.

## Source Requirements

- Upper-left: direct-I network with two dashed delay-chain frames and side variables `x(n-1)`, `x(n-2)`, `y(n-1)`, `y(n-2)`.
- Upper-right: exchanged two-part network with two independent dashed frames and variables `w_1`, `w_2`, `b_0`; no synthetic side-variable labels.
- Lower: merged direct-II network with no dashed frame and a shared two-stage delay chain plus both outer accumulator rails.
- Preserve source arrow directions, coefficient placement, node positions, and three-panel proportions without overlaps.

## Evidence

- Source: `tmp/pdfs/audit_source/iir-11.png`.
- Current generated page: batch-9 page 4; previous preview `tmp/pdfs/iir_preview/scan-04.png`.

## Completed

- Added structural tests for frame policy, independent-frame gap, side-label policy, and merged outer rails.
- Rebuilt batch 9 and rendered page 4.
- Verified against `iir-11.png` and the enlarged source crop.
- Result: `18 passed`; preview `tmp/pdfs/iir_preview/direct-ii-source-locked-04.png`.
