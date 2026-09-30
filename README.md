# Delimit for Codex

**Keep the state. Change the model.**

This repo is a Codex plugin marketplace with one plugin, `delimit`. It bundles Delimit's local MCP server and four skills: resume where you left off, record a decision, hand work to another assistant, and a step-by-step walkthrough ("walk me through Delimit") that also works with Codex voice. Delimit keeps persistent memory, a project ledger, and handoffs across assistants.

## Install

```sh
codex plugin marketplace add https://github.com/delimit-ai/codex-plugin
codex plugin add delimit@delimit
codex plugin list --marketplace delimit
```

To try it from a local clone, use `codex plugin marketplace add /path/to/codex-plugin` instead.

## Requirements

- A Codex CLI with `codex plugin` support.
- Delimit installed and initialized with `npx delimit-cli setup` (the walkthrough skill can guide you through it), including its local Python MCP server and dependencies. The bundled launcher uses the Delimit virtual environment when present and falls back to `python3`, as the setup command does.
- A Unix shell (`sh`).

The plugin reads and writes Delimit state in `~/.delimit` through the local stdio server. The marketplace and plugin do not include a hosted server. Model conversations and any data a user chooses to send to an assistant follow that assistant's own data handling.

## Status

- Codex CLI: tested on 0.159.2 (install, server start, and MCP handshake). If `delimit setup` has already configured Delimit for Codex, your existing entry stays in charge and the plugin adds the skills.
- ChatGPT desktop: untested.
- Windows: not supported yet (macOS and Linux).

## License

MIT
