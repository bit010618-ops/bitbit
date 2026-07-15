# DSP Handout Project Checkpoint

Last updated: 2026-07-15 10:45 +08:00
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

## Current WIP Defects - Not Fixed Yet

1. Four-network page (`tmp/pdfs/iir_preview/new-06.png`):
   - panel titles `H_1` and `H_2` sit too close to the main signal lines;
   - accumulator/return rails incorrectly repeat `z^{-1}` labels;
   - H2 direct-II right branch has only two coefficients but still draws a third vertical segment and dangling bottom node.
2. Direct-I overview page (`tmp/pdfs/iir_preview/scan-03.png` and latest user screenshot):
   - right dashed frame and `y(n)`/right explanatory text still need a clean separation;
   - frame/arrow geometry must be rechecked against `tmp/pdfs/audit_source/iir-10.png`.
3. The stable full-book PDF has not been rebuilt from these WIP generator changes.

## Source References

- Direct-I overview source: `tmp/pdfs/audit_source/iir-10.png`
- Formula source: `tmp/pdfs/audit_source/iir-15.png`
- Four-network source: `tmp/pdfs/audit_source/iir-16.png`
- Current four-network preview: `tmp/pdfs/iir_preview/new-06.png`
- Current direct-I overview preview: `tmp/pdfs/iir_preview/scan-03.png`

## Current Tests

- Target file: `work/test_iir_structure_source_topology.py`
- Existing topology tests include source coefficient preservation, H2 `-5`, delay-label policy, and H2 right-branch length.
- The delay-label policy test currently expects `direct_form_numeric_delay_label_policy()`; confirm whether it is still failing before implementation.

## Exact Next Step

1. Add failing geometry tests for title-to-main-line clearance and H2 direct-II right-rail length.
2. Run the target test file and confirm RED for the intended reasons.
3. Change only `draw_direct_form_numeric_examples()`:
   - label `z^{-1}` only on actual downward delay chains;
   - stop the H2 direct-II right return rail after its second coefficient;
   - move panel titles upward enough to clear the main line and gain labels.
4. Rebuild batch 9, render the new four-network page, compare it against `iir-16.png`, and only then update this checkpoint.
5. Return to the direct-I overview and visually verify it against `iir-10.png`.

## Commit Policy

- This checkpoint is intentionally WIP. Do not describe the three defects above as fixed.
- Update, commit, and push this file after each verified unit of work.
