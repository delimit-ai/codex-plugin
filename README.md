# Delimit for Codex

**Keep the state. Change the model.**

This repository is a Codex plugin marketplace containing the `delimit` plugin. It bundles Delimit's local stdio MCP server (`records` toolset) and three skills: resume where you left off, record a decision or task, and hand work to another assistant. Delimit maintains persistent memory, a project ledger, and handoff receipts across AI coding assistants (Codex, Claude Code, Cursor, Antigravity, and others).

## Getting Started

Once installed, use these prompts in your Codex session:

- **Resume open work**: Say `"resume where I left off"` or `"show open work"`. Codex calls `delimit_ledger_context` and `delimit_handoff_list` to summarize open tasks, decisions, unfinished work, and next actions.
- **Record a decision or task**: Say `"record decision: <decision>"` or `"record task: <task>"`. Codex calls `delimit_ledger_add` to store the item durably in the local ledger.
- **Hand off to another assistant**: Say `"create a handoff"` or `"prepare handoff"`. Codex updates the ledger items with `delimit_ledger_update` / `delimit_ledger_done` and creates a handoff receipt with `delimit_handoff_create`.

## Install

Install from the GitHub repository marketplace:

```sh
codex plugin marketplace add delimit-ai/codex-plugin
codex plugin add delimit@delimit
```

To install from a local clone:

```sh
codex plugin marketplace add /path/to/codex-plugin
codex plugin add delimit@delimit
```

Verify the installation:

```sh
codex plugin list
codex mcp list
```

To remove the plugin:

```sh
codex plugin remove delimit@delimit
```

## Requirements

- **Codex CLI**: `codex-cli 0.167.0` or later (or ChatGPT desktop app with plugin support).
- **Node.js**: Node 18+ (`npx` is used to launch the pinned `delimit-cli@4.23.0` server).
- **Network**: Internet access is needed on first run to download `delimit-cli@4.23.0` from npm. Once cached, the server runs completely offline.

## Storage Location

- All records stay local on your machine under `~/.delimit`.
- **Ledger entries**: stored as plain JSON/JSONL files in `~/.delimit/ledger/`.
- **Handoff receipts**: stored in `~/.delimit/handoffs/`.
- **Runtime cache**: isolated Python virtual environment under `~/.delimit/plugin-server/4.23.0/`.
- No data is transmitted to Delimit servers. See [PRIVACY.md](PRIVACY.md).

## Automatic Resume Pointer

The Codex plugin requires explicit prompt invocation (`"resume where I left off"`) because the Codex CLI plugin specification does not run automatic session-start hooks by default.

For automated session-start resume and global governance across CLI sessions:

```sh
npm install -g delimit-cli
delimit setup
```

What `delimit setup` configures for Codex in `delimit-cli 4.23.0`:
- **`~/AGENTS.md`**: Installs or updates the Delimit Consensus 123 governance block in `~/AGENTS.md`. Codex CLI automatically traverses parent directories and loads `AGENTS.md` from CWD up to your user home directory, instructing the model to invoke `delimit_revive` and `delimit_ledger_context` at session start.
- **`~/.delimit/shims/codex`**: Installs a command launcher shim in `~/.delimit/shims` (prepended to `PATH`) that can inject revived session state directly as the initial prompt when transitioning between assistants.
- **`~/.codex/config.toml`**: Registers the full local Delimit Python MCP server under `[mcp_servers.delimit]` with `approval_policy = "never"` and a 30-minute tool execution ceiling.

## License

MIT. See [LICENSE](LICENSE).
