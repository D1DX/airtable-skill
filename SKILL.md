---
name: airtable
description: Unified Airtable skill — MCP, public REST API, internal web API, Omni AI, scripting, formulas, webhooks, automations, field types, and gotchas. Auto-triggers on any Airtable task.
disable-model-invocation: false
user-invocable: true
argument-hint: "task description"
---

# Airtable — Unified Skill

Everything needed to work with Airtable: 6 methods, each with different strengths.

**As of April 2026.** API keys deprecated Feb 2024 — use PATs only.

---

## 1. Method Decision Tree

```
I need to read/write records
  → MCP available? → Use MCP (preferred — handles auth, pagination, batching)
  → No MCP?       → Public REST API with PAT

I need schema info (tables, fields, types)
  → MCP describe_table (detailLevel: full)

I need field configurations (formula text, rollup aggregation, lookup source)
  → MCP describe_table may include it (base-size dependent)
  → If not: Omni AI — ask it to list calculated field configs

I need to create/modify formulas, rollups, lookups, or buttons
  → Omni AI (natural language) — API support is very limited

I need to build or modify interfaces
  → Omni AI (creates full pages + AI-generated custom elements)
  → API has zero interface-building capability

I need to create automations
  → Omni AI or Airtable UI — no API for automation creation

I need interface page layout, visibility conditions, element structure
  → Internal Web API: readDraft

I need to query data as the interface sees it (with interface filters)
  → Internal Web API: readQueries

I need to export automation definitions
  → Internal Web API: application/read + workflow/read

I need to run logic inside Airtable
  → Scripting Extension (standalone) or Automation Script (triggered)

I need real-time change notifications
  → Public REST API: Webhooks

I need to build a formula
  → See Section 8: Formulas
```

---

## 2. MCP (Preferred for Records)

MCP wraps the REST API with structured tools. Always prefer when available.

### Tools

| Tool | Purpose | Safe? |
|------|---------|-------|
| `list_bases` | List all accessible bases | Read |
| `list_tables` | Tables in a base (3 detail levels) | Read |
| `describe_table` | Full field schema | Read |
| `list_records` | Read with filters | Read |
| `get_record` | Single record | Read |
| `search_records` | Full-text search | Read |
| `create_record` | Create record | **Write** |
| `update_records` | Update records | **Write** |
| `delete_records` | Delete records | **Destructive** |
| `create_table` / `create_field` / `update_field` / `update_table` | Schema changes | **Write** |
| `list_comments` / `create_comment` | Record comments | Read / **Write** |
| `upload_attachment` | Attach file | **Write** |

### Detail Level Optimization

| Level | Returns | When |
|-------|---------|------|
| `tableIdentifiersOnly` | Table IDs + names | Listing tables |
| `identifiersOnly` | + field + view IDs/names | Field references |
| `full` | + field types, descriptions, configs | Schema docs, type verification |

**Tip:** For large bases, use `tableIdentifiersOnly` first, then `describe_table full` on specific tables.

---

## 3. Omni AI

Airtable's built-in AI assistant (bottom-right of base UI). Can do things no API can.

### Capabilities (from official Airtable docs)

| Capability | Omni | REST API |
|---|---|---|
| Create/modify formula fields (natural language) | **Yes** | Very limited |
| Create/modify rollup/lookup fields | **Yes** | Limited |
| Build interfaces (full pages + AI-generated custom elements) | **Yes** | No |
| Create automations | **Yes** | No |
| Create complete apps (tables + interfaces + automations) | **Yes** | No |
| Web research (Field Agents — auto-run on data change) | **Yes** | No |
| Document analysis (Field Agents) | **Yes** | No |
| Data analysis / insights | **Yes** | No |
| Read/write records | **Yes** | Yes |

### AI-Generated Interface Elements

Beyond standard elements — Omni can generate custom bespoke elements: 3D viewers, heatmaps, relationship diagrams, geographic visualizations, infinite canvas tools.

### Field Agents

AI-powered fields that auto-run when data changes — analyze documents, search the web, generate images, translate content, extract insights.

### Access

- Via browser: open base → Omni chat (bottom-right)
- Via Chrome MCP / Claude Desktop: navigate to base → Omni chat → submit prompt
- Manual fallback: user pastes prompt, copies response back

### Cost

App building: free. Data analysis questions: 10 credits per response. Model choice: OpenAI, Anthropic, Meta, others.

### When to use Omni over API

- Need to read field configurations that MCP doesn't return (formula text, rollup aggregation functions, lookup source details)
- Need to create or modify calculated fields
- Need to build or modify interfaces
- Need to set up automations

---

## 4. Public REST API

**Base URL:** `https://api.airtable.com/v0/{baseId}/{tableIdOrName}`
**Auth:** `Authorization: Bearer <PAT>`

Claude knows REST API patterns — only non-obvious specifics here:

### Key Parameters (List Records)

`fields[]`, `filterByFormula`, `maxRecords`, `pageSize` (max 100), `sort[0][field]`, `sort[0][direction]`, `view`, `offset`, `returnFieldsByFieldId`, `recordMetadata[]=commentCount`.

**Pagination:** Response includes `offset` if more records. No `offset` = last page.

### Batch Limits

- Create/Update/Delete: **max 10 records per request**
- `typecast: true` — auto-creates select options, converts types. Without it, invalid values return 422.
- **PATCH** updates specified fields only. **PUT** clears everything not specified — almost always use PATCH.

### Upsert

```json
{
  "performUpsert": {"fieldsToMergeOn": ["Email"]},
  "records": [{"fields": {"Email": "user@d1dx.com", "Name": "Updated"}}],
  "typecast": true
}
```

Rules: 1-3 merge fields, must have unique values. Supported: singleLineText, email, number, autoNumber, barcode.

### Webhooks

- **Create:** POST to `/v0/bases/{baseId}/webhooks` — save `macSecretBase64` immediately (only returned on creation)
- **Poll:** `GET /v0/bases/{baseId}/webhooks/{webhookId}/payloads?cursor={n}`
- **Refresh:** expires every 7 days — refresh daily
- **HMAC:** `hmac-sha256=` + HMAC-SHA256(rawBody, base64decode(secret)) — compare with `X-Airtable-Content-MAC` header

---

## 5. Internal Web API (Unofficial)

Reverse-engineered from browser traffic. Cookie-based auth.

**Full spec:** `~/.claude/skills/airtable/interface-api.md`

### Authentication

Session cookies from authenticated browser. Key cookie: `__Host-airtable-session`.

Required headers: `x-airtable-application-id` (base ID), `x-airtable-inter-service-client` (`webClient`), `x-airtable-page-load-id`, `x-requested-with` (`XMLHttpRequest`), `x-time-zone`, `x-user-locale`, `cookie`.

**Capture:** DevTools → Network → filter XHR → copy Cookie from any `airtable.com/v0.3/` request.

### Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /v0.3/application/{baseId}/read?includeAllData=true` | Full base schema + automation IDs |
| `GET /v0.3/page/{pageId}/readDraft?stringifiedObjectParams={"expectedPageLayoutSchemaVersion":26}` | Interface page layout, elements, visibility |
| `POST /v0.3/application/{baseId}/readQueries` | Query data as interface sees it (with filters) |
| `GET /v0.3/workflow/{workflowId}/read` | Read automation definition |
| `GET /v0.3/workflowDeployment/{deploymentId}/read` | Read automation deployment |

### Interface Element Types

`cellEditor` (field display), `sectionGridRow` (layout), `section` (visual group with visibility), `button`, `queryContainer` (filtered list), `levels` (hierarchy), `text`, `attachmentCarousel`, `rowActivityFeed`, `recordContainer` (root).

### Visibility Filter Syntax

```json
{
  "conjunction": "and",
  "filterSet": [
    {"columnId": "fld...", "operator": "isAnyOf", "value": ["sel...", "sel..."]},
    {"columnId": "fld...", "operator": "isEmpty", "value": null}
  ]
}
```

Operators: `isAnyOf`, `isNoneOf`, `=`, `|` (linked record exists), `isEmpty`, `isNotEmpty`.

### ID Prefix Reference

| Prefix | Entity |
|--------|--------|
| `app` | Base |
| `tbl` | Table |
| `fld` | Field |
| `viw` | View |
| `rec` | Record |
| `sel` | Select option |
| `pag` | Interface page |
| `pbd` | Interface (dashboard) |
| `pel` | Page element |
| `qry` | Query |

---

## 6. Scripting API

Available in Scripting Extension (standalone) and Automation "Run script" actions.

### Standalone vs Automation

| Feature | Standalone | Automation |
|---------|-----------|------------|
| User interaction | `input.buttonsAsync()`, `input.textAsync()` | None — headless |
| Trigger data | None | `input.config()` |
| Timeout | 30 seconds | 30 seconds |
| Output | `output.text()`, `output.table()` | `output.set(key, value)` |
| Batch limit | 50 records | 50 records |

### Key Differences from REST API

- **Batch limit is 50** (not 10 like REST)
- **Single select:** `{name: 'Active'}` (not plain string like REST)
- **Multiple select:** `[{name: 'A'}]` (array of objects, not strings)
- **Linked records:** `[{id: 'recXXX'}]` (objects, not plain IDs)
- **Checkbox:** `true` or `null` (never `false` — null = unchecked)
- **`selectRecordsAsync` loads ALL records** — always specify `fields` to reduce memory

---

## 7. Automations (Native)

### Trigger Types

When record matches conditions, When record created, When record updated, When form submitted, At scheduled time, When webhook received, When button pressed.

### Actions

Create record, Update record, Find records, Send email, Send Slack, Run script, Call webhook, Repeat for each, Conditional logic.

### Key Rules

- **Never create duplicate automations** — both Airtable automation AND n8n watching same trigger = double-execution
- **Preference:** n8n for complex multi-step. Airtable automations for simple single-base logic only.
- **Webhook trigger latency:** ~30 seconds. For real-time, use n8n with API polling.
- **Run limits:** Free: 100/mo, Pro: 50k/mo, Enterprise: 500k/mo.

---

## 8. Formulas

### Key Functions

**Text:** `CONCATENATE()`, `LEN()`, `LEFT()`, `RIGHT()`, `MID()`, `TRIM()`, `LOWER()`, `UPPER()`, `FIND()` (case-sensitive), `SEARCH()` (case-insensitive), `SUBSTITUTE()`, `ENCODE_URL_COMPONENT()`

**Date:** `NOW()`, `TODAY()`, `DATETIME_FORMAT(d, 'YYYY-MM-DD')`, `DATETIME_PARSE('15/01/2024', 'DD/MM/YYYY')`, `DATETIME_DIFF(d1, d2, 'days')`, `DATEADD(d, -7, 'days')`, `IS_BEFORE()`, `IS_AFTER()`, `SET_TIMEZONE(d, 'Asia/Jerusalem')`, `WORKDAY_DIFF()`

**Format tokens (Moment.js):** `YYYY` year, `MM` month, `DD` day, `HH` 24h, `hh` 12h, `mm` min, `ss` sec, `A` AM/PM, `X` unix sec, `x` unix ms.

**Regex (RE2 — no backrefs, no lookahead):** `REGEX_MATCH()`, `REGEX_EXTRACT()`, `REGEX_REPLACE()`

**Arrays (only on Rollup/Lookup):** `ARRAYJOIN()`, `ARRAYCOMPACT()`, `ARRAYUNIQUE()`, `ARRAYFLATTEN()`, `ARRAYSLICE()`

**Logic:** `IF()`, `SWITCH()`, `AND()`, `OR()`, `NOT()`, `BLANK()`, `ERROR()`

### filterByFormula

Uses field **names** (not IDs), even with `returnFieldsByFieldId=true`.

```
{Status} = 'Active'
AND({Status} = 'Active', {Amount} > 100)
SEARCH('urgent', {Description}) > 0
{Notes} = BLANK()
IS_AFTER({Created}, '2024-01-01')
DATETIME_DIFF(NOW(), {Created}, 'days') <= 7
{Done} = TRUE()
```

---

## 9. Field Types — API JSON

### Reading

| Type | JSON |
|------|------|
| singleSelect | `"Active"` (string) |
| multipleSelects | `["A", "B"]` (string[]) |
| checkbox | `true` or null/absent (**not false**) |
| percent | `0.85` = 85% (0-1 range) |
| duration | `3600` = 1h (seconds) |
| multipleRecordLinks | `["recABC"]` (recId[]) |
| multipleAttachments | `[{"id":"att...","url":"...","filename":"..."}]` |
| multipleLookupValues | varies — array of lookup results |

### Writing (REST vs Scripting differences)

| Type | REST API | Scripting |
|------|----------|-----------|
| singleSelect | `"Active"` | `{name: "Active"}` |
| multipleSelects | `["A", "B"]` | `[{name: "A"}]` |
| checkbox | `true`/`false` | `true` or omit |
| linked records | `["recABC"]` | `[{id: "recABC"}]` |

**Read-only (422 on write):** formula, rollup, lookup, count, autoNumber, createdTime, lastModifiedTime, button, synced fields.

---

## 10. Gotchas

1. **Attachment URLs expire ~2h** — always fetch fresh before use
2. **filterByFormula uses field NAMES not IDs** — even with `returnFieldsByFieldId`
3. **Single select is case-sensitive** — `'Active'` ≠ `'active'`
4. **Checkbox unchecked = null** — not `false`
5. **Percent is 0-1** — `0.85` not `85`
6. **Duration is seconds** — `3600` not `"1h"`
7. **PATCH vs PUT** — PATCH updates specified; PUT clears unspecified
8. **Scripting batch = 50, REST batch = 10** — don't mix up
9. **Formula fields are read-only** — 422 on write
10. **Array functions only work on Rollup/Lookup** — can't construct arrays
11. **REGEX uses RE2** — no backreferences, no lookahead
12. **Webhook expiry = 7 days** — refresh daily
13. **Renaming a field silently breaks all scripts** — no error, wrong data
14. **`selectRecordsAsync` loads ALL records** — specify `fields`
15. **No `await` in `for...in`** — use `for...of`
16. **Buddhist Era dates** — Thai docs use B.E. (2568 = 2025). Store as-written in `Local Date`
17. **Internal API cookies expire** — capture fresh from DevTools each session
18. **Internal API responses use msgpack** — not plain JSON
19. **`_csrf` token required** for some internal write endpoints
20. **n8n Airtable node** — handles batching automatically, no URL encoding needed for formulas

### Rate Limits

| Limit | Value |
|-------|-------|
| REST API | 5 req/sec per base |
| PAT total | 50 req/sec across all bases |
| Record list page | 100 records max |
| REST batch | 10 records/request |
| Scripting batch | 50 records/call |
| Script timeout | 30 seconds |

---

## 11. Utilities

### Automation Export Script

`extract_automations.py` — exports all automations from a base via internal v0.3 API.

```bash
python3 extract_automations.py <base_id> <output_dir> <cookie>
```
