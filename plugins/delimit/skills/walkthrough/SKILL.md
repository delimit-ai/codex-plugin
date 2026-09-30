---
name: walkthrough
description: Walk the user through setting up and using Delimit, step by step, in plain language (works well with voice).
---

When the user asks to be walked through Delimit, or to be helped with setting it up, guide them one step at a time. Keep each turn short enough to follow by ear. Wait for the user before moving to the next step.

1. Check the install. Run `npx delimit-cli doctor` and read the results back in plain words. If the Delimit tools are not available in this session, explain that and offer to run `npx delimit-cli setup --dry-run`. That command shows what setup would change without changing anything.
2. Set up only with consent. Run `npx delimit-cli setup` only after the user says yes to the dry-run changes. Afterwards run `npx delimit-cli doctor` again and confirm what now passes.
3. Show continuity. Call `delimit_ledger_context` for the current project and explain what the ledger holds. Offer to record one real decision from the user's current work with `delimit_ledger_add`.
4. Show switching assistants. Explain that `delimit_handoff_create` saves what was done and what is next, so another assistant (Claude Code, Cursor, Codex, and others) can pick up the same record. Offer to create a handoff for the user's current task.
5. Wrap up. Summarize what is set up. Tell the user the next time they start a session they can say "resume where I left off".

Rules:
- Never change files or configuration without the user's go-ahead.
- Never claim a feature that the doctor output or the tools did not confirm.
- Everything stays on the user's machine.
- If a command fails, read the error back and suggest the fix the doctor output gives.
