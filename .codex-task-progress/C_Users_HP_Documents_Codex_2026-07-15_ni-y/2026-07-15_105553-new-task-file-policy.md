# New Task File Policy

- Created: 2026-07-15 10:55:53 Asia/Shanghai
- Task path: `C:\Users\HP\Documents\Codex\2026-07-15\ni-y`
- Objective: Require every new task to create its own appropriately named progress file and write the task into that file.
- Decisions:
  - Filename format: `YYYY-MM-DD_HHmmss-short-task-slug.md`.
  - Git-backed projects store task files under `.codex/tasks/`.
  - Non-Git tasks store task files under the designated fallback repository's path-isolated `.codex-task-progress/` directory.
  - Context recovery reads the current task's own file instead of a shared progress file.
- Completed:
  - Updated the global Codex instructions with the per-task file policy.
- Verification:
  - Confirmed the global instructions require a unique timestamped file for every new task.
  - Confirmed only this new task file is untracked in the fallback repository.
- Remaining: None.
- Next action: On the next new task, create its own timestamped descriptive file before substantive work.
