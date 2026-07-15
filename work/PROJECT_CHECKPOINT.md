# DSP Handout Project Checkpoint

Last updated: 2026-07-15 11:03 +08:00
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
- Targeted verification: `11 passed` in `work/test_iir_structure_source_topology.py`.

## Current WIP Defects - Not Fixed Yet

1. Direct-I overview page (`tmp/pdfs/iir_preview/scan-03.png` and latest user screenshot):
   - right dashed frame and `y(n)`/right explanatory text still need a clean separation;
   - frame/arrow geometry must be rechecked against `tmp/pdfs/audit_source/iir-10.png`.
2. The stable full-book PDF has not been rebuilt from these WIP generator changes.

## Source References

- Direct-I overview source: `tmp/pdfs/audit_source/iir-10.png`
- Formula source: `tmp/pdfs/audit_source/iir-15.png`
- Four-network source: `tmp/pdfs/audit_source/iir-16.png`
- Verified four-network preview: `tmp/pdfs/iir_preview/fixed-four-06.png`
- Current direct-I overview preview: `tmp/pdfs/iir_preview/scan-03.png`

## Current Tests

- Target file: `work/test_iir_structure_source_topology.py`
- Existing topology tests include source coefficient preservation, H2 `-5`, delay-label policy, H2 right-branch length, and source-title suppression.
- Current targeted result: `11 passed`.

## Exact Next Step

1. Reopen the current direct-I overview render and compare it against `tmp/pdfs/audit_source/iir-10.png`.
2. Add a failing geometry test for the remaining right-frame / `y(n)` / explanatory-text clearance defect.
3. Change only the direct-I overview geometry, rebuild batch 9, and render the affected page.
4. Visually compare the new render against the source before marking it verified.

## Commit Policy

- This checkpoint is intentionally WIP. Do not describe the three defects above as fixed.
- Update, commit, and push this file after each verified unit of work.
