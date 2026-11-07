#!/usr/bin/env python3
"""Validation script for Delimit Codex Plugin.

Validates JSON manifests against declared Agent Plugins schemas,
checks plugin directory structure, skills frontmatter, tool references,
and required documentation.
"""

import json
import os
import re
import sys
import urllib.request
import jsonschema

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

RECORDS_TOOLSET = {
    "delimit_memory_search",
    "delimit_memory_store",
    "delimit_memory_recent",
    "delimit_version",
    "delimit_help",
    "delimit_ledger_add",
    "delimit_ledger_update",
    "delimit_ledger_done",
    "delimit_ledger_list",
    "delimit_ledger_context",
    "delimit_handoff_create",
    "delimit_handoff_acknowledge",
    "delimit_handoff_list",
}

EXPECTED_SKILLS = {"handoff", "record", "resume"}
DISALLOWED_SKILLS = {"hand-off", "record-decision", "resume-work", "walkthrough"}

SCHEMA_CACHE = {}


def fetch_schema(url):
    if url in SCHEMA_CACHE:
        return SCHEMA_CACHE[url]
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    SCHEMA_CACHE[url] = data
    return data


def validate_schemas():
    print("==> Validating JSON against declared schemas...")

    plugin_json_path = os.path.join(REPO_ROOT, "plugins", "delimit", "plugin.json")
    with open(plugin_json_path, "r", encoding="utf-8") as f:
        plugin_data = json.load(f)

    plugin_schema = fetch_schema(plugin_data["$schema"])
    jsonschema.validate(instance=plugin_data, schema=plugin_schema)
    print("  [PASS] plugins/delimit/plugin.json conforms to schema")

    mcp_json_path = os.path.join(REPO_ROOT, "plugins", "delimit", "mcp.json")
    with open(mcp_json_path, "r", encoding="utf-8") as f:
        mcp_data = json.load(f)

    mcp_schema = fetch_schema(mcp_data["$schema"])
    jsonschema.validate(instance=mcp_data, schema=mcp_schema)
    print("  [PASS] plugins/delimit/mcp.json conforms to schema")

    # Validate marketplaces
    agents_mkt = os.path.join(REPO_ROOT, ".agents", "plugins", "marketplace.json")
    claude_mkt = os.path.join(REPO_ROOT, ".claude-plugin", "marketplace.json")

    with open(agents_mkt, "r", encoding="utf-8") as f:
        agents_data = json.load(f)
    with open(claude_mkt, "r", encoding="utf-8") as f:
        claude_data = json.load(f)

    assert agents_data == claude_data, "marketplace.json copies must match"
    print("  [PASS] marketplace.json manifests are valid and in sync")


def validate_structure():
    print("==> Validating plugin structure & fields...")

    plugin_json_path = os.path.join(REPO_ROOT, "plugins", "delimit", "plugin.json")
    with open(plugin_json_path, "r", encoding="utf-8") as f:
        plugin_data = json.load(f)

    assert plugin_data.get("name") == "delimit", "plugin.json name must be 'delimit'"
    assert plugin_data.get("version") == "1.0.0", f"version must be 1.0.0, got {plugin_data.get('version')}"
    print("  [PASS] plugin.json name and version (1.0.0) verified")

    mcp_json_path = os.path.join(REPO_ROOT, "plugins", "delimit", "mcp.json")
    with open(mcp_json_path, "r", encoding="utf-8") as f:
        mcp_data = json.load(f)

    server = mcp_data["mcpServers"]["delimit"]
    assert server.get("type") == "stdio", "MCP server type must be 'stdio'"
    assert server.get("command") == "npx", "MCP command must be 'npx'"
    expected_args = ["-y", "delimit-cli@4.23.0", "mcp", "--toolset", "records"]
    assert server.get("args") == expected_args, f"MCP args mismatch: {server.get('args')}"
    print("  [PASS] mcp.json pins delimit-cli@4.23.0 mcp --toolset records")

    skills_dir = os.path.join(REPO_ROOT, "plugins", "delimit", "skills")
    found_skills = set(os.listdir(skills_dir))
    assert found_skills == EXPECTED_SKILLS, f"Skills must be {EXPECTED_SKILLS}, found {found_skills}"

    for disallowed in DISALLOWED_SKILLS:
        assert not os.path.exists(os.path.join(skills_dir, disallowed)), f"Disallowed skill present: {disallowed}"

    for skill_name in EXPECTED_SKILLS:
        skill_file = os.path.join(skills_dir, skill_name, "SKILL.md")
        assert os.path.exists(skill_file), f"Missing {skill_file}"
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
        assert match, f"{skill_file} missing valid YAML frontmatter"
        fm = match.group(1)
        body = match.group(2)

        name_match = re.search(r"^name:\s*(\S+)", fm, re.MULTILINE)
        desc_match = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
        assert name_match and name_match.group(1) == skill_name, f"Wrong name in frontmatter of {skill_file}"
        assert desc_match and len(desc_match.group(1).strip()) > 10, f"Description too short in {skill_file}"

        # Check that any referenced delimit tools are strictly in the records toolset
        tool_refs = re.findall(r"`(delimit_[a-z0-9_]+)`", body)
        for t in tool_refs:
            assert t in RECORDS_TOOLSET, f"Tool `{t}` referenced in {skill_file} is not in records toolset!"

    print(f"  [PASS] Skills {EXPECTED_SKILLS} validated with valid frontmatter & tool references")

    # Required docs
    for doc in ["README.md", "PRIVACY.md", "LICENSE"]:
        p = os.path.join(REPO_ROOT, doc)
        assert os.path.exists(p) and os.path.getsize(p) > 100, f"Missing or empty {doc}"
    print("  [PASS] Required docs (README.md, PRIVACY.md, LICENSE) verified")


def main():
    try:
        validate_schemas()
        validate_structure()
        print("\nAll validation checks PASSED successfully.")
    except Exception as e:
        print(f"\n[FAIL] Validation error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
