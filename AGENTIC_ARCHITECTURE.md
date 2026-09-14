# Agentic Architecture — All Agents Named

See **AGENTIC_ARCHITECTURE.pdf** and **AGENTIC_ARCHITECTURE.png**.

## Orchestrator

Coordinates phases, validates outputs, enforces gates. Does not invent PBIX objects.

---

## Phase 1 — Inventory (6 agents)

**Agents 1–5 run in PARALLEL**, then **Agent 6 Merger**.

| # | Agent | Role | Output |
|---|--------|------|--------|
| 1 | **Schema Agent** | Extract tables, columns, types, calc tables, internal auto-date tables | `inventory/01_tables_columns.json` |
| 2 | **Relationships Agent** | Extract all relationships (cardinality, cross-filter, active) | `inventory/03_relationships.json` |
| 3 | **DAX Agent** | Extract all measures, calculated columns/tables (full expressions) | `inventory/02_dax_objects.json` |
| 4 | **Power Query M Agent** | Extract verbatim M; one `.m` per query | `04_power_query_m.json` + `04_m_raw/` |
| 5 | **TM Extras Agent** | Partitions, hierarchies, RLS/OLS, annotations, auto dates (`[]` if empty) | `inventory/05_tmschema_extras.json` |
| 6 | **Merger Agent** | Merge 1–5; action matrix; completeness gate | `OBJECT_INVENTORY.md`, `ACTION_MATRIX.csv`, `COMPLETENESS_GATE.json` |

**Gate:** Phase 2 starts only if `COMPLETENESS_GATE = PASS`.

Script: `inventory/run_phase1_six_agents.py`

---

## Phase 2 — Mapping (4 agents — different from Phase 1)

**Agents A–C run in PARALLEL**, then **Agent D Merger**.  
**No LookML / no warehouse SQL** in this phase.

| # | Agent | Role | Output |
|---|--------|------|--------|
| A | **Tables/Columns Mapping** | Map tables → views; columns → dimensions (incl. internal) | `phase2_agents/01_tables_columns_mapping.md` |
| B | **DAX Mapping** | Map measures & calc objects; flag COMPLEX DAX | `phase2_agents/02_dax_mapping.md` |
| C | **Rel / M / TM Mapping** | Map joins, Power Query destinations, RLS, hierarchies, auto dates | `phase2_agents/03_rels_m_tm_mapping.md` |
| D | **Mapping Merger** | Build full assessment + PDF; merge gate | `LOOKML_MAPPING_ASSESSMENT.md` / `.pdf` |

**Gate:** `phase2_agents/PHASE2_MERGE_GATE.json = PASS`

---

## Phase 3 — Implementation (3 subagents)

| # | Agent | Role | Output |
|---|--------|------|--------|
| W | **Warehouse Gaps** | Only M/DAX gaps; **base tables assumed present** | `phase3_agents/01_warehouse_gaps.md` + `phase3/warehouse_sql/` |
| L | **LookML Builder** | Views, measures, joins, model; TODO for complex DAX | `phase3/views/`, `phase3/models/` |
| C | **Coverage / Docs** | Accountability matrix + developer/migration guides | `phase3/IMPLEMENTATION_COVERAGE.md`, guides |

Folder: `phase3/` + `phase3_agents/`

---

## Thesis

Capture everything → Map with specialists → Implement with accountability → Validate KPIs later.  
**Never silently drop objects. Never fake complex DAX equivalence.**
