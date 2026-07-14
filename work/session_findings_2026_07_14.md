# 2026-07-14 Visual QA Findings

- The geometric magnitude formula remained too small at 19 pt because the nested products consumed the shared height budget. It now uses 24 pt and a 44 pt display height. The adjacent phase formula uses 19 pt and 34 pt. A 90 pt group reservation keeps both formulas on one page.
- The chapter-one discrete signal plot used a fixed negative vertical-axis tail of about 46 pt, placing the arrow too close to body text. It now uses a 24 pt negative tail; the 180 dpi render shows clear separation.
- The actual `x(1-2n)` figure in the merged PDF comes from `make_dsp_sample_handout_v2.py`, not only the duplicate helper in batch two. Both renderers now use a 150 pt plot, an 18 pt downward shift, and vertical range `[-3.2, 6.4]`.
- Old tests requiring an 82 pt example plot and vertical range `[-4.5, 5.2]` contradicted the latest user requirement. They were updated to the new explicit geometry rather than skipped.
