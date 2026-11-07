# Privacy & Local Storage

The plugin starts `npx -y delimit-cli@4.23.0 mcp --toolset records` locally. The records tools read and write ledger and handoff data in plain JSON and JSONL files under `~/.delimit`; those files belong to you. The launcher also stores its own server copy and Python venv under `~/.delimit/plugin-server/4.23.0`. It does not change Claude, Codex, or other assistant configuration files.

On first launch, `npx` fetches `delimit-cli` from the npm registry and `pip` may fetch the server's Python requirements from the Python package index. The records tools themselves do not send record contents to an external service. Codex processes the content you choose to share under its own terms.

Uninstalling the plugin (`codex plugin remove delimit@delimit`) leaves `~/.delimit` untouched. Inspect and delete that directory yourself if you want to remove the records.

## Where records live

- Records are kept in one local ledger under `~/.delimit/ledger/`. Each record is tagged with the project it was created in: the repository name or directory fallback; temporary scratch projects use `unsorted`. Listing shows records from all projects; the tag tells you where each one came from.
- Handoff receipts are stored locally under `~/.delimit/handoffs/`.
- Once installed, the records workflow runs with no network access. We tested it in a network-isolated environment.
