# Format and Source Notes

## 1. Primary Sources & OpenAI Documentation (2026-11-07)

### Documentation URLs

1. **Package your plugin**: [https://developers.openai.com/plugins/build/plugins](https://developers.openai.com/plugins/build/plugins) (markdown source: `https://developers.openai.com/plugins/build/plugins.md`)
2. **Upload and submit your plugin**: [https://developers.openai.com/plugins/deploy/submission](https://developers.openai.com/plugins/deploy/submission) (markdown source: `https://developers.openai.com/plugins/deploy/submission.md`)
3. **Submit desktop-only plugins**: [https://developers.openai.com/plugins/deploy/desktop-only](https://developers.openai.com/plugins/deploy/desktop-only) (markdown source: `https://developers.openai.com/plugins/deploy/desktop-only.md`)
4. **Local CLI help**: `codex-cli 0.167.0` (`codex plugin --help`, `codex plugin marketplace --help`, `codex plugin marketplace add --help`, `codex plugin add --help`, `codex mcp --help`)

---

### Official Plugin Directory & Submission / Review Process Report

**Does OpenAI now have an official plugin directory / submission or review process for Codex plugins?**
**YES.** OpenAI operates a unified, universal plugin directory shared by ChatGPT and Codex.

#### Directory & Review Process Overview
- **Universal Directory**: Public plugins published to the directory appear in both ChatGPT and Codex. The submission dashboard is located at `https://platform.openai.com/plugins`.
- **Submission Prerequisites**:
  - Submitter must be an Organization Owner or have the **Apps Management Write** role under Organization Roles (`https://platform.openai.com/settings/organization/people/roles`).
  - The organization or individual must complete identity verification under Organization Settings (`https://platform.openai.com/settings/organization/general`).
- **Submission Workflow**:
  1. **Upload ZIP**: Developer uploads the packaged plugin as a ZIP archive at `https://platform.openai.com/plugins` under their verified developer identity.
  2. **Automated Validation**: The platform runs automated scans in two categories:
     - **Metadata & Skills**: Scans `plugin.json` schema compliance, verified author identity URLs, and skill instruction safety / quality guidelines.
     - **MCPs**: Scans the MCP connection, tool schema, and endpoint reachability.
  3. **Issue Resolution**: Any detected issues must be resolved before proceeding. Updated ZIPs can be re-uploaded.
  4. **Human / Review Submission**: Once automated checks pass, the draft is submitted for review.
  5. **Publication**: Upon approval, the developer chooses when to publish from the portal dashboard.
  6. **Live Updates**: Post-publication, tool changes on a remote hosted server update automatically; metadata or skill changes require a new ZIP submission.

#### Requirements by Plugin Architecture
- **Remote MCP Plugins**:
  - Must declare a stable, public HTTPS endpoint.
  - Must complete domain verification and OAuth (or supported authentication).
  - Only one MCP server may be connected per plugin.
- **Local MCP / Desktop-Only Plugins (e.g. Delimit stdio)**:
  - Display a **Desktop only** badge in the directory.
  - Can only be installed from the ChatGPT desktop app and run in local threads.
  - **Approval Restriction**: *"Approval required: Local MCP submissions are limited to approved partners. Contact your OpenAI representative to confirm eligibility and have your submitting organization allowlisted before following these steps."*
  - **Submission Path**: Once allowlisted, authors select **Skills only** in the portal and upload the plugin ZIP containing the local stdio MCP declaration (`mcp.json` with `"type": "stdio"`).
  - For skills-only plugins requiring local desktop execution without an MCP server, the manifest declares `"requires_local_executor": true` under `extensions.com.openai` in `plugin.json`.
- **Independent Distribution (Repo & Local Marketplaces)**:
  - Codex CLI (`0.167.0`) supports direct installation from Git repository marketplaces (`codex plugin marketplace add <owner/repo>`) and local paths (`codex plugin marketplace add <path>`) without submitting to the OpenAI directory.

---

## 2. Local CLI Evidence on `codex-cli 0.167.0`

### Subcommands & Syntax
- `codex --version`: `codex-cli 0.167.0`
- `codex plugin marketplace add <SOURCE>`:
  - Accepts local path (`./path/to/marketplace`), GitHub shorthand (`delimit-ai/codex-plugin`), or HTTPS Git URL.
  - Optional `--ref <REF>` to pin branch or tag.
  - Optional `--sparse <PATH>` for sparse checkouts.
- `codex plugin add <PLUGIN[@MARKETPLACE]>`:
  - Accepts `delimit@delimit` (or `delimit --marketplace delimit`).
- `codex plugin list`:
  - Displays configured marketplaces and installed plugins.
- `codex mcp list`:
  - Lists registered MCP servers, transport command, args, cwd, and status.
- `codex plugin remove <PLUGIN[@MARKETPLACE]>`:
  - Uninstalls plugin and clears cache.

---

## 3. MCP Launch Migration: `delimit-cli@4.23.0` (`records` toolset)

In `v0.1.0`, the plugin relied on a shell launcher (`sh -c ...`) requiring a prior `npx delimit-cli setup` to create `~/.delimit/server/ai/server.py` and a virtual environment.

In `1.0.0`, the plugin switches to a direct, pinned launcher in `mcp.json`:
```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "delimit": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "delimit-cli@4.23.0",
        "mcp",
        "--toolset",
        "records"
      ]
    }
  }
}
```

### Verified Tools in `records` Toolset
Tested via MCP JSON-RPC 2.0 `initialize` and `tools/list`:
1. `delimit_memory_search` (Pro semantic search)
2. `delimit_memory_store` (Durable memory storage)
3. `delimit_memory_recent` (Chronological memory tail)
4. `delimit_version` (Server version and environment report)
5. `delimit_help` (Tool documentation and workflows)
6. `delimit_ledger_add` (Add task or decision to ledger)
7. `delimit_ledger_update` (Update ledger item fields/status)
8. `delimit_ledger_done` (Close out ledger item)
9. `delimit_ledger_list` (Filter and list ledger items)
10. `delimit_ledger_context` (Top open work summary)
11. `delimit_handoff_create` (Create cross-assistant handoff receipt)
12. `delimit_handoff_acknowledge` (Acknowledge handoff receipt)
13. `delimit_handoff_list` (List pending/acknowledged handoffs)

---

## 4. Skills & Parity with Claude Plugin

The plugin aligns with the approved Claude plugin structure and naming:

| Skill | Explicit-Invocation Description | Tools Called |
| --- | --- | --- |
| `resume` | "Use at the start of a session, when the user asks to see open work, or when switching assistants mid-project." | `delimit_ledger_context`, `delimit_handoff_list` |
| `record` | "Use when the user explicitly asks to record a stated decision or task in the Delimit ledger." | `delimit_ledger_add` |
| `handoff` | "Use when the user asks for a handoff or a work session reaches a stopping point." | `delimit_ledger_update`, `delimit_ledger_done`, `delimit_handoff_create` |

All 6 tools referenced by the skills exist in the 13 tools provided by the `records` toolset. Note that `delimit_revive` (used in v0.1.0) is not in the `records` toolset and has been replaced by `delimit_ledger_context` + `delimit_handoff_list`.

### Walkthrough Skill Audit
The legacy `walkthrough` skill from v0.1.0 claimed voice capability ("works well with voice") and instructed the agent to offer `npx delimit-cli setup --dry-run` if Delimit tools were not available in the session.
Because:
1. Codex CLI does not support voice interaction.
2. The plugin bundles and runs the MCP server directly via `npx -y delimit-cli@4.23.0 mcp --toolset records`, making tools immediately available without running setup.
3. The approved Claude plugin does not ship `walkthrough`.

The `walkthrough` skill was removed to maintain strict claim integrity and 1:1 parity with the Claude plugin.

---

## 5. Audit of `delimit setup` for Codex in `delimit-cli 4.23.0`

Audit of `/usr/lib/node_modules/delimit-cli/lib/cross-model-hooks.js`, `bin/delimit-setup.js`, and `lib/chat-repl.js`:
1. `~/AGENTS.md`: `delimit setup` writes the Delimit Consensus 123 instruction block to `~/AGENTS.md`. Codex CLI automatically traverses parent directories and loads `AGENTS.md` up to the user home directory.
2. `~/.delimit/shims/codex`: Installs a launcher wrapper in `~/.delimit/shims/` prepended to `PATH` that can inject revived session state directly as the initial prompt when transitioning between assistants.
3. `~/.codex/config.toml`: Registers `[mcp_servers.delimit]` pointing to the local Python MCP server with `approval_policy = "never"` and `tool_timeout_sec = 1800`.
