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
PAGE_ID="pagAAAAAAAAAAAAAAAA"
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
        \"source\": {\"type\": \"table\", \"tableId\": \"tblBBBBBBBBBBBBBBB\"},
        \"columnIds\": [\"fldPRESENTATION\", \"fldFOLLOWUP\"],
        \"sorts\": [{\"columnId\": \"fldFOLLOWUP\", \"ascending\": true}],
        \"filters\": {
          \"conjunction\": \"and\",
          \"filterSet\": [{
            \"columnId\": \"fldPRESENTATION\",
            \"operator\": \"isAnyOf\",
            \"value\": [\"selOPTION4\", \"selOPTION5\"]
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
curl "https://api.airtable.com/v0/$BASE_ID/Meetings?\
fields[]=Subject&fields[]=Status&fields[]=Start%20Date&\
filterByFormula=AND(%7BStatus%7D%3D'Scheduled'%2CIS_AFTER(%7BStart%20Date%7D%2CTODAY()))&\
sort[0][field]=Start%20Date&sort[0][direction]=asc&\
pageSize=100" \
  -H "Authorization: Bearer $PAT"
```

### Create with all field types

```bash
curl -X POST "https://api.airtable.com/v0/$BASE_ID/Meetings" \
  -H "Authorization: Bearer $PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [{
      "fields": {
        "External Title": "Q1 Review",
        "Status": "Prepare",
        "Start Date": "2026-04-01T10:00:00.000Z",
        "End Date": "2026-04-01T11:00:00.000Z",
        "Company": ["recXXX"],
        "Team": ["recYYY"],
        "Channel": "Zoom",
        "Priority": 4,
        "Objectives": "Review Q1 progress",
        "Price": 500,
        "Doing Happy": 2,
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
    .map(r => parseInt(r.getCellValueAsString('ID').replace('D1DX-', '')) || 0));
output.set('newId', `D1DX-${String(maxId + 1).padStart(5, '0')}`);
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
