# DSP Handout Project Checkpoint

Last updated: 2026-07-15 12:00 +08:00
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
- Targeted verification: `14 passed` in `work/test_iir_structure_source_topology.py`.

## Current WIP Defects - Not Fixed Yet

1. The stable full-book PDF has not been rebuilt from these batch-9 generator changes.
2. The remaining full-book source audit must continue from the next unverified item in `work/figure_audit_matrix.md`; do not repeat the verified FFT, four-network, or direct-I overview items above.

## Source References

- Direct-I overview source: `tmp/pdfs/audit_source/iir-10.png`
- Formula source: `tmp/pdfs/audit_source/iir-15.png`
- Four-network source: `tmp/pdfs/audit_source/iir-16.png`
- Verified four-network preview: `tmp/pdfs/iir_preview/fixed-four-06.png`
- Verified direct-I overview preview: `tmp/pdfs/iir_preview/direct-i-source-locked-v2-03.png`
- Enlarged source crop: `tmp/pdfs/iir_preview/source-direct-i-crop.png`

## Current Tests

- Target file: `work/test_iir_structure_source_topology.py`
- Existing topology tests include source coefficient preservation, H2 `-5`, delay-label policy, H2 right-branch length, and source-title suppression.
- Current targeted result: `14 passed`.

## Exact Next Step

1. Open `work/figure_audit_matrix.md` and select the next unverified diagram family after the verified direct-I overview.
2. Compare that diagram against its original PDF/PPT page before editing.
3. Add a failing structural test for any confirmed mismatch, then make the smallest source-faithful generator change.
4. Render and visually inspect the affected page before updating this checkpoint again.

## Commit Policy

- This checkpoint is intentionally WIP. Do not describe the full-book audit or stable full-book PDF as complete.
- Update, commit, and push this file after each verified unit of work.
