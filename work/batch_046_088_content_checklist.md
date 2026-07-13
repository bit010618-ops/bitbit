# Batch 03 content checklist: source PPT 46-88

Status: redo required. Previous four-page draft was too compressed and is not accepted as complete.

Hard rule for this and all later batches:
- Preserve all source content: headings, property names, definitions, red emphasis text, explanatory paragraphs, example statements, derivation steps, tables, formulas, and diagrams.
- Remove only watermark, decorative background, temporary wording, and layout noise.
- Correct only clear errors or formatting problems.
- Intermediate batch PDFs are review artifacts only. Final delivery must be one merged complete handout PDF.

## Source page checklist

- 46-49: chapter transition / guide / contents. Preserve chapter framing where useful for learning, omit only decoration.
- 50-51: z-transform motivation from sampled signal and definition. Preserve Laplace-to-z mapping and both definition/inverse-form content.
- 52-57: ROC definition and sequence-type explanation. Preserve finite/right-sided/left-sided/bilateral descriptions and diagrams/conclusions.
- 58-61: same algebraic z-transform with different ROC examples. Preserve all example steps and ROC comparisons.
- 62: common z-transform table. Preserve full table entries and ROC column.
- 63-65: inverse z-transform. Preserve methods, partial fraction process, ROC-dependent answers.
- 66-69: inverse z-transform examples/notes. Need recheck source images before finalizing this range.
- 70: z-transform property (1) linearity. Preserve property name, given conditions, ROC overlap formula, and zero-pole cancellation explanation.
- 71: linearity example. Preserve full example showing ROC expansion to whole z-plane.
- 72-73: property (2) time-shift. Preserve “双边单边大不同”,双边 z 变换, 单边 z 变换, and red emphasis that ROC does not change for bilateral time shift.
- 74-75: property (3) z-domain scaling / sequence exponential weighting. Preserve formulas and cosine example.
- 76: property (4) z-domain differentiation. Preserve general repeated-differentiation formula and example for `nu(n)`.
- 77: properties (5)-(7): initial value theorem, final value theorem, time-domain convolution theorem. Preserve causal-sequence condition and red emphasis about unit-circle poles.
- 78: convolution example. Preserve full derivation and conclusion about zero-pole cancellation expanding ROC.
- 79-83: DTFT definition, inverse transform, periodicity, and relation to z-transform. Preserve unit-circle mapping and all explanatory conditions.
- 84: DTFT properties (1)-(3): linearity, sequence shift, frequency shift. Preserve property names and formulas.
- 85: DTFT properties (4)-(6): sequence linear weighting, sequence reversal, conjugate symmetry. Preserve property names, definitions, red conclusion about real/imag parity, and component formulas.
- 86: real/imag and conjugate symmetric component DTFT relationships. Preserve all formulas and the following example statement.
- 87-88: example following conjugate-symmetry section. Need recheck source images and preserve full solution.

## Current correction focus

1. DONE: Rebuilt `work/make_dsp_batch_046_088.py` so section 2.1.3 includes z-transform property names, ROC notes, one-sided/two-sided shift distinction, red emphasis, and examples from source pages 70-78.
2. DONE: Restored source PPT page 73 single-sided z-transform difference-equation example with rendered formulas and inverse-transform derivation.
3. DONE: Rebuilt section 2.2.2 so DTFT properties include property names, conjugate-symmetry red emphasis text, component formulas, and the example plots from source pages 84-87.
4. DONE: Re-rendered to `work/pdfs/batch_046_088_render_full_v5/` and inspected pages 4, 5, 7, and 8.
5. REMAINS: before final merging, run a page-by-page source checklist for 46-88 to catch any smaller source-page items from 46-69 and 79-83 that may still need expansion.
