# Local Verification (2026-11-07)

All verification tests below were executed in an isolated, throwaway temporary directory at `/tmp/codex-live-verify-2e2exu5n`.
Neither `/root/.codex` nor `/root/.delimit` was accessed or modified.
Codex version: `codex-cli 0.167.0`.

| Check | Result | Detail |
| --- | --- | --- |
| Schema validation | PASS | `plugin.json` and `mcp.json` validate against Agent Plugins 1.0.0 schemas |
| Structure validation | PASS | Skills, manifests, required docs (`README.md`, `PRIVACY.md`, `LICENSE`) verified via `scripts/validate.py` |
| Add local marketplace | PASS | `codex plugin marketplace add <path> --json` |
| Install `delimit@delimit` | PASS | `codex plugin add delimit@delimit --json` installed version 1.0.0 |
| Plugin list | PASS | `codex plugin list` confirms `delimit@delimit` status: `installed, enabled` |
| Cache inspection | PASS | Cache contains `plugin.json`, `mcp.json`, `PRIVACY.md`, and skills (`resume`, `record`, `handoff`) |
| MCP registration | PASS | `codex mcp list` and `codex mcp get delimit --json` show pinned `npx -y delimit-cli@4.23.0 mcp --toolset records` |
| MCP handshake (initialize) | PASS | Server returns JSON-RPC 2.0 `initialize` response (`name: delimit`, `version: 4.23.0`, `protocolVersion: 2024-11-05`) |
| MCP tools/list | PASS | Server exposes all 13 tools of the `records` toolset |
| Interactive turn test | NOTE | `codex exec` requires active OpenAI credentials (returns 401 Unauthorized without auth); MCP server was tested directly |
| Plugin removal | PASS | `codex plugin remove delimit@delimit --json` successfully uninstalls and cleans state |

---

## Live Command Outputs

### 1. Isolated Test Environment

```text
HOME=/tmp/codex-live-verify-2e2exu5n
CODEX_HOME=/tmp/codex-live-verify-2e2exu5n/.codex
DELIMIT_HOME=/tmp/codex-live-verify-2e2exu5n/.delimit
codex-cli 0.167.0
```

### 2. Marketplace Addition & Listing

```text
$ codex plugin marketplace add /home/agent-worktrees/codex-plugin-final --json
{
  "marketplaceName": "delimit",
  "installedRoot": "/home/agent-worktrees/codex-plugin-final",
  "alreadyAdded": false
}

$ codex plugin marketplace list
MARKETPLACE  ROOT
delimit      /home/agent-worktrees/codex-plugin-final
```

### 3. Plugin Installation & Status

```text
$ codex plugin add delimit@delimit --json
{
  "pluginId": "delimit@delimit",
  "name": "delimit",
  "marketplaceName": "delimit",
  "version": "1.0.0",
  "installedPath": "/tmp/codex-live-verify-2e2exu5n/.codex/plugins/cache/delimit/delimit/1.0.0",
  "authPolicy": "ON_INSTALL"
}

$ codex plugin list
Marketplace `delimit`
/home/agent-worktrees/codex-plugin-final/.agents/plugins/marketplace.json

PLUGIN           STATUS              VERSION  SOURCE
delimit@delimit  installed, enabled  1.0.0    /home/agent-worktrees/codex-plugin-final/plugins/delimit
```

### 4. Cached Plugin Files

```text
Cached files in /tmp/codex-live-verify-2e2exu5n/.codex/plugins/cache/delimit/delimit/1.0.0:
 - PRIVACY.md
 - mcp.json
 - plugin.json
 - skills/handoff/SKILL.md
 - skills/record/SKILL.md
 - skills/resume/SKILL.md
```

### 5. MCP Server Registration in Codex

```text
$ codex mcp list
Name     Command  Args                                         Env                                   Cwd                                                                         Status   Auth       
delimit  npx      -y delimit-cli@4.23.0 mcp --toolset records  PLUGIN_DATA=*****, PLUGIN_ROOT=*****  /tmp/codex-live-verify-2e2exu5n/.codex/plugins/cache/delimit/delimit/1.0.0  enabled  Unsupported

$ codex mcp get delimit --json
{
  "name": "delimit",
  "enabled": true,
  "disabled_reason": null,
  "transport": {
    "type": "stdio",
    "command": "npx",
    "args": [
      "-y",
      "delimit-cli@4.23.0",
      "mcp",
      "--toolset",
      "records"
    ],
    "env": {
      "PLUGIN_DATA": "/tmp/codex-live-verify-2e2exu5n/.codex/plugins/data/agent-plugins/da709643ddda3e9acfd174b0ff33b50db9d1162e84b36bdf02ad903da4783d8c",
      "PLUGIN_ROOT": "/tmp/codex-live-verify-2e2exu5n/.codex/plugins/cache/delimit/delimit/1.0.0"
    },
    "env_vars": [],
    "cwd": "/tmp/codex-live-verify-2e2exu5n/.codex/plugins/cache/delimit/delimit/1.0.0"
  },
  "enabled_tools": null,
  "disabled_tools": null,
  "startup_timeout_sec": null,
  "tool_timeout_sec": null
}
```

### 6. MCP Protocol Handshake & Tool Listing

Invoking `npx -y delimit-cli@4.23.0 mcp --toolset records` directly over stdio:

#### JSON-RPC 2.0 Initialize Response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "experimental": {},
      "logging": {},
      "prompts": {
        "listChanged": false
      },
      "resources": {
        "subscribe": false,
        "listChanged": false
      },
      "tools": {
        "listChanged": true
      },
      "extensions": {
        "io.modelcontextprotocol/ui": {}
      }
    },
    "serverInfo": {
      "name": "delimit",
      "version": "4.23.0"
    }
  }
}
```

#### JSON-RPC 2.0 tools/list Response:
All 13 tools exposed by the `records` toolset:
1. `delimit_memory_search`
2. `delimit_memory_store`
3. `delimit_memory_recent`
4. `delimit_version`
5. `delimit_help`
6. `delimit_ledger_add`
7. `delimit_ledger_update`
8. `delimit_ledger_done`
9. `delimit_ledger_list`
10. `delimit_ledger_context`
11. `delimit_handoff_create`
12. `delimit_handoff_acknowledge`
13. `delimit_handoff_list`

### 7. Codex Interactive Exec Turn (Credential Requirement)

```text
$ codex exec --skip-git-repo-check show open work
[STDERR]: OpenAI Codex v0.167.0
--------
workdir: /home/agent-worktrees/codex-plugin-final
model: gpt-6.1-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 01a1b810-b96e-79f2-a30d-0f0f7d99fbd6
--------
user
show open work
2026-11-07T22:11:06.262430Z ERROR codex_api::endpoint::responses_websocket: failed to connect to Responses WebSocket stage=Unknown
...
ERROR: unexpected status 401 Unauthorized: Missing bearer or basic authentication in header, url: https://api.openai.com/v1/responses
```

*Note: Codex turns against OpenAI endpoints require an authenticated account/API key. The local MCP server integration was tested directly and operates completely offline once installed.*

### 8. Plugin Removal

```text
$ codex plugin remove delimit@delimit --json
{
  "pluginId": "delimit@delimit",
  "name": "delimit",
  "marketplaceName": "delimit"
}

$ codex plugin list
Marketplace `delimit`
/home/agent-worktrees/codex-plugin-final/.agents/plugins/marketplace.json

PLUGIN           STATUS         VERSION  SOURCE
delimit@delimit  not installed           /home/agent-worktrees/codex-plugin-final/plugins/delimit
```
