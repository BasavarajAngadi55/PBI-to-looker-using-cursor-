# Looker Developer Guide — HR Sample (Phase 3)

Guide for maintaining the migrated LookML semantic model.  
Design sources: `OBJECT_INVENTORY.md`, `LOOKML_MAPPING_ASSESSMENT.md`, `MIGRATION_SUMMARY.md`.

**KPI parity is NOT YET VALIDATED.**

---

## 1. Project Structure

```text
# Repo root
inventory/                      # Phase 1
LOOKML_MAPPING_ASSESSMENT.md    # Phase 2
PROMPT.md

phase3/                         # Phase 3 (this folder)
  LOOKER_DEVELOPER_GUIDE.md
  MIGRATION_SUMMARY.md
  IMPLEMENTATION_COVERAGE.md
  warehouse_sql/                # gap/reference templates only
  views/
  models/human_resources.model.lkml

phase3_agents/
  01_warehouse_gaps.md          # M/DAX gaps only (base tables assumed)
```

If your LookML project root is `phase3/`, keep `include: "/views/*.view.lkml"`.

Replace placeholders:

- Looker: `connection: "YOUR_LOOKER_CONNECTION"`
- BigQuery: `` `YOUR_PROJECT.YOUR_DATASET` `` and `` `YOUR_PROJECT.SOURCE_DATASET` ``

---

## 2. Naming Standards

| Object | Convention | Example |
|--------|------------|---------|
| View file | `snake_case.view.lkml` | `employee.view.lkml` |
| View name | snake_case | `employee` |
| Dimension | snake_case | `empl_id`, `ethnic_group` |
| Dimension group | noun | `snapshot`, `hire`, `term` |
| Measure | snake_case matching PBI intent | `new_hires`, `to_pct` |
| Join | view name | `join: gender` |
| Model | descriptive | `human_resources` |
| Explore | primary fact | `explore: employee` |

Preserve Power BI **business meaning** in `label:` even when SQL names differ.

---

## 3. Power BI → LookML Mapping Rules

```text
Power BI Table            → LookML View
Power BI Column           → LookML Dimension / dimension_group
Power BI Measure          → LookML Measure
Power BI Relationship     → LookML Join (explore)
Power Query / DAX gaps    → Warehouse add-on only if not on base (see § Warehouse)
Power BI RLS              → Looker Security (none in this PBIX)
Power BI Auto Date Table  → Internal/Skip (use business date)
```

---

## Warehouse layer (assumptions)

**Base warehouse tables are assumed to exist** (e.g. `AllEmps`, `Date`, `BU`, `FP`, `PayGroup`, `TermReason`). Do not treat Phase 3 as a full source recreate.

What still matters for warehouse work:

| Gap class | Examples | When to apply |
|-----------|----------|---------------|
| Embedded seeds | AgeGroup, Gender, Ethnicity | If those dims are missing |
| Employee.m transforms | UNION actives/seps, gender remap, +1 year dates, filters | If base is not already the Employee fact grain |
| Calculated columns | `isNewHire`, `AgeGroupID`, tenure, `BadHires`, `BU.Region`, `Date.MonthIncrementNumber` | If not already materialized |

`phase3/warehouse_sql/` is **gap / reference templates only** (including full-dim scripts). Prefer pointing LookML `sql_table_name` at existing bases; run or adapt a template only for a documented M/DAX gap. Inventory: `phase3_agents/01_warehouse_gaps.md`.

---

## 4. Measure Development Standards

| Pattern | LookML |
|---------|--------|
| SUM(column/flag) | `type: sum` |
| COUNT / COUNTA | `type: count` or `count_distinct` |
| Distinct people | Prefer `count_distinct` on `EmplID` |
| AVERAGE | `type: average` |
| Ratios / YoY / DIVIDE | `type: number` + `SAFE_DIVIDE()` |
| Percent display | `value_format_name: percent_1` |
| Decimal | `value_format_name: decimal_0` / `decimal_1` |

Never claim equivalence for complex DAX without a parity test.

---

## 5. Complex DAX Standards

| Pattern | This project |
|---------|--------------|
| CALCULATE + TermDate blank/not blank | Filtered measures (`actives`, `seps`) — PARTIAL vs EmpCount nesting |
| FILTER(ALL(PeriodNumber)=MAX) | **TODO** on `emp_count` |
| SAMEPERIODLASTYEAR | **TODO** NULL stubs (`*_sply`) |
| ALL(Gender/Ethnicity) | **TODO** on `to_pct_norm` |
| DIVIDE / arithmetic YoY | Implemented; blocked until SPLY parents work |
| SUMX / AVERAGEX / RANKX / USERELATIONSHIP | Not present as primary measure patterns here; if added later → warehouse or TODO |

Warehouse SQL is preferred for reusable row-level calc columns (`isNewHire`, tenure, BadHires).

---

## 6. Join Standards

All Phase 1 relationships are **M:1**, **Single**, **active**.

```lookml
type: left_outer
relationship: many_to_one
```

| Fanout risk | Mitigation |
|-------------|------------|
| Joining dims to fact | many_to_one from employee |
| Bidirectional | None in source |
| Many-to-many | None in source |
| Bridge | Not required |

Do not add joins absent from `inventory/03_relationships.json` without documenting why.

---

## 7. Dimension Standards

- Types: `string`, `number`, `yesno`, `date` / `dimension_group`
- Always set `label:`; add `description:` for grain / join keys
- Keys: `primary_key: yes` on dim PKs
- Sort: `order_by_field:` (Gender.Sort)
- Hidden: helper fields (e.g. sort)
- Dates: `dimension_group` with useful timeframes
- Drill: Date `yqm_drill` set approximates Power BI YQM hierarchy

---

## 8. Security Standards

Phase 1/2: **RLS = NONE_IN_SOURCE**.

No `access_grant` / `sql_always_where` implemented.

If a future PBIX has RLS:

```text
# TODO: USER INPUT REQUIRED
# Do not invent user_attribute names
```

Map from mapping assessment only.

---

## 9. Testing Standards

1. **Object coverage** — every inventory row in `IMPLEMENTATION_COVERAGE.md`
2. **SQL** — warehouse scripts compile against real sources (after placeholder replacement)
3. **LookML validate** — Looker IDE / `lookml validator`
4. **Joins** — Gender/Region/AgeGroup labels non-null for known keys
5. **Measures** — Actives/Seps/New Hires for one month vs Power BI
6. **Fanout** — row counts don’t explode when joining dims
7. **Nulls** — TermDate null = active
8. **Edge** — BadHires 60-day boundary

**Do not mark KPI parity PASS without compared numbers.**

---

## 10. Developer Rules

1. Never silently remove a Power BI object — use TODO / SKIP / PARTIAL.
2. Preserve business logic; document deviations (`Actives` vs EmpCount nesting).
3. Prefer warehouse for reusable M/DAX **gaps** only; base tables assumed; avoid unnecessary PDTs.
4. No hard-coded real project IDs — use `YOUR_PROJECT.YOUR_DATASET`.
5. Unresolved logic → `# TODO:` with DAX + reason + next step.
6. Validate measures against Power BI before claiming done.
7. Do not contradict `LOOKML_MAPPING_ASSESSMENT.md` without a Migration Note.

---

## Quick start (after warehouse exists)

1. Confirm base tables exist; apply only M/DAX gaps from `phase3_agents/01_warehouse_gaps.md` (seeds / Employee.m / calc cols). Use `warehouse_sql/` as templates — not mandatory full DDL.
2. Set `connection:` in `models/human_resources.model.lkml`.
3. Align every view `sql_table_name` to base or gap add-ons.
4. LookML Validate → Explore **Human Resources**.
5. Smoke: Actives, Seps, New Hires by Month × Gender.
6. Park SPLY / EmpCount / TO % Norm until PoP work.
7. Update `MIGRATION_SUMMARY.md` progress table as you close TODOs.
