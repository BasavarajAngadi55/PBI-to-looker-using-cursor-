# Dashboard Developer Guide — Phase 3

_Generated 2026-09-16 09:59 UTC_

## Purpose

Convert Power BI report **pages** into Looker **LookML dashboards** using deterministic rules.
This is best-effort functional parity — **not** pixel-perfect recreation.

**Weighted completion:** 83.9% (target ≥ 70%).

## What Looker gets

| Power BI | Looker equivalent | Notes |
|----------|-------------------|-------|
| Report page | `.dashboard.lookml` | One file per page |
| Card / KPI | `single_value` | Primary measure |
| Clustered bar/column | `looker_bar` / `looker_column` | Category + measure |
| Line / area | `looker_line` / `looker_area` | Time/category + measure |
| Pie / donut | `looker_pie` | Category + measure |
| Table / matrix | `looker_grid` | Dimensions + measures |
| Slicer | Dashboard `filters` + `listen` | Cross-tile filtering |
| Text box | `text` tile | Title/subtitle |
| Shape / image / button | Skipped or gap tile | See deficiencies |

## Prerequisites

1. Phase 1 inventory exists for the same PBIX.
2. Phase 2 LookML model + explore are generated.
3. Warehouse tables / views behind Phase 2 are deployed (or use SQL runner).

## Deploy LookML dashboards

1. Unzip `LOOKML_DASHBOARDS.zip`.
2. Copy `dashboards/*.dashboard.lookml` into your LookML project (same project as Phase 2).
3. Ensure each dashboard `model:` and tile `explore:` match Phase 2 names.
4. Validate in Looker IDE; deploy to a non-prod folder.
5. Open each dashboard; fix any red fields (missing from explore).

## Page inventory

- **Project Overview** → `dashboards/project_overview.dashboard.lookml` (1 visuals)
- **Executive Summary** → `dashboards/executive_summary.dashboard.lookml` (23 visuals)
- **Hospital Insights** → `dashboards/hospital_insights.dashboard.lookml` (18 visuals)
- **Patient Analysis** → `dashboards/patient_analysis.dashboard.lookml` (22 visuals)
- **Payer-Provider Analysis** → `dashboards/payer_provider_analysis.dashboard.lookml` (17 visuals)
- **Monthly Expenses Trends** → `dashboards/monthly_expenses_trends.dashboard.lookml` (2 visuals)

## Coverage summary

- Mapped / generated: 48
- Partial: 22
- Gaps / skipped: 5 gaps; 8 decorative skips
- Weighted completion: **83.9%**

## Deficiencies (expected)

- Bookmarks / buttons / page navigation
- Drillthrough / drill-down hierarchies as PBI defines them
- Custom visuals / R / Python visuals
- Exact pixel layout, themes, backgrounds, images
- Combo charts, treemaps, maps (partial or gap tiles)
- Sync slicers across pages (configure manually if needed)

Each gap appears as a **text tile** on the Looker dashboard so nothing is silently dropped.

## How to reach ~100%

1. Replace gap tiles with native Looker viz or extensions.
2. Add missing fields to Phase 2 views / explores.
3. Rebuild complex KPI cards with `single_value` + comparison measures.
4. Recreate navigation with Looker dashboard links / folders.
5. Apply Looker themes / CSS for brand parity (optional).

## Hard rules

- Never invent visuals that are not in the PBIX layout.
- Field references must resolve via Phase 2 naming.
- Report weighted coverage honestly — do not claim pixel parity.
