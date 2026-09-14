# Looker Developer Guide — HR Sample (Phase 3)

Guide for maintaining the migrated LookML semantic model.  
Design sources: `OBJECT_INVENTORY.md`, `LOOKML_MAPPING_ASSESSMENT.md`, `MIGRATION_SUMMARY.md`.

**KPI parity is NOT YET VALIDATED.**

---

## 1. Project Structure

```text
inventory/                 # Phase 1 extraction (do not delete)
LOOKML_MAPPING_ASSESSMENT.md
warehouse_sql/             # Phase 3 BigQuery templates (seeds + dims + fact)
views/                     # LookML views
models/human_resources.model.lkml
IMPLEMENTATION_COVERAGE.md
MIGRATION_SUMMARY.md
LOOKER_DEVELOPER_GUIDE.md  # this file
PROMPT.md                  # Phase 1 orchestrator prompt
```

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
Power Query Transformation→ Warehouse SQL / Seed (warehouse_sql/)
Power BI RLS              → Looker Security (none in this PBIX)
Power BI Auto Date Table  → Internal/Skip (use business date)
```

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
3. Prefer warehouse for reusable transforms; avoid unnecessary PDTs.
4. No hard-coded real project IDs — use `YOUR_PROJECT.YOUR_DATASET`.
5. Unresolved logic → `# TODO:` with DAX + reason + next step.
6. Validate measures against Power BI before claiming done.
7. Do not contradict `LOOKML_MAPPING_ASSESSMENT.md` without a Migration Note.

---

## Quick start (after warehouse exists)

1. Replace placeholders in `warehouse_sql/*.sql` and run in order `01`→`09`.
2. Set `connection:` in `models/human_resources.model.lkml`.
3. Align every view `sql_table_name`.
4. LookML Validate → Explore **Human Resources**.
5. Smoke: Actives, Seps, New Hires by Month × Gender.
6. Park SPLY / EmpCount / TO % Norm until PoP work.
7. Update `MIGRATION_SUMMARY.md` progress table as you close TODOs.
