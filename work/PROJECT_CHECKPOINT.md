# DSP Handout Project Checkpoint

Last updated: 2026-07-18 +08:00
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

- The full-book mathematical rendering audit is clean across all 13 active generators: source scanner `0` findings.
- All 13 batch PDFs were regenerated; their combined 117 content pages pass the PDF-text scan with `0` raw-LaTeX, raw-subscript, or mathematical slash-division findings.
- The focused math-rendering suite reports `44 passed`.
- Contact sheets for batches 5, 7, 8, 9, 10, and 13 were visually inspected; no new clipping, overlap, or unrendered formula text was found.
- Audit reports: `work/full_book_math_text_audit.md` and `work/full_book_pdf_text_audit.md`.
- Visual evidence: `tmp/pdfs/math_audit/batch5-contact.png`, `batch7-contact.png`, `batch8-contact.png`, `batch9-contact.png`, `batch10-contact.png`, and `batch13-contact.png`.

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

## Full-book Math Audit Completion

- The 13 verified batch PDFs were merged into a temporary 119-page A4 candidate with the existing cover, directory, and page-number workflow.
- Candidate PDF text audit: `0` findings.
- Candidate PDF regression: `4 passed` (cover/directory, near-blank pages, text bounds, image bounds).
- Merge and full-book audit suite: `50 passed`.
- Candidate visual inspection passed for cover, directory, all chapter starts, and representative formula/diagram-heavy pages. Evidence: `tmp/pdfs/math_audit/candidate_pages/contact-1.png` through `contact-5.png`.
- The verified candidate replaced `outputs/华理814DSP讲义_完整彩色A4版.pdf`.
- Stable PDF: 119 pages, A4, 15,660,703 bytes; SHA-256 matches the candidate.
- Stable source audit: `0` findings; stable PDF-text audit: `0` findings; stable PDF regression: `4 passed`.
- Full project regression: `236 passed`.
- Six legacy assertions were migrated from obsolete PDF text extraction or old literal source strings to the current rendered-math and source-topology rules.
- This regression-only update did not change any generator or PDF content; the verified 119-page stable PDF remains unchanged.

## Current WIP Defects - Not Fixed Yet

- `3.6 用 DFT 进行频谱分析`: the left `三类误差` card wraps `不可见` so that a lone `见` is left on the next line. Source: `draw_frequency_summary()` / `draw_two_col()` in `work/make_dsp_batch_185_227.py`.
- `5.2.2 直接 I 型`: the current rendered overview is missing source horizontal arrow(s) and must be rechecked against `tmp/pdfs/audit_source/iir-10.png`.
- `5.2.3 直接 II 型`: the derivation page omits the source difference equation, the rendered `H(z)` formula, and the complete direct-I/direct-II characteristic lists with source emphasis. Compare against `iir-11.png` and `iir-15.png`.
- No production fixes have been applied for these latest reports. The stable 119-page PDF remains the verified baseline.
- Full session recovery instructions are in repository-root `HANDOFF.md`.

## Full-book Spacing And Formula-size Audit Completion

- Shared rich-text helpers now reserve explicit vertical leading for headings, paragraphs, and bullet rows; the previously reported cramped bullet blocks no longer collide.
- Active display-formula helpers enforce a 28 pt printable minimum height. Same-level formulas use this common baseline; only genuinely dense multi-level formulas retain larger requested heights.
- All affected batch PDFs were rebuilt and merged into a 119-page A4 candidate without deleting content or compressing chapter endings.
- Ten contact sheets cover all 119 pages and were visually inspected. High-resolution checks were completed for pages 3, 6, 18, 24, 36, 40, 45, 70, 96, 102, and 118.
- The geometry audit's ten remaining hits were confirmed as diagram/axis boundary contacts rather than body-text overlap.
- Stable mathematical-text audit: `0 findings`; stable PDF regression: `4 passed`; full project regression: `246 passed`.
- Candidate and stable artifact SHA-256 match: `EF4B400AC3182BAD903492B57235ED6746A7D815F5F193A2A1634B95175CFE69`.
- Stable PDF replaced at `outputs/华理814DSP讲义_完整彩色A4版.pdf`: 119 A4 pages, 15,659,492 bytes.

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

Read `HANDOFF.md`, add failing regression tests for the four current WIP defects, and repair only batches 7 and 9 before producing a full-book candidate.

## Commit Policy

- The full-book mathematical rendering and stacked-fraction audit is complete and verified.
- Update, commit, and push this file after each verified unit of work.
