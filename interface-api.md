# Airtable Interface Designer — Internal API Specification

Reverse-engineered from desktop app HAR capture (March 2026).
Base URL: `https://airtable.com`

---

## Authentication & Common Headers

All requests to `/v0.3/` endpoints use cookie-based session auth (browser session).

| Header | Value | Required |
|--------|-------|----------|
| `x-airtable-application-id` | `app...` (base ID) | Yes |
| `x-airtable-inter-service-client` | `webClient` | Yes |
| `x-airtable-page-load-id` | `pglo...` (session-scoped) | Yes |
| `x-requested-with` | `XMLHttpRequest` | Yes |
| `x-time-zone` | IANA timezone (e.g. `Asia/Bangkok`) | Yes |
| `x-user-locale` | `en` | Yes |
| `x-airtable-client-queue-time` | float (ms) | Optional |
| `content-type` | `application/x-www-form-urlencoded; charset=UTF-8` (readQueries) or `application/json` (others) | Yes |
| `cookie` | Full session cookie string | Yes |

---

## 1. Page Layout — `readDraft`

Fetches the full layout schema of an interface page: all elements, their types, properties, visibility conditions, canvas structure, and slot hierarchy.

### Request

```
GET /v0.3/page/{pageId}/readDraft?stringifiedObjectParams={json}&requestId={reqId}&secretSocketId={socId}
```

**Path Parameters:**
- `pageId` — Interface page ID (prefix `pag`, 17 chars). Example: `pagAAAAAAAAAAAAAAAA`

**Query Parameters:**
- `stringifiedObjectParams` — URL-encoded JSON: `{"expectedPageLayoutSchemaVersion": 26}`
- `requestId` — Client-generated request ID (prefix `req`, 17 chars)
- `secretSocketId` — WebSocket session ID (prefix `soc`, 17 chars)

### Response

```json
{
  "msg": "SUCCESS",
  "data": {
    "id": "pagAAAAAAAAAAAAAAAA",
    "value": {
      "schemaVersion": 26,
      "rootCanvasAreaId": "pla...",
      "rootRowContainer": {
        "tableId": "tbl...",
        "output": { "type": "row", "id": "peo..." }
      },
      "elementById": { /* 20–200+ elements */ },
      "slotElementsById": { /* parent-child relationships */ },
      "canvasAreaById": { /* canvas area → canvas mapping */ },
      "fullCanvasElementById": { /* canvas → root element mapping */ },
      "rowCanvasById": {},
      "elementRowById": {},
      "columnsRowById": {},
      "columnById": {},
      "horizontalBarById": {},
      "horizontalBarRowById": {},
      "horizontalBarElementById": {}
    }
  }
}
```

### Element Types

Every element in `elementById` has `nodeType: "element"`, an `id` (prefix `pel`), and a `type`:

#### `recordContainer`
Root container for a record detail page.
```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "recordContainer",
  "areSectionsCollapsible": true,
  "areTabsEnabled": true
}
```

#### `section`
Groups elements visually. Can have visibility conditions.
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
  "visibilityFilters": { /* see Visibility Filters below */ }
}
```

#### `sectionGridRow`
Layout row within a section.
```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "sectionGridRow",
  "childWidthBehavior": "stretch",
  "contentArea": "center",
  "shouldHideLabels": false
}
```

#### `cellEditor`
Renders a single field. The most common element type.
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
  "label": { "isEnabled": true, "value": "Custom Label" },
  "shouldShowDescription": true,
  "description": [{ "type": "paragraph", "children": [{ "text": "..." }] }],
  "visibilityFilters": { /* optional */ },
  "visualVariant": { /* optional display config */ },
  "foreignRowSelectionConstraint": { /* optional — for linked record fields */ },
  "foreignRowEmbeddedFormButton": { /* optional — inline form creation */ }
}
```

#### `queryContainer`
Embeds a filtered list/grid of linked records.
```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "queryContainer",
  "source": {
    "type": "foreignKey",
    "tableId": "tbl...",
    "foreignColumnId": "fld...",
    "foreignRow": {
      "type": "row",
      "tableId": "tbl...",
      "outputId": "peo..."
    }
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
  "outputs": {
    "query": { "type": "query", "id": "peo..." }
  },
  "viewCanvasAreas": [{ "canvasAreaId": "pla..." }],
  "isPdfExportEnabled": true,
  "label": { "isEnabled": true, "value": "Actions" }
}
```

#### `levels`
Hierarchical/nested record list.
```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "levels",
  "leafTableId": "tbl...",
  "sourceLevel": 1,
  "rowHeight": "medium",
  "isReadOnly": true,
  "editability": { /* per-level edit config */ },
  "label": { "isEnabled": true, "value": "..." },
  "queryByLevel": { /* level → query mapping */ },
  "levelsConfig": { /* level definitions */ },
  "expandedRowByTableId": {}
}
```

#### `button`
Action button with visibility conditions.
```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "button",
  "action": { "type": "openUrl", "url": { /* source config */ } },
  "colorTheme": "red",
  "buttonText": null,
  "visibilityFilters": { /* when to show */ }
}
```

#### `text`
Static rich text block.
```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "text",
  "document": [{ "type": "paragraph", "children": [{ "text": "..." }] }]
}
```

#### `attachmentCarousel`
Displays attachment field as a carousel.
```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "attachmentCarousel",
  "source": { "type": "column", "columnId": "fld..." },
  "isReadOnly": false,
  "previewImageCoverFitType": "fit",
  "numAttachmentsPerCarouselPage": 1,
  "visibilityFilters": { /* optional */ }
}
```

#### `rowActivityFeed`
Comment/activity feed for a record.
```json
{
  "nodeType": "element",
  "id": "pel...",
  "type": "rowActivityFeed",
  "sourceRow": { "type": "row", "tableId": "tbl...", "outputId": "peo..." },
  "areCommentsDisabled": true,
  "isRevisionHistoryEnabled": true
}
```

### Slot Elements (`slotElementsById`)

Define parent-child relationships in the layout tree.

```json
{
  "id": "pls...",
  "nodeType": "slotElement",
  "parentId": "pel...",
  "slotType": "sectionGridRows" | "sectionGridRowChildren",
  "elementId": "pel...",
  "index": "a0"
}
```

- `parentId` — the section or row that contains this slot
- `elementId` — the element placed in this slot
- `index` — alphabetical ordering key (e.g. `a0`, `a3`, `a4`)
- `slotType` — `sectionGridRows` (rows in a section) or `sectionGridRowChildren` (elements in a row)

### Canvas Areas (`canvasAreaById`)

```json
{
  "nodeType": "canvasArea",
  "id": "pla...",
  "canvasId": "plf..."
}
```

### Full Canvas Elements (`fullCanvasElementById`)

Maps a canvas to its root element.

```json
{
  "nodeType": "fullCanvasElement",
  "id": "plf...",
  "elementId": "pel..."
}
```

### Layout Tree Traversal

```
rootCanvasAreaId → canvasAreaById[id].canvasId
  → fullCanvasElementById[canvasId].elementId
    → elementById[elementId] (root recordContainer/levels)
      → slotElementsById (filter by parentId) → child elements
        → recurse
```

---

## 2. Visibility Filters

Control when elements/sections are shown on the record detail page. Evaluated client-side against the current record's field values.

### Structure

```json
{
  "conjunction": "and" | "or",
  "filterSet": [
    {
      "columnId": "fld...",
      "operator": "<operator>",
      "value": <value>,
      "type": "columnComparison"  // optional
    }
  ]
}
```

### Operators

| Operator | Value Type | Meaning |
|----------|-----------|---------|
| `isAnyOf` | `["sel...", ...]` | Field value is one of the listed select option IDs |
| `isNoneOf` | `["sel...", ...]` | Field value is NOT any of the listed options |
| `=` | `"sel..."` or `"value"` or `null` | Exact match (single select, checkbox) |
| `\|` | `null` or `["sel...", ...]` | Linked record "is not empty" (pipe = OR/exists) |
| `isEmpty` | `null` | Field has no value |
| `isNotEmpty` | `null` | Field has a value |

### Empty filter (always visible)

```json
{ "conjunction": "and", "filterSet": [] }
```

### Impossible filter (always hidden)

Use contradictory conditions, e.g. field = "1" AND field = "2":
```json
{
  "conjunction": "and",
  "filterSet": [
    { "columnId": "fld...", "operator": "=", "value": "1" },
    { "columnId": "fld...", "operator": "=", "value": "2" }
  ]
}
```

---

## 3. Data Queries — `readQueries`

Fetches actual record data for an interface page. Sent after the page layout is loaded.

### Request

```
POST /v0.3/application/{baseId}/readQueries
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
```

**Body** (URL-encoded form):
- `stringifiedObjectParams` — URL-encoded JSON (see below)
- `requestId` — `req...`
- `secretSocketId` — `soc...` (optional, for realtime)

### Query Payload Structure

```json
{
  "queries": [
    {
      "id": "qry...",
      "spec": {
        "source": { /* see Source Types below */ },
        "columnIds": ["fld...", "fld..."],
        "sorts": [{ "columnId": "fld...", "ascending": true }],
        "filters": { /* see Filter Structure below */ },
        "virtualColumns": {
          "commentCounts": {
            "columnIds": ["fld..."],
            "includeRowLevelComments": false
          },
          "comments": {
            "isSubscriptionOnly": true,
            "includeRowLevelComments": true,
            "columnIds": ["fld..."]
          }
        },
        "realm": { "type": "application" },
        "mayHaveAcceptableAuthorizationError": false
      }
    }
  ],
  "subscribeToRealtimeUpdates": true,
  "allowMsgpackOfResult": true
}
```

### Source Types

#### Table source (list page)
```json
{ "type": "table", "tableId": "tbl..." }
```

#### Foreign key source (record detail — linked records)
```json
{
  "type": "foreignKey",
  "tableId": "tbl...",           // linked table
  "foreignTableId": "tbl...",    // source table
  "foreignColumnId": "fld...",   // link field on source table
  "foreignRowId": "rec..."       // current record ID
}
```

### Filter Structure (readQueries)

Filters in readQueries are more complex than visibility filters. They combine:
- **Interface element filters** (from page layout)
- **Permission filters** (row-level security)
- **Arbitrary column filters** (status filters, etc.)
- **Foreign key filters** (cross-table scoping)

#### Top-level filter
```json
{
  "conjunction": "and",
  "filterSet": [ /* nested filter groups */ ],
  "filterSourcePageElementId": "pel..."
}
```

#### Nested filter group
```json
{
  "type": "nested",
  "conjunction": "and" | "or",
  "filterSet": [ /* more filters or leaf conditions */ ],
  "filterSourcePageElementId": "pel...",
  "source": "permissionsFilters" | "arbitraryColumnFilters"
}
```

#### Leaf condition (column filter)
```json
{
  "columnId": "fld...",
  "operator": "isAnyOf" | "isEmpty" | "isNotEmpty" | "=" | "isNoneOf",
  "value": ["sel...", ...] | null
}
```

#### Column comparison
```json
{
  "type": "columnComparison",
  "columnId": "fld...",
  "operator": "isEmpty",
  "value": null
}
```

#### Foreign key filter (cross-table)
```json
{
  "type": "foreignKey",
  "sourceColumnId": "fld...",
  "foreignTableId": "tbl...",
  "foreignTableFilter": {
    "conjunction": "and",
    "filterSet": [ /* recursive filter structure */ ],
    "filterSourcePageElementId": "pel...",
    "type": "nested"
  }
}
```

#### Row IDs filter (record detail page)
```json
{
  "type": "rowIds",
  "rowIds": ["rec..."]
}
```

#### Special `filterSourcePageElementId` values
- `pelPAGENAVIGATION` — page-level navigation filter (record detail)
- `pel...` — references a specific page element that provides the filter context

### Response

Response uses **msgpack** format (binary, base64-encoded in HAR).

**Content-Type:** `application/msgpack`

The msgpack stream uses a custom Airtable serialization with `ExtType(code=114)` markers as map delimiters. The logical structure is:

```
{
  "msg": "SUCCESS",
  "data": {
    "applicationTransactionNumber": 1000000,
    "querySlices": [
      {
        "tableId": "tbl...",
        "columnIds": ["fld...", ...],
        "rowIds": ["rec...", ...],
        "colorByRowId": null | { "rec...": 66 }
      },
      ...
    ],
    "tableDataById": {
      "tbl...": {
        "id": "tbl...",
        "name": "TableName",
        "columns": [
          {
            "id": "fld...",
            "name": "FieldName",
            "type": "singleSelect",
            "typeOptions": { /* field config */ }
          }
        ]
      }
    },
    "failureReasonByQueryId": {},
    "signedUserContentUrls": {}
  }
}
```

#### Query Slice Structure

Each slice corresponds to one query in the request. Contains:
- `tableId` — which table the data is from
- `columnIds` — which fields were requested
- `rowIds` — ordered list of matching record IDs
- Cell values follow in the msgpack stream as parallel arrays (one value per columnId per rowId)

#### Cell Value Types in Response

| Airtable Field Type | msgpack Value |
|---------------------|---------------|
| `singleLineText` | `"string"` |
| `singleSelect` | `"sel..."` (option ID) |
| `multipleSelects` | `["sel...", ...]` |
| `multipleRecordLinks` | `["rec...", ...]` |
| `dateTime` | `"2026-03-25T10:00:00.000Z"` (ISO 8601) |
| `number` / `currency` | `123` or `123.45` |
| `rating` | `3` (integer) |
| `checkbox` | `true` / `null` |
| `multilineText` / `richText` | `"string with \n"` |
| `multipleAttachments` | `[{"id": "att...", "url": "...", ...}]` |
| `formula` | Computed value (string, number, or date) |
| `rollup` | Computed value |
| `aiText` | `{"state": "generated", "value": "...", ...}` |
| `autoNumber` | `123` |
| `createdTime` | `"2026-03-25T10:00:00.000Z"` |
| `duration` | `3600` (seconds as integer) |
| `url` | `"https://..."` |
| `email` | `"user@example.com"` |
| `phoneNumber` | `"+1234567890"` |
| `button` | `null` (buttons are UI-only) |

---

## 4. Record Open Event — `emitOpenRecordDetailsFromInterfaceEvent`

Tracks when a user opens a record in an interface. Fires on navigation to a record detail page.

### Request

```
POST /v0.3/emitOpenRecordDetailsFromInterfaceEvent
Content-Type: application/json
```

```json
{
  "enterpriseAccountId": "entr...",
  "applicationId": "app...",
  "interface": {
    "id": "pbd...",
    "name": "Meetings"
  },
  "entryPage": {
    "id": "pag...",
    "name": "Overview"
  },
  "table": {
    "id": "tbl...",
    "name": "Meetings"
  },
  "recordId": "rec...",
  "interfaceViewMode": "edit",
  "_csrf": "..."
}
```

### Response

```json
{ "success": true }
```

---

## 5. ID Prefix Reference

| Prefix | Entity |
|--------|--------|
| `app` | Base (application) |
| `tbl` | Table |
| `fld` | Field (column) |
| `viw` | View |
| `rec` | Record (row) |
| `sel` | Select option |
| `att` | Attachment |
| `pag` | Interface page |
| `pbd` | Interface (published dashboard) |
| `pel` | Page element |
| `pls` | Slot element |
| `pla` | Canvas area |
| `plf` | Full canvas element |
| `peo` | Page element output |
| `qry` | Query |
| `req` | Request ID |
| `soc` | Socket ID |
| `pglo` | Page load ID |
| `entr` | Enterprise account |

---

## 6. Interface Navigation Flow

### Page load sequence

1. **`readDraft`** — GET page layout (elements, visibility, slots)
2. **`readQueries`** — POST data queries for the list page (companies + meetings)
3. User clicks a record →
4. **`emitOpenRecordDetailsFromInterfaceEvent`** — POST tracking event
5. **`readDraft`** — GET record detail page layout
6. **`readQueries`** — POST 10-12 queries for all linked record elements on the detail page

### Multi-page interfaces

Each interface (`pbd...`) has multiple pages (`pag...`). Each page has its own `readDraft` layout. Pages observed in this capture:

| Page ID | Name | Root Table | Elements | Purpose |
|---------|------|-----------|----------|---------|
| `pagBBBBBBBBBBBBBBB` | (Company list) | `tblAAAAAAAAAAAAAAAA` (Companies) | 207 | Company overview with meetings |
| `pagAAAAAAAAAAAAAAAA` | (Meeting detail) | `tblBBBBBBBBBBBBBBB` (Meetings) | 121 | Single meeting record |
| `pagCCCCCCCCCCCCCCC` | (Action detail) | `tblCCCCCCCCCCCCCCC` (Actions) | 20 | Single action record |

### Interface metadata (from event payload)

```json
{
  "id": "pbdXXXXXXXXXXXXXXX",
  "name": "Meetings",
  "entryPage": { "id": "pagDDDDDDDDDDDDDDD", "name": "Overview" }
}
```

---

## 7. Query Patterns

### List page — two queries batched

1. **Companies query** — `source.type: "table"`, `tableId: tblAAAAAAAAAAAAAAAA`, requesting `Name` field only, with foreign key filter through Meetings table
2. **Meetings query** — `source.type: "table"`, `tableId: tblBBBBBBBBBBBBBBB`, requesting 12 display fields, filtered by Status + Company scoping

### Record detail page — 12 queries batched

1. **Main record** — `filter.type: "rowIds"`, all 42 fields
2. **Supplementary fields** — same record, different field set (attachments, presentations)
3-12. **Linked records** — `source.type: "foreignKey"`, one per linked record element:
   - Company (`fldSTATUS`)
   - Team (`fldDATE`)
   - Advisors (`fldCOMPANY`)
   - Contacts (`fldTEAM`)
   - Briefly contacts (`fldCHANNEL`)
   - Type (`fldTITLE`)
   - Epic (`fldEPIC`)
   - Sprints (`fldSPRINTS`)
   - Actions (`fldACTIONS`)
   - Followups (`fldADVISORS`)

---

## 8. Realtime Updates

Queries include `subscribeToRealtimeUpdates: true` and a `secretSocketId`. The socket connection (not captured in HAR) pushes incremental updates when records change. The `applicationTransactionNumber` in responses is used for ordering/deduplication.

---

## Appendix A: Complete Visibility Filter Map (Meetings Detail Page)

Resolved with field names from the Meetings table schema.

| Element ID | Element Type | Title/Field | Conjunction | Condition |
|------------|-------------|-------------|-------------|-----------|
| `pel...001` | button | — | AND | Status `isEmpty` |
| `pel...002` | section | — | AND | Status `isAnyOf` [Scheduled, Published, Summarize, Followup, Closed] |
| `pel...003` | section | Hidden Fields | AND | Title = "1" AND Title = "2" *(always hidden)* |
| `pel...004` | section | Shared With The Client | AND | Status `isAnyOf` [Summarize, Followup, Closed] |
| `pel...005` | cellEditor | Epic (linked) | AND | Company `\|` (is not empty) |
| `pel...006` | cellEditor | Location Address | AND | Channel `=` In-Person |
| `pel...007` | cellEditor | Objectives | OR | Objectives `isNotEmpty` OR Status `isAnyOf` [Prepare, Schedule, Pending, Scheduled] |
| `pel...008` | section | Recordings | AND | Status `isAnyOf` [Summarize, Followup, Closed] |
| `pel...009` | section | New Group | AND | Status `isNoneOf` [Prepare] |
| `pel...010` | cellEditor | — | AND | Company `\|` (is not empty) |
| `pel...011` | cellEditor | — | AND | Status(Company) `\|` [First Call, Idea, Negotiation] AND Transparent(Type) `=` null |
| `pel...012` | cellEditor | Sprints (linked) | AND | Epic `isNotEmpty` |
| `pel...013` | cellEditor | Agenda | OR | Agenda `isNotEmpty` OR Status `isAnyOf` [Pending, Scheduled, Schedule, Prepare] |
| `pel...014` | section | Internal Summary | AND | Status `isAnyOf` [Summarize, Followup, Closed] |
| `pel...015` | button | — | AND | Status `isAnyOf` [Scheduled, Published] AND Location URL `isNotEmpty` |
| `pel...016` | attachmentCarousel | Presentation | OR | Presentation `isNotEmpty` OR Status `isAnyOf` [Prepare] |
| `pel...017` | section | Followup | AND | Status `isAnyOf` [Followup, Summarize, Closed] |
| `pel...018` | cellEditor | External Title | OR | External Title `isNotEmpty` OR Status `isAnyOf` [Scheduled, Pending, Schedule, Prepare] |
| `pel...019` | cellEditor | Followup Date | AND | Followup `isNotEmpty` |
| `pel...020` | cellEditor | Purpose | OR | Purpose `isNotEmpty` OR Status `isAnyOf` [Prepare, Schedule, Pending, Scheduled, Published] |
| `pel...021` | section | Time | AND | Status `isAnyOf` [Schedule, Pending, Scheduled, Published, Summarize] |
| `pel...022` | cellEditor | Advisors | AND | Advisors `isNotEmpty` |
| `pel...023` | section | — | AND | Status `isAnyOf` [Summarize, Followup, Closed] |
| `pel...024` | cellEditor | — | AND | Channel `isAnyOf` [Zoom] |
| `pel...025` | section | Time | AND | Status `isAnyOf` [Closed, Followup] |
| `pel...026` | section | Meeting | AND | Status `isNoneOf` [Prepare, Schedule, Pending] |
| `pel...027` | button | — | AND | Status `isAnyOf` [Published, Scheduled, Pending, Schedule, Prepare] |

---

## Appendix B: Status Lifecycle (Meeting)

The Status field (`fldPRESENTATION`) drives all visibility. The lifecycle:

```
Prepare → Schedule → Pending → Scheduled → Published → Summarize → Followup → Closed
                                                                              → Canceled
                                                                              → No Show
```

| Status | Select ID | In list filter | Sections visible |
|--------|-----------|---------------|-----------------|
| Prepare | `selOPTION1` | Yes | Objectives, Agenda, External Title, Purpose, Presentation |
| Schedule | `selOPTION2` | Yes | + Time |
| Pending | `selOPTION3` | Yes | + Time |
| Scheduled | `selOPTION4` | Yes | + Time, New Group, Meeting |
| Published | `selOPTION5` | Yes | + Time, New Group, Meeting |
| Summarize | `selOPTION6` | Yes | + Recordings, Internal Summary, Shared With Client, Followup |
| Followup | `selOPTION7` | Yes | + Time (extra), Recordings, Internal Summary, Shared, Followup |
| Closed | `selOPTION8` | Sometimes | Same as Followup |
| Canceled | `selOPTION9` | No | — |
| No Show | `selOPTION10` | No | — |
