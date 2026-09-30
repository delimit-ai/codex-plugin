---
name: record-decision
description: Record a durable decision in Delimit.
---

When asked to record a decision, capture the decision and its reason. Use `delimit_memory_store` for cross-session context. If it belongs to a project's strategy ledger, use `delimit_ledger_add` with `ledger="strategy"` and a clear title. Report the stored result; do not claim success if a tool fails.
