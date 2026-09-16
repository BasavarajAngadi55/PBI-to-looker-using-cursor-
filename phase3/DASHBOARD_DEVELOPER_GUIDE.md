# Dashboard Developer Guide — Phase 3

_Generated 2026-09-16 12:26 UTC_

## Purpose

Convert Power BI report **pages** into Looker **LookML dashboards** using deterministic rules.
This is best-effort functional parity — **not** pixel-perfect recreation.

**Weighted completion:** 75.1% (target ≥ 70%).

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

- **Overview** → `dashboards/overview.dashboard.lookml` (8 visuals)
- **Geographic / Location Analysis** → `dashboards/geographic_location_analysis.dashboard.lookml` (12 visuals)
- **Revenue Analysis** → `dashboards/revenue_analysis.dashboard.lookml` (13 visuals)
- **Customer Analysis** → `dashboards/customer_analysis.dashboard.lookml` (12 visuals)
- **Rental Analysis** → `dashboards/rental_analysis.dashboard.lookml` (12 visuals)
- **Film Analysis** → `dashboards/film_analysis.dashboard.lookml` (14 visuals)
- **Actor Analysis** → `dashboards/actor_analysis.dashboard.lookml` (10 visuals)
- **Q1** → `dashboards/q1.dashboard.lookml` (3 visuals)
- ** Q2** → `dashboards/q2.dashboard.lookml` (4 visuals)
- **Q3** → `dashboards/q3.dashboard.lookml` (3 visuals)
- **Q4** → `dashboards/q4.dashboard.lookml` (3 visuals)
- **Q5** → `dashboards/q5.dashboard.lookml` (3 visuals)
- **Q6** → `dashboards/q6.dashboard.lookml` (3 visuals)
- **Q7** → `dashboards/q7.dashboard.lookml` (4 visuals)
- **Q8** → `dashboards/q8.dashboard.lookml` (3 visuals)
- **Q9** → `dashboards/q9.dashboard.lookml` (3 visuals)
- **Q10** → `dashboards/q10.dashboard.lookml` (3 visuals)
- **Q11** → `dashboards/q11.dashboard.lookml` (3 visuals)
- **Q12** → `dashboards/q12.dashboard.lookml` (3 visuals)
- **Q13** → `dashboards/q13.dashboard.lookml` (3 visuals)
- **Q14** → `dashboards/q14.dashboard.lookml` (3 visuals)
- **Q15** → `dashboards/q15.dashboard.lookml` (3 visuals)
- **Q16** → `dashboards/q16.dashboard.lookml` (3 visuals)
- **Q17** → `dashboards/q17.dashboard.lookml` (3 visuals)
- **Q18** → `dashboards/q18.dashboard.lookml` (3 visuals)
- **Q19** → `dashboards/q19.dashboard.lookml` (3 visuals)
- **Q20** → `dashboards/q20.dashboard.lookml` (3 visuals)
- **Q21** → `dashboards/q21.dashboard.lookml` (3 visuals)
- **Q22** → `dashboards/q22.dashboard.lookml` (3 visuals)
- **Q23** → `dashboards/q23.dashboard.lookml` (3 visuals)
- **Q24** → `dashboards/q24.dashboard.lookml` (3 visuals)
- **Q25** → `dashboards/q25.dashboard.lookml` (3 visuals)
- **Q26** → `dashboards/q26.dashboard.lookml` (3 visuals)
- **Q27** → `dashboards/q27.dashboard.lookml` (3 visuals)
- **Q28** → `dashboards/q28.dashboard.lookml` (3 visuals)
- **Q29** → `dashboards/q29.dashboard.lookml` (3 visuals)
- **Q30** → `dashboards/q30.dashboard.lookml` (3 visuals)

## Coverage summary

- Mapped / generated: 70
- Partial: 99
- Gaps / skipped: 4 gaps; 0 decorative skips
- Weighted completion: **75.1%**

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
