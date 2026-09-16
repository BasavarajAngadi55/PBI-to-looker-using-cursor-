# Power BI → Looker — Phase 3 ONLY: Deterministic dashboard migration

You are the **Orchestrator** for Phase 3.

## Approach (important)

Phase 3 is **deterministic** Python — **not** LLM / agentic generation.  
It reads PBIX `Report/Layout` + Phase 2 model/explore and emits LookML dashboards with honest coverage scoring (~70% target).

References:

- [Building LookML dashboards](https://cloud.google.com/looker/docs/building-lookml-dashboards)
- [Dashboard LookML type parameter](https://cloud.google.com/looker/docs/reference/param-lookml-dashboard-type)
- [looker-open-source/looker-skills](https://github.com/looker-open-source/looker-skills)

## Scope

- Extract Power BI report pages and visuals from PBIX `Report/Layout`
- Map each visual type to a Looker dashboard element (fixed rules)
- Bind fields to Phase 2 `view.field` / measures
- Emit one `.dashboard.lookml` per page (newspaper layout)
- Score weighted completion; produce PAGE_COMPARISON (PBI vs Looker)
- Package **`LOOKML_DASHBOARDS.zip`** + **Dashboard Developer Guide** PDF

## Out of scope

- Re-building semantic model / views (Phase 1 / 2)
- Pixel-perfect layout, themes, bookmarks, drillthrough, custom visuals
- Calling an LLM

## INPUT

- PBIX file (same as Phase 1; default from `phase1/CURRENT_PBIX.json` or `uploads/`)
- Phase 2 `PHASE2_SUMMARY.json` (model name, fact explore)
- Phase 1 inventory (for context / counts)

## OUTPUT

```text
phase3/
  AGENTIC_ARCHITECTURE.md / .pdf / .png
  DASHBOARD_DEVELOPER_GUIDE.md / .pdf
  LOOKML_DASHBOARDS.zip
  PHASE3_SUMMARY.json
  inventory/
    01_report_pages.json
    02_visuals.json
    03_dashboard_mapping.json
    COVERAGE.json
  lookml_dashboards/
    dashboards/*.dashboard.lookml
    README.md
  comparison/
    PAGE_COMPARISON.md
```

## Visual equivalence (fixed)

| Power BI | Looker |
|---|---|
| card / kpi | `single_value` |
| bar / column | `looker_bar` / `looker_column` |
| line / area | `looker_line` / `looker_area` |
| pie / donut | `looker_pie` |
| table / matrix | `looker_grid` |
| slicer | dashboard `filters` + `listen` |
| textbox | `text` |
| shape | skip (decorative) |
| image / button / unknown | gap tile / documented deficiency |

## ORCHESTRATOR WORKFLOW

```bash
cd phase3
../.venv312/bin/python run_phase3.py
```

1. Generate architecture diagram  
2. Extract `Report/Layout` → pages + visuals JSON  
3. Map visuals → Looker types + bind Phase 2 fields  
4. Emit `.dashboard.lookml` + coverage + PAGE_COMPARISON  
5. Generate Dashboard Developer Guide MD+PDF  
6. Zip dashboards + comparison → `LOOKML_DASHBOARDS.zip`  
7. Write `PHASE3_SUMMARY.json`

Hard rules: never invent visuals; field refs from inventory/Phase 2 only; report weighted % honestly.
