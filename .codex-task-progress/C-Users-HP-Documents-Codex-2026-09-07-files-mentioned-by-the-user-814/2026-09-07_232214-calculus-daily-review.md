# Calculus daily review bank

## Objective and accepted requirements
Create a daily mixed review bank from the five user-supplied calculus wrong-question Anki exports (.apk.1g files), 60-90 minutes daily. PDF is the first delivery. PDF: all text, formulas and options retyped in real LaTeX; choice/fill typically 3 questions per page and large questions 2 per page; each day starts a fresh page; small source labels; handwriting space; NO answers. Use the two Arthur mock-paper PDFs as font and spacing references. Scientific diagrams must match the originals in every detail except proportional scale; use original diagram crops when exact redraw cannot be ensured.
MarginNote afterwards: SAME day assignments; narrow native source header and large question body, plus folded final-answer and detailed-solution branches. Original Anki exports do not include the actual answer/solution content, only question images and collapsed thumbnails; authored solutions must be identified as such. User will later supply series and other topics; keep stable IDs and a re-plannable data source.

## Verified PDF milestone (2026-09-08)
- Extracted 276 distinct records: S93, M66, E62, D48, I7. All 276 have transcription records and preserved original source UUIDs.
- PDF includes 274 usable questions in 34 days, each with four major subjects, plus seven improper-integral questions spread across days. Estimated daily total 75-84 minutes including 12 minutes review.
- Two pending source records clearly listed on final page: M016 missing original question image; E006 original equation and stated inflection-point condition conflict. Other source notations are documented in the appendix.
- Built via Tectonic / real LaTeX, 132 A4 pages, 17 embedded fonts, 4 exact original diagram crops, 36 navigation bookmarks. Text, formulas and options are vector/type text; only diagrams are cropped raster images.
- Final artifact: C:/Users/HP/Documents/Codex/2026-09-07/files-mentioned-by-the-user-814/outputs/高数错题每日复习_阶段一_题目留白版.pdf
- SHA256: 2e8f851ed82aae8789a16bc0812636340964e8bd4c52b569a74e527447649241
- Verification: work/calculus/verification.json reports VERIFY_OK. All 274 IDs occur exactly once on planned exercise pages, every day starts fresh, page counts and contents match the daily plan, no missing glyphs/overfull boxes/LaTeX errors, all fonts embedded, 4 diagram crops only. All-page contact sheets inspected; representative full-size formula/multi-part/diagram pages and final Poppler rendering inspected. No clipping or layout overflow found.

## Durable files
work/calculus/inventory.json; transcribed_{S,M,E,D,I}.json; daily_plan.json; daily_index.csv; daily_review.tex; build_pdf.py; verify_pdf.py; verification.json. Native MarginNote helper from earlier 814 work: work/native_excerpt.py and work/package_bank.py. Do not modify the earlier delivered 814 bank.

## Remaining and exact next action
Deliver the verified PDF immediately, then continue the MarginNote phase. Audit which solution fields are already populated and verify them; author and check missing solutions by topic, render compact answer/solution cards, package day groups with small native headers and large question bodies, then verify native database/media completeness and layout. Await source clarification for M016 and E006 without blocking all other work. Earlier transcription agents saved partial work and hit quota; remaining transcription was completed locally. User explicitly requested a persistent goal on 2026-09-08; a goal is ACTIVE for the PDF plus MarginNote workflow. Do not mark complete until both requested deliverables are verified.

## Git
This task uses fallback repository progress only. Stage/commit this task file only; never stage unrelated changes. Historical remote authentication failure SEC_E_NO_CREDENTIALS; do not claim upload unless push succeeds.
