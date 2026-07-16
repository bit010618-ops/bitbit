# DSP Handout Project Checkpoint

Last updated: 2026-07-15 16:08 +08:00
Branch: `main`
Remote: `origin` -> `https://github.com/bit010618-ops/bitbit.git`
Baseline before this checkpoint: `9a70116 Fix DTFT sample value labels`

## Recovery Protocol

1. Read this file.
2. Run `git status --short` and `git log -5 --oneline`.
3. Inspect the latest rendered PNGs named below.
4. Run the listed targeted tests before changing production code.
5. Treat chat screenshots only as defect reports; use disk files and rendered output as the progress source of truth.

## Verified Work

- The FFT source audit is complete for the three tracked FFT diagram families in `work/figure_audit_matrix.md`.
- The stable full-book PDF remains the prior 118-page version at `outputs/华理814DSP讲义_完整彩色A4版.pdf`.
- The direct-I general-page geometry was partially separated from its frames and side text, but the latest user screenshot shows the page still needs visual correction before it can be marked verified.
- PPT pages 280-281 topology data and the missing four numerical direct-I/direct-II diagrams have been added to `work/make_dsp_batch_266_300_redraw.py`.
- The H2 numerator was corrected from `+5` to `-5` in the corresponding formula.
- The four numerical direct-I/direct-II diagrams now match the source 2x2 topology: synthetic H1/H2 panel titles were removed, `z^{-1}` appears only on true downward delay chains, and the H2 direct-II right branch stops after its second coefficient.
- Verified render: `tmp/pdfs/iir_preview/fixed-four-06.png`, compared against `tmp/pdfs/audit_source/iir-16.png`.
- The direct-I overview now restores the source topology and omission notation: both blue dashed network frames, four internal red dotted omission segments, terminal dots, interior main-line arrows, no synthetic internal node dots, the feedback accumulator rail, and the left-pointing callout arrow.
- Verified direct-I render: `tmp/pdfs/iir_preview/direct-i-source-locked-v2-03.png`, compared against `tmp/pdfs/audit_source/iir-10.png` and the enlarged crop `tmp/pdfs/iir_preview/source-direct-i-crop.png`.
- The parallel-IIR overview now matches the source topology and proportions: compact input/output bus, direct polynomial branch, both omission rails, first and final second-order branches, source arrow directions, source labels, and vertical ellipses.
- Verified parallel-IIR render: `tmp/pdfs/iir_preview/parallel-source-locked-08.png`, compared against `tmp/pdfs/audit_source/iir-19.png`.
- The direct-II derivation page now matches original PPT page 276: the upper direct-I panel retains two separate delay-chain frames and side variables; the exchanged upper-right panel uses two independent dashed networks rather than a prematurely merged delay chain; the lower network alone shares the central delay chain and has no synthetic dashed frame.
- Verified direct-II render: `tmp/pdfs/iir_preview/direct-ii-source-locked-04.png`, compared against `tmp/pdfs/audit_source/iir-11.png` and `tmp/pdfs/iir_preview/source-direct-ii-upper-right-crop.png`.
- The analog ideal low/high/band-pass/band-stop plots now retain all source annotations from PPT page 289. The previously omitted low-pass `全部为阻带` and high-pass `全部为通带` callouts, red direction arrows, and infinity marks have been restored without axis or label collisions.
- Verified analog-filter render: `tmp/pdfs/iir_preview/analog-filter-source-candidate-10.png`, compared against `tmp/pdfs/audit_source/iir-25.png`.
- The four periodic digital ideal-response plots now retain the source repetition pattern, red omission dots, `omega = Omega T` / periodic-extension annotation, low/high cutoff labels, band-pass/band-stop cutoff labels, and source-specific outer pi ticks.
- Verified digital-filter render: `tmp/pdfs/iir_preview/digital-filter-source-candidate-11.png`, compared against `tmp/pdfs/audit_source/iir-26.png`.
- The Butterworth design-indicator graph now restores the source dark-filled `1dB`, `3dB`, and `40dB` badges with white text and the complete `Omega_c称为3dB截止频率` definition.
- Verified Butterworth render: `tmp/pdfs/iir_preview/butterworth-source-candidate-11.png`, compared against `tmp/pdfs/audit_source/iir-28.png`.
- The Butterworth table group now includes the original normalized pole-position table while preserving the existing factorization table and the original expanded-coefficient table.
- The pole table retains all 1-9 order rows, five pole columns, the diagonal corner header, source colors, and rendered mathematical notation; the factorization heading remains with its table.
- Verified table renders: `tmp/pdfs/iir_preview/butter-pole-table-final-12.png` and `tmp/pdfs/iir_preview/butter-pole-table-final-13.png`, compared against `tmp/pdfs/audit_source/iir-33.png` and `tmp/pdfs/audit_source/iir-34.png`.
- Targeted verification: `24 passed` in `work/test_iir_structure_source_topology.py`.
- The direct I/direct II numerical example page now restores source-style input/output terminal dots and top-line interior arrows; the output endpoint is no longer replaced by an arrowhead.
- The already-correct internal coefficient, delay-chain, and branch topology was left unchanged.
- `draw_simple_coeff_grid` has no call site in `build()` and is recorded as not applicable rather than audited as a current PDF page.
- Verified direct-example render: `tmp/pdfs/iir_preview/direct-example-source-locked-05.png`, compared against `tmp/pdfs/audit_source/iir-14.png`.
- Targeted verification now reports `25 passed` in `work/test_iir_structure_source_topology.py`.
- The cascade-IIR example now restores every source coefficient and node: section gains `2` and `4`, first-order pair `0.25/-0.379`, second-order pairs `1/-1.24` and `-0.5/5.264`, terminal dots, section junction dots, and interior main-line arrows.
- Verified cascade render: `tmp/pdfs/iir_preview/cascade-example-source-locked-07.png`, compared against `tmp/pdfs/audit_source/iir-18.png`.
- Targeted verification now reports `26 passed` in `work/test_iir_structure_source_topology.py`.

## Current WIP Defects - Not Fixed Yet

1. The stable full-book PDF has not been rebuilt from these batch-9 generator changes.
2. The remaining full-book source audit must continue from `draw_parallel_example`; do not repeat the verified FFT, four-network, direct-I, parallel-IIR overview, Butterworth-table, direct-example, or cascade-example items above.

## Source References

- Direct-I overview source: `tmp/pdfs/audit_source/iir-10.png`
- Formula source: `tmp/pdfs/audit_source/iir-15.png`
- Four-network source: `tmp/pdfs/audit_source/iir-16.png`
- Verified four-network preview: `tmp/pdfs/iir_preview/fixed-four-06.png`
- Verified direct-I overview preview: `tmp/pdfs/iir_preview/direct-i-source-locked-v2-03.png`
- Enlarged source crop: `tmp/pdfs/iir_preview/source-direct-i-crop.png`
- Parallel-IIR source: `tmp/pdfs/audit_source/iir-19.png`
- Verified parallel-IIR preview: `tmp/pdfs/iir_preview/parallel-source-locked-08.png`
- Direct-II source: `tmp/pdfs/audit_source/iir-11.png`
- Verified direct-II preview: `tmp/pdfs/iir_preview/direct-ii-source-locked-04.png`
- Analog ideal-response source: `tmp/pdfs/audit_source/iir-25.png`
- Verified analog-response preview: `tmp/pdfs/iir_preview/analog-filter-source-candidate-10.png`
- Digital ideal-response source: `tmp/pdfs/audit_source/iir-26.png`
- Verified digital-response preview: `tmp/pdfs/iir_preview/digital-filter-source-candidate-11.png`
- Butterworth indicator source: `tmp/pdfs/audit_source/iir-28.png`
- Verified Butterworth preview: `tmp/pdfs/iir_preview/butterworth-source-candidate-11.png`
- Butterworth pole-table source: `tmp/pdfs/audit_source/iir-33.png`
- Butterworth coefficient-table source: `tmp/pdfs/audit_source/iir-34.png`
- Verified Butterworth table previews: `tmp/pdfs/iir_preview/butter-pole-table-final-12.png`, `tmp/pdfs/iir_preview/butter-pole-table-final-13.png`
- Direct-example source: `tmp/pdfs/audit_source/iir-14.png`
- Verified direct-example preview: `tmp/pdfs/iir_preview/direct-example-source-locked-05.png`
- Cascade-example source: `tmp/pdfs/audit_source/iir-18.png`
- Verified cascade-example preview: `tmp/pdfs/iir_preview/cascade-example-source-locked-07.png`

## Current Tests

- Target file: `work/test_iir_structure_source_topology.py`
- Existing topology tests include source coefficient preservation, H2 `-5`, delay-label policy, H2 right-branch length, and source-title suppression.
- Current targeted result: `26 passed`.

## Exact Next Step

1. Continue with the next unverified matrix item, `draw_parallel_example`, comparing the current batch page against its original PPT page.
2. Compare that diagram against its original PDF/PPT page before editing.
3. Add a failing structural test for any confirmed mismatch, then make the smallest source-faithful generator change.
4. Render and visually inspect the affected page before updating this checkpoint again.

## Commit Policy

- This checkpoint is intentionally WIP. Do not describe the full-book audit or stable full-book PDF as complete.
- Update, commit, and push this file after each verified unit of work.
