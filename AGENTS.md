# DSP Handout Project Instructions

## Context Recovery

- Before editing, generating PDFs, or reporting progress, read `work/PROJECT_CHECKPOINT.md`.
- Verify the checkpoint against `git status --short`, `git log -5 --oneline`, and the latest rendered PNGs on disk.
- Chat screenshots are evidence of defects, not evidence that a change was completed.
- Never repeat a completed action after context compaction unless disk or tests show it is necessary.

## Progress Recording

- After every verified work unit, update `work/PROJECT_CHECKPOINT.md` with completed work, current failures, tests, rendered preview paths, and the exact next step.
- Commit and push each verified work unit to `origin` so later sessions can recover from Git history.
- If a checkpoint is intentionally incomplete, use a commit message beginning with `WIP:` and list the remaining failures in the checkpoint.
- Do not replace the stable full-book PDF until the affected pages pass tests and visual inspection.

## PDF Verification

- Compare diagrams against the original PDF/PPT page before marking them verified.
- Render affected PDF pages to PNG and inspect them visually.
- A structural test passing is not sufficient when labels, arrows, frames, or spacing are visibly wrong.
