# Migration Summary — Power BI → Looker (Phase 3)

**Source PBIX:** Human Resources Sample  
**Phase 1 gate:** PASS  
**Phase 2 mapping:** `LOOKML_MAPPING_ASSESSMENT.md`  
**Phase 3 status:** PARTIAL implementation (accountable LookML + warehouse templates; **KPI parity NOT YET VALIDATED**)

---

## Pipeline

```text
Power BI Tabular
        ↓
Power Query / M
        ↓
Warehouse Layer   (base tables assumed; warehouse_sql/ = M/DAX gap templates only)
        ↓
LookML Semantic Model  (views/ + models/)
        ↓
Looker Explore
        ↓
KPI Parity Validation   ← not started
```

---

## 1. Migration Objective

### What is migrated
- Semantic model: tables, columns, measures, calculated columns/tables (as inventory), relationships, Power Query destinations, hierarchies (semantic), RLS status, partitions (documented).

### What is intentionally not migrated
- Report pages, visuals, dashboards, bookmarks, themes, Q&A UI.

### Target Looker architecture
- Base warehouse tables assumed present; add only M/DAX gaps (seeds, Employee.m fact transforms, calc cols).
- LookML views (one per business table) + `human_resources` model explore with 8 joins.
- Complex DAX kept as `# TODO` until PoP / period / ALL() patterns + parity tests exist.

---

## 2. Source Model Summary (Phase 1)

| Object | Count |
|--------|------:|
| Tables | 15 |
| Business tables | 9 |
| Internal auto date tables | 6 |
| Columns | 87 |
| Measures | 30 |
| Calculated columns | 43 (7 business) |
| Calculated tables | 6 (all auto date) |
| Relationships | 8 |
| Power Query queries | 9 |
| Hierarchies | 7 |
| RLS roles | 0 |
| Partitions | 122 |
| Auto date tables | 6 |

---

## 3. Mapping Summary (Phase 2 → Phase 3)

| Category | Approach |
|----------|----------|
| Direct | 9 business tables → views; simple measures → sum/count_distinct/average/SAFE_DIVIDE |
| Partial | Actives vs EmpCount nesting; YoY formulas pending SPLY; Date YQM → drill set; partitions → warehouse refresh notes |
| Complex | EmpCount, * SPLY, TO % Norm → TODO stubs |
| Warehouse gaps only | Embedded seeds + Employee.m transforms + 7 biz calc cols (base tables assumed; see `phase3_agents/01_warehouse_gaps.md`) |
| Internal | LocalDateTable_* / DateTableTemplate_* → SKIP |
| Blocked | Measure format strings missing from extract; SOURCE_DATASET placeholders need user mapping |

---

## 4. Architecture Decisions

| Layer | What goes here | Why |
|-------|----------------|-----|
| **Warehouse** | Base tables assumed. Only M/DAX gaps: seeds if missing; Employee.m transforms; calc cols (`isNewHire`, tenure, `BadHires`, `BU.Region`, `MonthIncrementNumber`). `warehouse_sql/` = gap/reference templates only | Looker cannot run M/DAX; do not recreate full base DDL |
| **LookML** | Views, measures, joins, explore | Semantic layer for Explores |
| **PDT** | Not used in Phase 3 | Prefer gap templates / existing bases first |
| **Security** | N/A | RLS NONE_IN_SOURCE |
| **Skipped/internal** | Auto date tables/hierarchies | Replaced by business `date` + timeframes |

---

## 5. Implementation Progress

| Area | Total | Completed | Pending | Blocked | Notes |
|------|------:|----------:|--------:|--------:|-------|
| Tables (business views) | 9 | 9 | 0 | 0 | Internal 6 SKIP |
| Dimensions (source cols) | ~45 biz | ~45 | 0 | 0 | On views |
| Measures | 30 | 11 | 12 PARTIAL | 7 TODO | SPLY / EmpCount / TO % Norm |
| Calculated Columns (biz) | 7 | 7 | 0 | 0 | In warehouse + LookML |
| Calculated Tables | 6 | 0 | 0 | 0 | All SKIP_INTERNAL |
| Joins | 8 | 8 | 0 | 0 | model explore |
| M Transformations | 9 | 9 templates | 9 load | 0 | Placeholders — not executed |
| RLS | 0 | N/A | 0 | 0 | NONE_IN_SOURCE |

---

## 6. Known Gaps

| Object | Reason | Dependency | Impact | Recommended solution | Status |
|--------|--------|------------|--------|----------------------|--------|
| Employee.m load | SOURCE tables not connected | `YOUR_PROJECT.SOURCE_DATASET.*` | All KPIs | Map sources; run `09_fact_employee.sql`; validate counts | BLOCKED (env) |
| EmpCount | MAX PeriodNumber pattern | Date.PeriodNumber | Headcount / Actives nesting | always_filter / SQL max period + parity | TODO |
| * SPLY measures | SAMEPERIODLASTYEAR | Date explore | YoY family | Looker PoP / prior-year join | TODO |
| TO % Norm | ALL(Gender/Ethnicity) | dims | TO % Var | Filtered measure ignore dims | TODO |
| Gender/Ethnicity seed labels | Embedded M decode | PBIX values | Join labels | Validate seed vs PBIX | PARTIAL |
| Measure formats | Not in dax_measures extract | Power BI UI | Display | Infer %/decimal; confirm in PBI | PARTIAL |
| KPI parity | No compared run | Loaded warehouse + Looker | Trust | Side-by-side checklist | NOT STARTED |

---

## Related files

- `LOOKML_MAPPING_ASSESSMENT.md` / `.pdf` — Phase 2 design  
- `phase3/LOOKER_DEVELOPER_GUIDE.md` — developer standards  
- `phase3/IMPLEMENTATION_COVERAGE.md` — object-by-object status  
- `phase3_agents/01_warehouse_gaps.md` — M/DAX warehouse gaps only  
- `phase3/warehouse_sql/` — BigQuery gap/reference templates  
- `phase3/views/` · `phase3/models/human_resources.model.lkml`
