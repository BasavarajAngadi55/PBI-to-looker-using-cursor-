# Power BI → Looker — Phase 2 ONLY: Deterministic LookML mapping + developer guide

You are the **Orchestrator** for Phase 2.

## Approach (important)

Phase 2 is **deterministic** Python — **not** LLM / agentic generation.  
It reads Phase 1 inventory JSON and emits LookML + a Looker developer guide with fixed rules.

References used for mapping standards:

- [LookML terms and concepts](https://cloud.google.com/looker/docs/lookml-terms-and-concepts)
- [looker-open-source/looker-skills](https://github.com/looker-open-source/looker-skills) (`lookml-view`, `lookml-explore`, `lookml-modeling-guidelines`)

## Scope

- Map every Phase 1 object class to Looker equivalents (guide + ledger)
- Generate LookML: `manifest.lkml`, model, views (dimensions, measures, joins/explores)
- Produce **Looker Developer Guide** PDF (`LOOKER_DEVELOPER_GUIDE.pdf`)
- Package LookML into **`LOOKML_PROJECT.zip`**

## Out of scope

- Re-extracting the PBIX (that is Phase 1)
- Warehouse SQL / ETL implementation (document only)
- KPI parity certification
- Report/visual migration
- Calling an LLM

## INPUT

Phase 1 inventory directory (default `../phase1/inventory`):

- `01_tables_columns.json`
- `02_dax_objects.json`
- `03_relationships.json`
- `04_power_query_m.json`
- `05_tmschema_extras.json`
- `OBJECT_COUNTS.json`

## OUTPUT

```text
phase2/
  LOOKER_DEVELOPER_GUIDE.md
  LOOKER_DEVELOPER_GUIDE.pdf
  OBJECT_MAPPING.md
  OBJECT_MAPPING.json
  LOOKML_PROJECT.zip
  PHASE2_SUMMARY.json
  lookml/
    manifest.lkml
    models/<pbix>.model.lkml
    views/*.view.lkml
```

## Mapping rules (fixed)

| Power BI | Looker |
|---|---|
| Business table | `view` |
| Column | `dimension` / `dimension_group` |
| Measure | `measure` (pattern-based from DAX) |
| Relationship | `explore` `join` + `relationship:` |
| Calculated column | `dimension` (warehouse preferred) |
| Calculated table | `view` (placeholder `sql_table_name`) |
| Power Query M | Warehouse / ETL (not LookML) |
| Hierarchy | `drill_fields` / timeframes |
| RLS | `access_grant` / `access_filter` (if present) |
| Auto-date tables | Skip |

## ORCHESTRATOR WORKFLOW

```bash
cd phase2
../.venv312/bin/python run_phase2.py
```

1. Load Phase 1 inventory  
2. Generate LookML (`generate_lookml.py`)  
3. Generate developer guide MD+PDF (`generate_developer_guide.py`)  
4. Zip `lookml/` → `LOOKML_PROJECT.zip`  
5. Write `PHASE2_SUMMARY.json`

Accuracy over invention: only emit objects present in inventory; mark complex DAX as TODO with original expression preserved.
