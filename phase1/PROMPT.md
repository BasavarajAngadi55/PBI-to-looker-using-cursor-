# Power BI → Looker — Phase 1 ONLY: Extract Semantic Model + Data Model

You are the **Orchestrator** for Phase 1 of a Power BI semantic-model extraction.

## Approach (important)

Phase 1 is **deterministic** (Python + `pbixray`) — **not** an LLM / agentic extract.  
Six specialist **stages** write inventory files with fixed code. Same PBIX → same outputs.

**Optional later (out of scope here):** enable natural-language conversation on top of the finished inventory to make the system **agentic** — users can ask any question about the **current** uploaded PBIX (inventory is wiped and rewritten each extract). That agent must not invent model objects; extract stays deterministic.

## Scope (this phase only)

- Extract **every** semantic-model object from the PBIX
- Produce inventory JSON + verbatim M + object inventory
- Produce a **data model** file/diagram (`DATA_MODEL.md` / `.pdf` / `.png`)
- Print a **summary of all objects and counts** at the end

## Out of scope

Do **NOT**:

- Load or generate sample/table row data
- Create warehouse SQL
- Create LookML / views / models
- Run Phase 2 or Phase 3
- Run completeness gates or PASS/FAIL validation
- Invent objects, columns, relationships, DAX, or M
- Call an LLM during extract

We are migrating **only the semantic model and business logic** eventually — not report pages, visuals, dashboards, bookmarks, or themes. NL Q&A over inventory is a future optional layer, not part of extract.

---

## INPUT

Pass the **current** PBIX path (CLI or Streamlit upload). Do **not** hardcode an old sample.

Examples:

- CLI: `../.venv312/bin/python inventory/run_phase1_six_agents.py "/path/to/current.pbix"`
- UI: upload a `.pbix` — it becomes the only file under `phase1/uploads/`

If no path is passed, the runner uses `CURRENT_PBIX.json` or the single file in `phase1/uploads/`.

Workspace: use the **currently opened Cursor workspace**. Write outputs there.

Use Python 3.12 (`.venv312`) and `pbixray` if needed.

---

## ARCHITECTURE — 6 deterministic extract stages

Run specialists **1–5**, then **6 Merger** (fixed Python modules; no LLM):

1. **Tabular Schema** — tables, columns, calculated tables, internal auto-date tables
2. **Relationships** — every relationship (cardinality, cross-filter, active)
3. **DAX** — all measures, calculated columns, calculated tables (full expressions)
4. **Power Query M** — full M per query + `04_m_raw/<Name>.m`
5. **TM Extras** — partitions, hierarchies, RLS/OLS, annotations, format/sort, auto dates (`[]` if empty)
6. **Merger** — `OBJECT_INVENTORY.md` + `OBJECT_COUNTS.json` + object summary counts

Then regenerate the data model diagram from inventory.

---

## COMMON RULES

Every extract stage must:

1. Read the PBIX with `pbixray` (or equivalent)
2. Never invent objects or rewrite DAX/M
3. Preserve **exact** original names and **full** expressions
4. Capture empty categories as `[]` (do not omit)
5. Include Power BI internal objects (`LocalDateTable_*`, `DateTableTemplate_*`) completely
6. Write only to the specified `inventory/` paths
7. Not modify another stage’s files

---

## STAGE 1 — TABULAR SCHEMA

Capture for every table: name, type, hidden/visible, description.  
Capture for every column: table, name, data type, source column, hidden/visible, calculated flag, expression/format/description if available.  
List calculated tables and **all** internal auto-date tables.

**Output:** `inventory/01_tables_columns.json`

```json
{
  "tables": [],
  "columns": [],
  "calculated_tables": [],
  "internal_tables": []
}
```

---

## STAGE 2 — RELATIONSHIPS

Capture every relationship: from/to table & column, cardinality, cross-filter, active/inactive, type, any security/filter metadata. Do not invent missing metadata.

**Output:** `inventory/03_relationships.json`

---

## STAGE 3 — DAX

Extract **all** measures, calculated columns, and calculated tables with **complete** DAX. Optionally classify SIMPLE / MODERATE / COMPLEX as a migration aid only (do not rewrite DAX).

**Output:** `inventory/02_dax_objects.json`

---

## STAGE 4 — POWER QUERY M

Extract **all** M exactly. Tag SQL/embedded/append/merge/transforms. Write:

- `inventory/04_power_query_m.json`
- `inventory/04_m_raw/<QueryName>.m` (one file per query)

---

## STAGE 5 — TM EXTRAS

Capture partitions, hierarchies, RLS (`"rls": []` if none), perspectives, annotations, display folders, sort-by, format strings, auto date tables, other useful Tabular metadata.

**Output:** `inventory/05_tmschema_extras.json`

---

## STAGE 6 — MERGER

Merge stages 1–5 into:

- `inventory/OBJECT_INVENTORY.md` — full readable inventory
- `inventory/OBJECT_COUNTS.json` — machine-readable counts

**Do not** create `COMPLETENESS_GATE.json` or `ACTION_MATRIX.csv`.  
**Do not** run PASS/FAIL validation.

---

## DATA MODEL (required end product)

After inventory exists, generate:

- `DATA_MODEL.pdf` — **primary** (ER diagram + relationships; download and zoom)
- `DATA_MODEL.md` — text/mermaid companion
- `DATA_MODEL.png` — source render used to build the PDF pages (not shown in UI)

Prefer:

```bash
.venv312/bin/python generate_data_model_diagram.py
```

---

## ORCHESTRATOR WORKFLOW

1. Check PBIX path  
2. Ensure `inventory/` and `inventory/04_m_raw/`  
3. Run extract stages 1–5  
4. Run Merger (inventory + counts only)  
5. Generate DATA_MODEL assets  
6. Print the object summary (below)

Preferred one-shot extract:

```bash
.venv312/bin/python inventory/run_phase1_six_agents.py
.venv312/bin/python generate_data_model_diagram.py
```

---

## FINAL SUMMARY (print this)

```text
PHASE 1 COMPLETE — OBJECT SUMMARY

Tables:
  Business:
  Internal auto-date:
Columns:
Measures:
Calculated columns:
Calculated tables:
Relationships:
Power Query queries:
M raw files:
Hierarchies:
Partitions:
Auto date tables:
RLS roles:

Primary deliverable: DATA_MODEL.md / .pdf / .png
Inventory: inventory/OBJECT_INVENTORY.md
```

Accuracy over speed: capture everything that exists in the PBIX; leave empty lists empty; never invent.
