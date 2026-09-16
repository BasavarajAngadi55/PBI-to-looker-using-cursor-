# Phase 3 — Looker dashboard migration

Deterministic conversion of **Power BI report pages** into:

1. **LookML dashboards** (one `.dashboard.lookml` per page)  
2. **Dashboard Developer Guide** (PDF) — PBI ↔ Looker equivalence + gaps  
3. **PAGE_COMPARISON.md** — side-by-side visual inventory  
4. **Coverage score** — weighted completion (target ≥ 70%)

**Approach:** fixed Python rules (no LLM). Layout from PBIX `Report/Layout`; fields bound to Phase 2 explores. Pixel-perfect is **not** claimed.

## Quick start

```bash
# Prerequisites: Phase 1 inventory + Phase 2 LookML for the same PBIX

cd phase3
../.venv312/bin/python run_phase3.py
# or:
../.venv312/bin/python run_phase3.py --pbix ../phase1/uploads/dashboards.pbix
```

## Deliverables

| File | Purpose |
|------|---------|
| [AGENTIC_ARCHITECTURE.pdf](AGENTIC_ARCHITECTURE.pdf) | Deterministic dashboard migration architecture |
| [DASHBOARD_DEVELOPER_GUIDE.pdf](DASHBOARD_DEVELOPER_GUIDE.pdf) | How to deploy + finish gaps |
| [LOOKML_DASHBOARDS.zip](LOOKML_DASHBOARDS.zip) | All `.dashboard.lookml` + comparison |
| `comparison/PAGE_COMPARISON.md` | Power BI visual → Looker equivalent per page |
| `inventory/COVERAGE.json` | Weighted completion % |
| `PHASE3_SUMMARY.json` | Run summary |

## What maps well vs gaps

**Strong:** cards, bar/column/line/area/pie, tables/matrices, slicers→filters.  
**Partial:** KPI trend/goal, donut, combo, treemap, maps, rich text.  
**Gaps / skip:** shapes, images, action buttons, bookmarks, drillthrough, custom visuals, themes.

## Layout

```text
phase3/
  PROMPT.md
  run_phase3.py
  extract_report_layout.py
  generate_lookml_dashboards.py
  generate_dashboard_guide.py
  generate_architecture_assets.py
  lib/                  # naming + visual_mapping
  inventory/            # generated
  lookml_dashboards/    # generated
  comparison/           # generated
```

## Before Looker validate

1. Deploy Phase 2 model/views first (same project).  
2. Copy `lookml_dashboards/dashboards/*.dashboard.lookml` into that project.  
3. Confirm `model:` / `explore:` match Phase 2.  
4. Open each dashboard; fix red fields; replace gap text tiles as needed.
