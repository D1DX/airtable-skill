# Airtable — Extended Reference

Appendix for the unified Airtable skill. Full payload examples, element schemas, curl templates.

---

## Internal API — Curl Templates

### Setup

```bash
# Capture from DevTools → Network → any v0.3 request → Copy Cookie header
COOKIE="__Host-airtable-session=...; ..."
BASE_ID="appXXXXXXXXXXXXXX"
```

### Common headers (all internal endpoints)

```bash
HEADERS=(
  -H "x-airtable-application-id: $BASE_ID"
  -H "x-airtable-inter-service-client: webClient"
  -H "x-airtable-page-load-id: pgloXXXXXXXXXXXXX"
  -H "x-requested-with: XMLHttpRequest"
  -H "x-time-zone: UTC"
  -H "x-user-locale: en"
  -H "cookie: $COOKIE"
)
```

### Read base schema (includes automation IDs)

```bash
curl -s "https://airtable.com/v0.3/application/$BASE_ID/read?includeAllData=true" \
  "${HEADERS[@]}" | jq '.data.workflowSectionsById'
```

### Read interface page layout

```bash
PAGE_ID="pagXXXXXXXXXXXXXXX"
curl -s "https://airtable.com/v0.3/page/$PAGE_ID/readDraft?stringifiedObjectParams=%7B%22expectedPageLayoutSchemaVersion%22%3A26%7D" \
  "${HEADERS[@]}" | jq '.data.value.elementById | keys | length'
```

### Read automation

```bash
WORKFLOW_ID="wflXXXXXXXXXXXXX"
curl -s "https://airtable.com/v0.3/workflow/$WORKFLOW_ID/read" \
  "${HEADERS[@]}" | jq '.data.workflow.name'
```

### Read automation deployment (full definition)

```bash
DEPLOYMENT_ID="wdpXXXXXXXXXXXXX"
curl -s "https://airtable.com/v0.3/workflowDeployment/$DEPLOYMENT_ID/read?stringifiedObjectParams=%7B%7D" \
  "${HEADERS[@]}" | jq '.data'
```

### readQueries (data fetch)

```bash
curl -s -X POST "https://airtable.com/v0.3/application/$BASE_ID/readQueries" \
  "${HEADERS[@]}" \
  -H "content-type: application/x-www-form-urlencoded; charset=UTF-8" \
  --data-urlencode "stringifiedObjectParams={
    \"queries\": [{
      \"id\": \"qryCustom1\",
      \"spec\": {
        \"source\": {\"type\": \"table\", \"tableId\": \"tblXXXXXXXXXXXXXXX\"},
        \"columnIds\": [\"fldSTATUS\", \"fldDATE\"],
        \"sorts\": [{\"columnId\": \"fldDATE\", \"ascending\": true}],
        \"filters\": {
          \"conjunction\": \"and\",
          \"filterSet\": [{
            \"columnId\": \"fldSTATUS\",
            \"operator\": \"isAnyOf\",
            \"value\": [\"selOPTION1\", \"selOPTION2\"]
          }]
        }
      }
    }],
    \"subscribeToRealtimeUpdates\": false,
    \"allowMsgpackOfResult\": false
  }"
```

**Tip:** Set `allowMsgpackOfResult: false` to get JSON instead of msgpack for debugging.

---

## Internal API — Full Element Type Schemas

### cellEditor (most common)

```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "cellEditor",
  "source": {
    "type": "column",
    "columnId": "fld..."
  },
  "isReadOnly": false,
  "label": {"isEnabled": true, "value": "Custom Label"},
  "shouldShowDescription": true,
  "description": [{"type": "paragraph", "children": [{"text": "Help text"}]}],
  "visibilityFilters": {"conjunction": "and", "filterSet": [...]},
  "visualVariant": {"type": "grid", "size": "medium"},
  "foreignRowSelectionConstraint": {
    "filters": {"conjunction": "and", "filterSet": [{"columnId": "fld...", "operator": "|", "value": null}]}
  },
  "foreignRowEmbeddedFormButton": {
    "isEnabled": true,
    "buttonLabel": "Add new",
    "formFieldVisibility": "allNonComputed",
    "formFields": {}
  }
}
```

### section

```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "section",
  "visualVariant": "grid",
  "title": "Section Title",
  "shouldDisplayTitle": true,
  "shouldDisplayDescription": false,
  "labelLayoutVariant": "stacked",
  "style": null,
  "visibilityFilters": {"conjunction": "and", "filterSet": [...]}
}
```

### queryContainer

```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "queryContainer",
  "source": {
    "type": "foreignKey",
    "tableId": "tbl...",
    "foreignColumnId": "fld...",
    "foreignRow": {"type": "row", "tableId": "tbl...", "outputId": "peo..."}
  },
  "staticFilters": null,
  "presetFilters": null,
  "savedFilterSets": null,
  "activeFilterType": "custom",
  "allRowsLabel": null,
  "endUserControls": {
    "isFilterEnabled": false,
    "isSortEnabled": false,
    "isSearchEnabled": false,
    "isGroupLevelsEnabled": false,
    "isHideEmptyParentsEnabled": false
  },
  "outputs": {"query": {"type": "query", "id": "peo..."}},
  "viewCanvasAreas": [{"canvasAreaId": "pla..."}],
  "isPdfExportEnabled": true,
  "label": {"isEnabled": true, "value": "Actions"}
}
```

### levels (hierarchical list)

```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "levels",
  "leafTableId": "tbl...",
  "sourceLevel": 1,
  "rowHeight": "medium",
  "isReadOnly": true,
  "editability": {},
  "label": {"isEnabled": true, "value": "Actions"},
  "queryByLevel": {},
  "levelsConfig": {},
  "expandedRowByTableId": {}
}
```

### button

```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "button",
  "action": {"type": "openUrl", "url": {"type": "column", "columnId": "fld..."}},
  "colorTheme": "red",
  "buttonText": null,
  "visibilityFilters": {"conjunction": "and", "filterSet": [...]}
}
```

### attachmentCarousel

```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "attachmentCarousel",
  "source": {"type": "column", "columnId": "fld..."},
  "isReadOnly": false,
  "previewImageCoverFitType": "fit",
  "numAttachmentsPerCarouselPage": 1,
  "visibilityFilters": {"conjunction": "or", "filterSet": [...]}
}
```

### slotElement (layout tree)

```json
{
  "id": "pls...",
  "nodeType": "slotElement",
  "parentId": "pel...",
  "slotType": "sectionGridRows",
  "elementId": "pel...",
  "index": "a0"
}
```

`slotType`: `sectionGridRows` (rows in section) or `sectionGridRowChildren` (elements in row).
`index`: alphabetical sort key (a0, a3, a4).

### Layout Tree Traversal

```
rootCanvasAreaId
  → canvasAreaById[id].canvasId
    → fullCanvasElementById[canvasId].elementId
      → elementById[elementId] (root: recordContainer or levels)
        → slotElementsById filtered by parentId → child elements
          → recurse
```

---

## REST API — Extended Examples

### List with complex filter

```bash
curl "https://api.airtable.com/v0/$BASE_ID/Orders?\
fields[]=Subject&fields[]=Status&fields[]=Start%20Date&\
filterByFormula=AND(%7BStatus%7D%3D'Scheduled'%2CIS_AFTER(%7BStart%20Date%7D%2CTODAY()))&\
sort[0][field]=Start%20Date&sort[0][direction]=asc&\
pageSize=100" \
  -H "Authorization: Bearer $PAT"
```

### Create with all field types

```bash
curl -X POST "https://api.airtable.com/v0/$BASE_ID/Orders" \
  -H "Authorization: Bearer $PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [{
      "fields": {
        "Title": "Sample Order",
        "Status": "Open",
        "Start Date": "2026-04-01T10:00:00.000Z",
        "End Date": "2026-04-01T11:00:00.000Z",
        "Customer": ["recXXX"],
        "Owner": ["recYYY"],
        "Channel": "Web",
        "Priority": 4,
        "Notes": "Sample notes",
        "Price": 500,
        "Rating": 2,
        "External": true
      }
    }],
    "typecast": true
  }'
```

### Upsert with merge

```bash
curl -X PATCH "https://api.airtable.com/v0/$BASE_ID/Contacts" \
  -H "Authorization: Bearer $PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "performUpsert": {"fieldsToMergeOn": ["Email"]},
    "records": [{"fields": {"Email": "client@example.com", "Name": "Updated Name"}}],
    "typecast": true
  }'
```

### Webhook payload structure

```json
{
  "cursor": 43,
  "mightHaveMore": true,
  "payloads": [{
    "timestamp": "2026-03-28T10:30:00.000Z",
    "baseTransactionNumber": 42,
    "actionMetadata": {
      "source": "client",
      "sourceMetadata": {"user": {"id": "usrXXX", "email": "x@y.com"}}
    },
    "changedTablesById": {
      "tblXXX": {
        "changedRecordsById": {
          "recABC": {
            "current": {"cellValuesByFieldId": {"fldXXX": "new"}},
            "previous": {"cellValuesByFieldId": {"fldXXX": "old"}}
          }
        },
        "createdRecordsById": {},
        "destroyedRecordIds": []
      }
    }
  }]
}
```

Sources: `client`, `publicApi`, `formSubmission`, `automation`, `system`, `sync`, `anonymousUser`.

---

## Scripting — Advanced Patterns

### Fetch external API

```javascript
let response = await fetch('https://api.example.com/data', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer TOKEN'},
    body: JSON.stringify({key: 'value'})
});
let data = await response.json();
```

### Generate unique ID

```javascript
const table = base.getTable('Records');
const query = await table.selectRecordsAsync({fields: ['ID']});
const maxId = Math.max(0, ...query.records
    .map(r => parseInt(r.getCellValueAsString('ID').replace('ACME-', '')) || 0));
output.set('newId', `ACME-${String(maxId + 1).padStart(5, '0')}`);
```

### Deduplicate records

```javascript
const table = base.getTable('Contacts');
const query = await table.selectRecordsAsync({fields: ['Email', 'Name']});
const seen = new Map();
const duplicates = [];
for (const record of query.records) {
    const email = record.getCellValueAsString('Email').toLowerCase();
    if (seen.has(email)) duplicates.push({id: record.id, email});
    else seen.set(email, record.id);
}
output.text(`Found ${duplicates.length} duplicates`);
output.table(duplicates);
```

### Cross-table sync

```javascript
const source = base.getTable('Source');
const target = base.getTable('Target');
const srcQ = await source.selectRecordsAsync({fields: ['Key', 'Value']});
const tgtQ = await target.selectRecordsAsync({fields: ['Key', 'Value']});
const tgtMap = new Map(tgtQ.records.map(r => [r.getCellValueAsString('Key'), r]));

const updates = [], creates = [];
for (const sr of srcQ.records) {
    const key = sr.getCellValueAsString('Key');
    const value = sr.getCellValueAsString('Value');
    const existing = tgtMap.get(key);
    if (existing) {
        if (existing.getCellValueAsString('Value') !== value)
            updates.push({id: existing.id, fields: {'Value': value}});
    } else {
        creates.push({fields: {'Key': key, 'Value': value}});
    }
}
while (updates.length) await target.updateRecordsAsync(updates.splice(0, 50));
while (creates.length) await target.createRecordsAsync(creates.splice(0, 50));
```

### Rate limit retry (REST API)

```javascript
async function airtableRequest(url, options, maxRetries = 3) {
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
        const response = await fetch(url, options);
        if (response.status === 429) {
            await new Promise(r => setTimeout(r, Math.max(30000, 2 ** attempt * 1000)));
            continue;
        }
        if (!response.ok) throw new Error(`HTTP ${response.status}: ${await response.text()}`);
        return response.json();
    }
    throw new Error('Max retries exceeded');
}
```

---

## Complete DATETIME_FORMAT Tokens

| Token | Output | Example |
|-------|--------|---------|
| `YYYY` | 4-digit year | 2026 |
| `YY` | 2-digit year | 26 |
| `Q` | Quarter | 1-4 |
| `M` / `MM` | Month | 3 / 03 |
| `MMM` / `MMMM` | Month name | Mar / March |
| `D` / `DD` | Day | 5 / 05 |
| `Do` | Day ordinal | 5th |
| `d` / `dd` / `ddd` / `dddd` | Weekday | 5 / Fr / Fri / Friday |
| `H` / `HH` | Hour 24h | 9 / 09 |
| `h` / `hh` | Hour 12h | 9 / 09 |
| `m` / `mm` | Minute | 5 / 05 |
| `s` / `ss` | Second | 5 / 05 |
| `SSS` | Milliseconds | 123 |
| `A` / `a` | AM/PM | AM / am |
| `X` | Unix seconds | 1774692000 |
| `x` | Unix ms | 1774692000000 |
| `W` | ISO week | 13 |

---

## Internal API — Calculated Field Creation

The public Meta API refuses to create calculated fields (`UNSUPPORTED_FIELD_TYPE_FOR_CREATE: "Creating rollup fields is not supported at this time"` — same for `formula`, `lookup`, `count`, `aiText`). The **internal** `/v0.3/column/{fieldId}/create` endpoint fully supports them — this is the endpoint the Airtable web UI itself uses.

### When to use this vs. Omni AI

Two supported paths exist for creating calculated fields. Pick per task:

| Situation | Path |
|-----------|------|
| One-off field, human at the keyboard | **Omni AI** — natural language, in-browser, zero setup |
| Bulk / repeated / scripted / CI-driven | **Internal Web API** (this section) |
| Need reproducibility across environments | **Internal Web API** |
| Don't want to maintain an undocumented-endpoint integration | **Omni AI** |

**Risk of this path:** the `/v0.3/column/` endpoints are not part of Airtable's public contract. Airtable can change the payload shape, add CSRF validation, or block non-browser clients without notice. If the browser UI still works but your script 4xx's, assume the payload shape drifted — re-capture a HAR and diff.

Reverse-engineered from a browser HAR capture (April 2026). No `_csrf` token is required for these endpoints — only session cookies.

### Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| POST | `/v0.3/column/{newFieldId}/create` | Create a new field (text, formula, rollup, lookup, count, select, foreignKey, button, …). **The `{newFieldId}` is generated client-side** — the server uses the ID you put in the URL as the new field's ID. |
| POST | `/v0.3/column/{fieldId}/updateConfig` | Update an existing field's type/typeOptions (e.g. add filters to a rollup, change formula text). Returns `{"data": {"actionId": "act..."}}`. |
| POST | `/v0.3/table/{tableId}/getUnsavedColumnConfigResultType` | Validate a formula before saving. Returns `{"pass": true, "resultType": "text"}`. Optional but recommended for formulas — catches syntax errors before `create`. |

**Client-generated field IDs.** The Airtable web client generates a random `fld...` ID (17 chars, starts with `fld`, then 14 chars of `A-Za-z0-9`) and puts it in the URL. The server trusts it. If you send two creates with the same ID, the second will conflict. Use a short random generator — e.g. Python `"fld" + "".join(random.choices(string.ascii_letters + string.digits, k=14))`.

### Auth

Cookie-based session. Same cookies as the existing "Internal Web API" section of `SKILL.md` — capture from DevTools → Network → any `/v0.3/` request → copy the full `Cookie` header. The important cookie is `__Host-airtable-session`; Airtable also sets `brwIds`, `__Host-airtable-session.sig`, and several analytics cookies, so copy the whole header as one blob.

**Never hardcode.** Store the full cookie string in 1Password under the appropriate client/base vault — `op://{vault}/airtable-web-session/cookie` — and retrieve with `op read` at runtime. One secret, one consumer: each base gets its own item; do not share cookies across clients.

```bash
export AIRTABLE_COOKIE="$(op read 'op://{vault}/airtable-web-session/cookie')"
```

Session lifetime is whatever the browser session is — typically weeks, but any logout or password change invalidates it. If a request returns `401` or redirects to `/login`, re-capture.

### Required headers (all calculated-field endpoints)

```
x-airtable-application-id: {baseId}
x-airtable-inter-service-client: webClient
x-airtable-page-load-id: pglo{14 chars}      # any stable random value per session is fine
x-requested-with: XMLHttpRequest
x-time-zone: {IANA tz, e.g. UTC}
x-user-locale: en
origin: https://airtable.com
referer: https://airtable.com/{baseId}/{tableId}/{viewId}
content-type: application/x-www-form-urlencoded; charset=UTF-8
cookie: {full cookie blob}
```

`origin` and `referer` are checked loosely — missing them gets 403. `x-airtable-page-load-id` is checked for presence/format, not against any registry.

### Body format — form-encoded with a JSON blob

Every `create` / `updateConfig` body is `application/x-www-form-urlencoded` with **one** field of interest:

```
stringifiedObjectParams={url-encoded JSON}&requestId=req{14 chars}&secretSocketId=soc{14 chars}
```

- `requestId` — any `req` + 14 random chars; appears in idempotency / log correlation but the server does not require strict uniqueness
- `secretSocketId` — any `soc` + 14 random chars; only used for realtime push fan-out, safe to invent

### Create — text / select / etc. (baseline shape)

```json
{
  "tableId": "tbl...",
  "name": "Label",
  "config": { "default": null, "type": "text", "typeOptions": null },
  "description": null,
  "activeViewId": "viw...",
  "afterOverallColumnIndex": 4,
  "origin": "gridAddFieldButton"
}
```

`afterOverallColumnIndex` controls column position (0-indexed, places new column after that index). `activeViewId` can be any view on the target table; `origin` is telemetry — any string works but `"gridAddFieldButton"` is safest.

### Create — formula

```json
{
  "tableId": "tbl...",
  "name": "Calculation",
  "config": {
    "default": null,
    "type": "formula",
    "typeOptions": {
      "formulaText": "DATETIME_DIFF(TODAY(), {Created}, 'days')"
    }
  },
  "description": null,
  "activeViewId": "viw...",
  "afterOverallColumnIndex": 7,
  "origin": "gridAddFieldButton"
}
```

**Formula text uses field NAMES** (wrapped in `{}` if they contain spaces), not field IDs. Same syntax as the UI formula editor. Validate first via `getUnsavedColumnConfigResultType`:

```json
// POST /v0.3/table/{tableId}/getUnsavedColumnConfigResultType
{
  "config": {
    "default": null,
    "type": "formula",
    "typeOptions": { "formulaText": "TODAY()&Status" }
  }
}
// → {"msg":"SUCCESS","data":{"pass":true,"resultType":"text"}}
```

`resultType` returned: `text`, `number`, `date`, `boolean`, or the parent field type if the formula resolves to a select. If `pass: false`, the create will return 422.

**Formula output type coercion (select).** To make a formula output a single-select with colored chips, add to `typeOptions`:

```json
{
  "formulaText": "...",
  "formulaSelectFallbackChoice": "selFORMULADEFAULT",
  "choices": {
    "selFORMULADEFAULT": { "id": "selFORMULADEFAULT", "name": "Default", "color": "gray" },
    "sel{14chars}":       { "id": "sel{14chars}",       "name": "OptionA", "color": "blue" }
  },
  "choiceOrder": ["selFORMULADEFAULT", "sel{14chars}"],
  "disableColors": false,
  "formulaOutputColumnType": "select"
}
```

### Create — rollup

Minimum required fields: `relationColumnId`, `foreignTableRollupColumnId`, `formulaText`.

```json
{
  "tableId": "tbl...",
  "name": "Total Paid",
  "config": {
    "default": null,
    "type": "rollup",
    "typeOptions": {
      "relationColumnId": "fld{LINK FIELD on this table}",
      "foreignTableRollupColumnId": "fld{FIELD on linked table to aggregate}",
      "formulaText": "SUM(values)"
    }
  },
  "description": null,
  "activeViewId": "viw...",
  "afterOverallColumnIndex": 10,
  "origin": "gridAddFieldButton"
}
```

**Aggregation formulas** — `formulaText` is a formula expression over the implicit array variable `values`:
- `SUM(values)`, `AVERAGE(values)`, `MIN(values)`, `MAX(values)`, `COUNT(values)`, `COUNTA(values)`, `COUNTALL(values)`
- `ARRAYUNIQUE(values)`, `ARRAYCOMPACT(values)`, `ARRAYJOIN(values, ', ')`
- `AND(values)`, `OR(values)`
- Any regular formula — e.g. `IF(SUM(values) > 100, "hi", "lo")`

**Filter on rollup source rows** — `filters` is optional in both `create` and `updateConfig`. Observed working in the HAR via `updateConfig` after create (the UI flow always created first with empty filter, then updated with filters), but the structure is identical to `create` bodies for other field types, so it should work in `create` too. Safe path: create without filters, then `updateConfig` with filters.

```json
"typeOptions": {
  "relationColumnId": "fld...",
  "foreignTableRollupColumnId": "fld...",
  "formulaText": "SUM(values)",
  "filters": {
    "conjunction": "and",
    "filterSet": [
      {
        "id": "flt{14chars}",
        "columnId": "fld{column on the LINKED table to filter by}",
        "operator": "=",
        "value": false
      }
    ]
  },
  "sorts": [
    { "id": "srt{14chars}", "columnId": "fld...", "ascending": true }
  ]
}
```

**Checkbox filter operators** — observed in HAR: `contains` for text. For checkbox fields, the standard Airtable filter operators are `=` with `value: true`/`value: false`, and `isEmpty` / `isNotEmpty`. Checkbox `unchecked` stores as `null` in cell data but filter comparison with `=false` works in the UI. If `=false` fails, fall back to `isEmpty` (for unchecked) or `isNotEmpty` (for checked).

**Each filter needs a client-generated `id`** — `flt` + 14 random chars. Same for sorts: `srt` + 14 chars.

### Create — count

Count is just a filter-aware counter over linked records. Minimum: `relationColumnId`.

```json
{
  "tableId": "tbl...",
  "name": "Active Registrations",
  "config": {
    "default": null,
    "type": "count",
    "typeOptions": {
      "relationColumnId": "fld{LINK FIELD}",
      "filters": {
        "conjunction": "and",
        "filterSet": [
          { "id": "flt{14chars}", "columnId": "fld{col on linked table}", "operator": "=", "value": false }
        ]
      }
    }
  },
  "description": null,
  "activeViewId": "viw...",
  "afterOverallColumnIndex": 11,
  "origin": "gridAddFieldButton"
}
```

### Create — lookup

```json
{
  "tableId": "tbl...",
  "name": "Linked Names",
  "config": {
    "default": null,
    "type": "lookup",
    "typeOptions": {
      "relationColumnId": "fld{LINK FIELD}",
      "foreignTableRollupColumnId": "fld{FIELD on linked table to read}",
      "rowLimit": { "limit": 1, "firstOrLast": "last" },
      "filters": {
        "conjunction": "and",
        "filterSet": [
          { "id": "flt{14chars}", "columnId": "fld...", "operator": "contains", "value": "das" }
        ]
      },
      "sorts": [
        { "id": "srt{14chars}", "columnId": "fld...", "ascending": true }
      ]
    }
  },
  "description": null,
  "activeViewId": "viw...",
  "afterOverallColumnIndex": 11,
  "origin": "gridAddFieldButton"
}
```

`rowLimit` is optional (omit for all rows). `firstOrLast: "last"` takes the latest by sort order.

### Create — AI text (aiText)

Not captured in the HAR used for this reverse-engineering. The shape matches other calculated fields — `type: "aiText"`, `typeOptions` with a prompt template. Capture fresh from a session where you create an AI field, then update this section.

### Response shape

On success:
```json
{ "msg": "SUCCESS", "data": null }
```
(The field is now live. Re-read the table schema via MCP `describe_table` or Meta API to get the full created config.)

On failure — returns 422 with:
```json
{ "error": { "type": "VALIDATION_FAILED", "message": "Sorry, there was a problem creating this field. The options are not valid." } }
```
Observed cause: rollup created with empty `relationColumnId`, or formula that fails parse.

Warnings (e.g. schema dependency impact) return 422 with `type: "COLUMN_CONFIG_UPDATE_WARNING"` and a base64-JSON body containing `hasDependencyCheckWarning: true`. To bypass, re-send with `schemaDependenciesCheckParams.columnUpdateSkipWarningPrefs.skipColumnConfigExternalSyncWarning: true` and `skipColumnConfigChangeWarning: true`.

### Python recipe

```python
import os, json, secrets, string, urllib.parse, requests

def _rid(prefix, n=14):
    alphabet = string.ascii_letters + string.digits
    return prefix + "".join(secrets.choice(alphabet) for _ in range(n))

BASE_ID  = os.environ["AIRTABLE_BASE_ID"]
TABLE_ID = os.environ["AIRTABLE_TABLE_ID"]
VIEW_ID  = os.environ["AIRTABLE_VIEW_ID"]     # any view on that table
COOKIE   = os.environ["AIRTABLE_COOKIE"]       # full Cookie header from op read

HEADERS = {
    "x-airtable-application-id": BASE_ID,
    "x-airtable-inter-service-client": "webClient",
    "x-airtable-page-load-id": _rid("pglo"),
    "x-requested-with": "XMLHttpRequest",
    "x-time-zone": "UTC",
    "x-user-locale": "en",
    "origin": "https://airtable.com",
    "referer": f"https://airtable.com/{BASE_ID}/{TABLE_ID}/{VIEW_ID}",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": COOKIE,
}

def create_column(config, name, after_index=0, description=None):
    new_field_id = _rid("fld")
    params = {
        "tableId": TABLE_ID,
        "name": name,
        "config": config,
        "description": description,
        "activeViewId": VIEW_ID,
        "afterOverallColumnIndex": after_index,
        "origin": "gridAddFieldButton",
    }
    body = urllib.parse.urlencode({
        "stringifiedObjectParams": json.dumps(params),
        "requestId": _rid("req"),
        "secretSocketId": _rid("soc"),
    })
    r = requests.post(
        f"https://airtable.com/v0.3/column/{new_field_id}/create",
        headers=HEADERS, data=body, timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if data.get("msg") != "SUCCESS":
        raise RuntimeError(f"create failed: {data}")
    return new_field_id

def update_column_config(field_id, typeOptions_config):
    """typeOptions_config is the FULL config object (default, type, typeOptions)."""
    params = {
        **typeOptions_config,
        "activeViewId": VIEW_ID,
        "schemaDependenciesCheckParams": {
            "columnUpdateSkipWarningPrefs": {
                "skipColumnConfigExternalSyncWarning": False,
                "skipColumnConfigChangeWarning": False,
            }
        },
    }
    body = urllib.parse.urlencode({
        "stringifiedObjectParams": json.dumps(params),
        "requestId": _rid("req"),
        "secretSocketId": _rid("soc"),
    })
    r = requests.post(
        f"https://airtable.com/v0.3/column/{field_id}/updateConfig",
        headers=HEADERS, data=body, timeout=30,
    )
    r.raise_for_status()
    return r.json()
```

Usage — a rollup `SUM(values)` of `Payments.amount`:

```python
fid = create_column(
    config={
        "default": None,
        "type": "rollup",
        "typeOptions": {
            "relationColumnId": "fldLINK",
            "foreignTableRollupColumnId": "fldAMOUNT",
            "formulaText": "SUM(values)",
        },
    },
    name="Total Paid",
    after_index=20,
)
print("created", fid)
```

### Gotchas

1. **Public Meta API still refuses these field types.** Always use the internal endpoint for create; use the public API for reads/updates of records after creation.
2. **Field ID collisions.** Client generates the `fld...` ID — roll a cryptographically random 14-char suffix. Don't reuse IDs.
3. **`relationColumnId` must be a link field on the SAME table** as the rollup/count/lookup. `foreignTableRollupColumnId` must be a field on the **linked** table (the target of the link).
4. **Rollup `formulaText` syntax differs from regular formulas** — uses `values` as the implicit array. `SUM({Amount})` will NOT work; use `SUM(values)` where `foreignTableRollupColumnId` already points at `Amount`.
5. **Filter `id` required.** Every filter entry and sort entry must have a unique `flt...` / `srt...` id — the server rejects filters without one.
6. **Warning bypass.** If `updateConfig` returns 422 with `COLUMN_CONFIG_UPDATE_WARNING`, re-send with both `skipColumnConfigExternalSyncWarning: true` and `skipColumnConfigChangeWarning: true`.
7. **Referer must be a valid base/table/view URL** on airtable.com. A blank referer returns 403.
8. **Cookies expire silently.** A 302 redirect to `/login` HTML instead of JSON means re-capture the cookie.
9. **No rate limit documented, but UI throttles to ~1 field-create per 500 ms.** Don't loop faster than 2 QPS or you'll hit the generic 429.
10. **Filters with `msg:"SUCCESS", data:null`** — success returns `data: null` on create. Don't confuse with failure.
11. **`updateConfig` returns an `actionId`** — you can poll it via the base realtime socket, or just re-read schema after ~500 ms.
12. **Formula preview endpoint (`getUnsavedColumnConfigResultType`) only validates formulas** — it ignores `relationColumnId` validity for rollups. Do your own existence check before POSTing.

---

## Internal API — Personal Access Token Management

The public REST API does not expose any PAT-management endpoints — listing, creating, regenerating, renaming, and revoking PATs are all UI-only as far as Airtable's public docs go. The Builder Hub uses internal `/v0.3/user/{userId}/...` endpoints for all five operations. Reverse-engineered from a HAR capture (May 2026, Builder Hub session).

**When to use this:**
- Programmatic rotation of PATs across many automations / consumers
- Audits ("which PATs exist, what scopes, accessible to which bases")
- CI-driven PAT lifecycle (mint → use → revoke at end of job)

**When NOT to use this:**
- One-off mint/revoke — Builder Hub UI is faster
- Anywhere the cookie-session liveness is fragile (CI on a shared runner)

### Auth

Same cookie-based auth as the rest of the internal API. The PAT-management endpoints DO require `_csrf` (unlike `/v0.3/column/...`). Capture both the cookie blob AND the CSRF token from any logged-in `/v0.3/...` request — the CSRF token is in the `x-csrf-token` request header and rotates per session.

```bash
# In secret-capture or a 1P item, store both:
op://{vault}/airtable-web-session/cookie       # full Cookie header
op://{vault}/airtable-web-session/csrf-token   # x-csrf-token header value
```

### Endpoints

All bodies use the `stringifiedObjectParams` envelope — the params are JSON-encoded as a string field inside the outer JSON. Don't send the params as a nested object; the server expects a string.

| Method | URL | Purpose |
|--------|-----|---------|
| GET    | `/v0.3/user/{userId}/getPersonalAccessTokensForDevelopersHub` | List the calling user's PATs (id, name, scopes, accessible workspaces/applications, last-used). Does NOT return the token value — values are write-only at mint time. |
| POST   | `/v0.3/user/{userId}/createPersonalAccessToken` | Mint a new PAT. Response includes the plaintext token value once — capture and route to consumer immediately. |
| POST   | `/v0.3/user/{userId}/regeneratePersonalAccessToken` | In-place value swap — same `tokenId`, new value. Old value invalidated server-side at the moment the new value is returned. **No revoke step needed**; this IS rotation. |
| POST   | `/v0.3/user/{userId}/updatePersonalAccessTokenName` | Rename a PAT. |
| POST   | `/v0.3/user/{userId}/destroyMultiplePersonalAccessTokens` | Revoke one or more PATs by id. |

### Request body shapes (scrubbed)

```json
// POST createPersonalAccessToken
{
  "stringifiedObjectParams": "{\"name\":\"my-rotation-pat\",\"explicitTokenResources\":{\"type\":\"specificModelIds\",\"workspaceIds\":[],\"applicationIds\":[\"appXXXXXXXXXXXXXX\"]},\"scopes\":[\"data.records:read\",\"data.records:write\",\"webhook:manage\"]}",
  "requestId": "req<random16>",
  "_csrf": "<csrf-token>"
}

// POST regeneratePersonalAccessToken
{
  "stringifiedObjectParams": "{\"tokenId\":\"patXXXXXXXXXXXXXX\"}",
  "requestId": "req<random16>",
  "_csrf": "<csrf-token>"
}

// POST updatePersonalAccessTokenName
{
  "stringifiedObjectParams": "{\"tokenId\":\"patXXXXXXXXXXXXXX\",\"name\":\"new-name\"}",
  "requestId": "req<random16>",
  "_csrf": "<csrf-token>"
}

// POST destroyMultiplePersonalAccessTokens
{
  "stringifiedObjectParams": "{\"tokenIds\":[\"patXXXXXXXXXXXXXX\",\"patYYYYYYYYYYYYYY\"]}",
  "requestId": "req<random16>",
  "_csrf": "<csrf-token>"
}
```

### Response envelope

```json
{ "msg": "SUCCESS", "data": { ... } }
```

- `createPersonalAccessToken` and `regeneratePersonalAccessToken` return the plaintext PAT value in `data.personalAccessToken` — single chance to capture it.
- `getPersonalAccessTokensForDevelopersHub` returns `data.tokens` (array of token metadata; values masked).
- `destroyMultiplePersonalAccessTokens` returns `data: null` on success.
- `updatePersonalAccessTokenName` returns `data.name`.

### Scope vocabulary

The `scopes` array in `createPersonalAccessToken` accepts the same scope strings exposed in Builder Hub UI. Common ones:

- `data.records:read`
- `data.records:write`
- `data.recordComments:read`
- `data.recordComments:write`
- `schema.bases:read`
- `schema.bases:write`
- `webhook:manage`
- `block:manage`
- `enterprise.account:read` (enterprise plans only)

### Resource targeting

`explicitTokenResources` controls which workspaces / bases the PAT can access:

| `type` | Behavior |
|--------|----------|
| `allCurrentAndFuture` | Every workspace + base the user has access to, including future ones. |
| `specificModelIds` | Limited to the listed `workspaceIds[]` and/or `applicationIds[]`. Empty arrays means none — be careful, you can mint a PAT with no resources by accident. |

### Operational gotchas

1. **The token value appears once.** Both `create` and `regenerate` return the plaintext value in the response and never again. Capture into the consumer immediately — `secret-capture` skill is the safe path so the value never enters the agent transcript.
2. **`regenerate` is the safest rotation primitive.** Same token id, scopes, and resource list — only the value changes. Consumers that store the value (only) need updating; consumers that store the token id can keep going. Use this over `create` + `destroy` whenever the goal is a value-only swap.
3. **Old value dies the moment the new one is returned.** There is no overlap window. Stage the consumer update so the old value's last successful call happens BEFORE you call regenerate, and the next call uses the new value.
4. **`destroyMultiple` is bulk + idempotent.** Sending an already-revoked id returns success. Useful for a "revoke all PATs matching a name prefix" sweep.
5. **CSRF token rotates per session.** Cache it for the duration of a script's run; re-capture on `403 Invalid CSRF`.
6. **Listing returns metadata only — never the value.** A "show me what PATs exist" audit is safe; a "what is the value of this PAT" lookup is impossible (correctly).
7. **PAT id is `pat` + 14 chars `[A-Za-z0-9]`** — same prefix as the value but a different identifier. The id is stable across regenerations; the value changes.
8. **The user's own user id (`usrXXX...`)** is in the URL path. Find it in the response of any `/v0.3/user/{userId}/...` call you've already captured, or via `getMe`-style endpoints that some Builder Hub screens hit.

### Python helper

```python
import json, secrets, string, urllib.request

def _airtable_internal_post(path: str, params: dict, *, cookie: str, csrf: str, base_id: str | None = None) -> dict:
    """POST to /v0.3/... with the stringifiedObjectParams envelope."""
    body = json.dumps({
        "stringifiedObjectParams": json.dumps(params, separators=(",", ":")),
        "requestId": "req" + "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16)),
        "_csrf": csrf,
    }).encode()
    req = urllib.request.Request(
        f"https://airtable.com{path}",
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Cookie": cookie,
            "x-csrf-token": csrf,
            "x-airtable-inter-service-client": "webClient",
            "x-requested-with": "XMLHttpRequest",
            "x-airtable-application-id": base_id or "appAAAAAAAAAAAAAA",
        },
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def regenerate_pat(user_id: str, token_id: str, *, cookie: str, csrf: str) -> str:
    """Rotate a PAT in place. Returns the new plaintext token value (capture once)."""
    res = _airtable_internal_post(
        f"/v0.3/user/{user_id}/regeneratePersonalAccessToken",
        {"tokenId": token_id},
        cookie=cookie, csrf=csrf,
    )
    if res.get("msg") != "SUCCESS":
        raise RuntimeError(f"regenerate failed: {res}")
    return res["data"]["personalAccessToken"]

def list_pats(user_id: str, *, cookie: str) -> list[dict]:
    req = urllib.request.Request(
        f"https://airtable.com/v0.3/user/{user_id}/getPersonalAccessTokensForDevelopersHub",
        headers={
            "Cookie": cookie,
            "x-airtable-inter-service-client": "webClient",
            "x-requested-with": "XMLHttpRequest",
        },
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["data"]["tokens"]

def destroy_pats(user_id: str, token_ids: list[str], *, cookie: str, csrf: str) -> None:
    res = _airtable_internal_post(
        f"/v0.3/user/{user_id}/destroyMultiplePersonalAccessTokens",
        {"tokenIds": token_ids},
        cookie=cookie, csrf=csrf,
    )
    if res.get("msg") != "SUCCESS":
        raise RuntimeError(f"destroy failed: {res}")
```

### Safe rotation pattern

```python
# Goal: swap the PAT value without ever exposing it to logs/transcripts.
# The new value is captured directly into the consumer (env file, 1P, n8n).

new_value = regenerate_pat(USER_ID, TOKEN_ID, cookie=COOKIE, csrf=CSRF)
# `new_value` is in process memory only. Do NOT print it.
write_to_consumer(new_value)              # e.g. ssh + sed -i, or n8n credential update
del new_value
```

For agentic flows where the value should never enter the agent's process memory, use the `secret-capture` skill's ssh adapter — the user pastes the regenerated value into a hidden dialog, and the adapter routes it directly to the target without round-tripping through the agent.

