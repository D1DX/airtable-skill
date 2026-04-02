# Airtable Skill for Claude Code

[![Author](https://img.shields.io/badge/Author-Daniel_Rudaev-000000?style=flat)](https://github.com/daniel-rudaev)
[![Studio](https://img.shields.io/badge/Studio-D1DX-000000?style=flat)](https://d1dx.com)
[![Airtable](https://img.shields.io/badge/Airtable-Skill-18BFFF?style=flat&logo=airtable&logoColor=white)](https://airtable.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](./LICENSE)

Unified Airtable skill for Claude Code. 6 access methods with a decision tree, covering MCP, REST API, internal web API, Omni AI, scripting, formulas, webhooks, and automations. Built from real production work at [D1DX](https://d1dx.com).

## What's Included

| Topic | What it covers |
|-------|---------------|
| Method Decision Tree | When to use MCP vs REST API vs Internal API vs Omni AI vs Scripting |
| MCP | Tool reference, detail levels, safe vs write operations |
| Omni AI | Capabilities the API can't do — field configs, interfaces, automations, Field Agents |
| REST API | Batch limits, upsert, webhooks (create, poll, HMAC), pagination |
| Internal Web API | Reverse-engineered endpoints — Interface Designer layout, visibility filters, automation export, ID prefixes |
| Scripting API | Standalone vs Automation context, batch limits (50 not 10), field value type differences |
| Automations | Trigger/action types, duplicate automation prevention, latency notes |
| Formulas | Text, date, regex (RE2), arrays, logic functions, filterByFormula patterns |
| Field Types | REST vs Scripting JSON differences for every field type |
| Gotchas | 20 hard-won lessons — attachment URL expiry, checkbox null, Buddhist Era dates, msgpack responses |

## Install

### Claude Code (CLI or IDE)

```bash
# Clone
git clone https://github.com/D1DX/airtable-skill.git

# Copy to Claude Code skills
cp -r airtable-skill ~/.claude/skills/airtable
```

Or add as a git submodule in your own skills repo:

```bash
git submodule add https://github.com/D1DX/airtable-skill.git path/to/skills/airtable
```

### Verify

Start a new Claude Code session. The skill should appear in the skill list as `airtable`. Test with `/airtable` or ask any Airtable-related question.

## Structure

```
airtable-skill/
├── SKILL.md                  — Main skill (auto-triggers on Airtable tasks)
├── interface-api.md          — Full internal web API spec (Interface Designer, readQueries)
├── reference.md              — Quick reference tables
└── extract_automations.py    — Script to export automations via internal API
```

## Recommended: Airtable MCP Server

This skill works standalone but is designed to pair with an Airtable MCP server for live base access. The skill provides knowledge; the MCP provides record operations.

Compatible MCP servers:

| MCP Server | What it adds |
|-----------|-------------|
| [airtable/airtable-mcp](https://github.com/airtable/airtable-mcp) | Official — record CRUD, schema, search, comments, attachments |

## Sources

- **REST API & Scripting:** Verified against [Airtable Web API docs](https://airtable.com/developers/web/api/introduction) and production usage (60+ bases).
- **Internal Web API:** Reverse-engineered from browser traffic (HAR captures, March 2026). Endpoints may change without notice.
- **Omni AI:** Capabilities verified from [official Airtable documentation](https://support.airtable.com/docs/using-omni-ai-in-airtable) (April 2026).
- **Formulas:** Verified against [Airtable formula reference](https://support.airtable.com/docs/formula-field-reference).

## Credits

Built by [Daniel Rudaev](https://github.com/daniel-rudaev) at [D1DX](https://d1dx.com).

## License

MIT License — Copyright (c) 2026 Daniel Rudaev @ D1DX
