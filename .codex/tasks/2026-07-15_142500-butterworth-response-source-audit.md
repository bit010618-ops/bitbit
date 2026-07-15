# Task: Butterworth response source audit

## Objective

Compare `draw_butterworth_response` against its original PPT page and current batch-9 rendering, preserving every source indicator, cutoff line, label, color, and spacing without collisions.

## Recovery Evidence

- Previous verified item: periodic digital ideal responses, commit `fa350e6`.
- Current tests: `20 passed`.
- Stable full-book PDF remains unchanged.

## Exact Next Action

Completed. The source dark-filled dB badges and the complete cutoff-frequency definition were restored.

## Verification

- Tests: `21 passed` in `work/test_iir_structure_source_topology.py`.
- Source: `tmp/pdfs/audit_source/iir-28.png`.
- Render: `tmp/pdfs/iir_preview/butterworth-source-candidate-11.png`.
- Stable full-book PDF was not replaced.

## Next Action

Start a new task for `draw_butter_table`, the next unverified matrix item.
