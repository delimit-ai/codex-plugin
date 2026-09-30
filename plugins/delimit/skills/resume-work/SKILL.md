---
name: resume-work
description: Resume work using Delimit's saved session state and project ledger.
---

When asked to resume where the user left off, call `delimit_revive` with the current project's path, then `delimit_ledger_context` for that project. Summarize the last known state and open ledger work. Check the current worktree before taking action; saved context may be older than the files.
