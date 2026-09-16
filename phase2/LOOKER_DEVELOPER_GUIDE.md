# Looker Developer Guide — Power BI → LookML (Phase 2)

**Source PBIX:** `Human Resources Sample PBIX.pbix`  
**LookML model:** `lookml/models/human_resources_sample_pbix.model.lkml`  
**Primary explore (fact):** `FactTable`  
**Audience:** Looker developers implementing and validating this migration.

This is a **build playbook**: full instructions, checks, suggestions, examples, and gaps.

References: [LookML concepts](https://cloud.google.com/looker/docs/lookml-terms-and-concepts) · [looker-skills](https://github.com/looker-open-source/looker-skills)

---

## 1. How to use this guide

1. Read **Best practices** (mandatory).
2. Complete **Prerequisites**.
3. Study **Object equivalence** — each object has What / Build / Check / Suggestions / Example.
4. Execute **Build plan** for THIS PBIX.
5. Close **Gaps** (HIGH first).
6. Sign off with **Validation & acceptance**.

## 2. Best practices (mandatory)

| Rule | Why |
|---|---|
| Every view has `primary_key: yes` | Symmetric aggregates; prevents fan-out |
| Always set join `relationship:` | Correct SQL / aggregate behavior |
| Prefer `${dimension}` in measure sql | Single source of truth |
| Granular `include:` paths | Faster compile, fewer collisions |
| Explore `label` + `description` | Discoverability |
| Rebuild Power Query in warehouse | LookML is semantic, not ETL |
| No KPI claims without side-by-side tests | Complex DAX is not auto-translated |
| Review inactive / M:M joins | Avoid silent wrong numbers |

## 3. Prerequisites checklist

- [ ] Looker project + Git branch ready
- [ ] Database connection created in Looker Admin
- [ ] Warehouse tables exist (or tickets filed)
- [ ] Phase 1 inventory matches this PBIX
- [ ] `LOOKML_PROJECT.zip` imported
- [ ] SQL dialect known (BigQuery vs Snowflake)

## 4. Object equivalence — full developer instructions

For each Power BI object: follow **How to build**, verify **What to check**, apply **Suggestions**.

### 4.1 Table (business) → **view (.view.lkml)**

**What it means:** Create views/<name>.view.lkml with `view: <name> { sql_table_name: ... }`. Every view needs a primary_key dimension (Looker skills / symmetric aggregates).

**How to build (step-by-step):**

1. Create views/<name>.view.lkml with `view: <name> { sql_table_name: ... }`. Every view needs a primary_key dimension (Looker skills / symmetric aggregates).

**What to check:**

- [ ] Present in Phase 1 inventory
- [ ] LookML validator clean
- [ ] Explore sample matches expected grain

**Suggestions / best practice:**

Docs: https://cloud.google.com/looker/docs/reference/param-view-view · https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-view/SKILL.md

### 4.2 Column → **dimension (or dimension_group for dates)**

**What it means:** Add `dimension: field { type: ... sql: ${TABLE}.col ;; }`. Date/time columns → `dimension_group: ... { type: time timeframes: [raw, date, week, month, quarter, year] }`.

**How to build (step-by-step):**

1. Add `dimension: field { type: ... sql: ${TABLE}.col ;; }`. Date/time columns → `dimension_group: ... { type: time timeframes: [raw, date, week, month, quarter, year] }`.

**What to check:**

- [ ] Present in Phase 1 inventory
- [ ] LookML validator clean
- [ ] Explore sample matches expected grain

**Suggestions / best practice:**

Docs: https://cloud.google.com/looker/docs/reference/param-field-dimension · https://cloud.google.com/looker/docs/reference/param-field-dimension-group

### 4.3 Measure (DAX) → **measure**

**What it means:** Map SUM/AVERAGE/COUNT/DISTINCTCOUNT to type: sum|average|count|count_distinct. Ratios → type: number + SAFE_DIVIDE. CALCULATE/time-intel → filters, period patterns, or warehouse + TODO.

**How to build (step-by-step):**

1. Map SUM/AVERAGE/COUNT/DISTINCTCOUNT to type: sum|average|count|count_distinct. Ratios → type: number + SAFE_DIVIDE. CALCULATE/time-intel → filters, period patterns, or warehouse + TODO.

**What to check:**

- [ ] Present in Phase 1 inventory
- [ ] LookML validator clean
- [ ] Explore sample matches expected grain

**Suggestions / best practice:**

Docs: https://cloud.google.com/looker/docs/reference/param-field-measure · https://cloud.google.com/looker/docs/reference/field-reference

### 4.4 Relationship (M:1 From→To) → **explore join (relationship: many_to_one)**

**What it means:** In the model file, `explore: fact { join: dim { type: left_outer relationship: many_to_one sql_on: ${fact.fk} = ${dim.pk} ;; } }`. Always set relationship explicitly (looker-skills).

**How to build (step-by-step):**

1. In the model file, `explore: fact { join: dim { type: left_outer relationship: many_to_one sql_on: ${fact.fk} = ${dim.pk} ;; } }`. Always set relationship explicitly (looker-skills).

**What to check:**

- [ ] Present in Phase 1 inventory
- [ ] LookML validator clean
- [ ] Explore sample matches expected grain

**Suggestions / best practice:**

Docs: https://cloud.google.com/looker/docs/reference/param-explore-join · https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-explore/SKILL.md

### 4.5 Calculated column (DAX) → **dimension (prefer warehouse column)**

**What it means:** Prefer materializing in warehouse SQL, then expose as dimension. Simple row expressions may use LookML sql:; complex DAX stays as migration TODO.

**How to build (step-by-step):**

1. Prefer materializing in warehouse SQL, then expose as dimension. Simple row expressions may use LookML sql:; complex DAX stays as migration TODO.

**What to check:**

- [ ] Present in Phase 1 inventory
- [ ] LookML validator clean
- [ ] Explore sample matches expected grain

**Suggestions / best practice:**

Docs: https://cloud.google.com/looker/docs/lookml-terms-and-concepts

### 4.6 Calculated table → **view (sql_table_name or derived_table)**

**What it means:** If the table is seeded/small, warehouse seed + standard view. Otherwise SQL derived table / NDT per lookml-view derived_table guidance.

**How to build (step-by-step):**

1. If the table is seeded/small, warehouse seed + standard view. Otherwise SQL derived table / NDT per lookml-view derived_table guidance.

**What to check:**

- [ ] Present in Phase 1 inventory
- [ ] LookML validator clean
- [ ] Explore sample matches expected grain

**Suggestions / best practice:**

Docs: https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-view/SKILL.md

### 4.7 Power Query M → **Warehouse / ETL (not LookML)**

**What it means:** Rebuild M transforms in the warehouse (dbt/Dataform/SQL). LookML only points sql_table_name at the finished table.

**How to build (step-by-step):**

1. Rebuild M transforms in the warehouse (dbt/Dataform/SQL). LookML only points sql_table_name at the finished table.

**What to check:**

- [ ] Present in Phase 1 inventory
- [ ] LookML validator clean
- [ ] Explore sample matches expected grain

**Suggestions / best practice:**

Docs: https://cloud.google.com/looker/docs/lookml-terms-and-concepts

### 4.8 Hierarchy → **drill_fields / sets / dimension_group timeframes**

**What it means:** Date hierarchies → dimension_group timeframes. Attribute hierarchies → drill_fields: [year, quarter, month, day] or sets.

**How to build (step-by-step):**

1. Date hierarchies → dimension_group timeframes. Attribute hierarchies → drill_fields: [year, quarter, month, day] or sets.

**What to check:**

- [ ] Present in Phase 1 inventory
- [ ] LookML validator clean
- [ ] Explore sample matches expected grain

**Suggestions / best practice:**

Docs: https://cloud.google.com/looker/docs/reference/param-field-drill-fields

### 4.9 RLS / OLS → **access_grant / access_filter / required_access_grants**

**What it means:** Map roles to Looker user attributes + access_filter on explores, or access_grant on fields.

**How to build (step-by-step):**

1. Map roles to Looker user attributes + access_filter on explores, or access_grant on fields.

**What to check:**

- [ ] Present in Phase 1 inventory
- [ ] LookML validator clean
- [ ] Explore sample matches expected grain

**Suggestions / best practice:**

Docs: https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-access-grants/SKILL.md

### 4.10 LocalDateTable_* / DateTableTemplate_* → **Skip (use business date + dimension_group)**

**What it means:** Do not migrate auto-date tables. Use the business date column with Looker timeframes.

**How to build (step-by-step):**

1. Do not migrate auto-date tables. Use the business date column with Looker timeframes.

**What to check:**

- [ ] Present in Phase 1 inventory
- [ ] LookML validator clean
- [ ] Explore sample matches expected grain

**Suggestions / best practice:**

Docs: https://cloud.google.com/looker/docs/reference/param-field-dimension-group

### 4.11 Model / Dataset → **model (.model.lkml) + connection**

**What it means:** One model file: connection, includes, datagroup, explore(s). Prefer granular includes over wildcards (lookml-modeling-guidelines).

**How to build (step-by-step):**

1. One model file: connection, includes, datagroup, explore(s). Prefer granular includes over wildcards (lookml-modeling-guidelines).

**What to check:**

- [ ] Present in Phase 1 inventory
- [ ] LookML validator clean
- [ ] Explore sample matches expected grain

**Suggestions / best practice:**

Docs: https://cloud.google.com/looker/docs/lookml-terms-and-concepts · https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-modeling-guidelines/SKILL.md

## 5. Build plan (this PBIX)

### Step A — Import LookML
1. Unzip `LOOKML_PROJECT.zip`.
2. Place `manifest.lkml`, `models/`, `views/` in the Looker project.
3. Set `connection:` in the model file.

### Step B — Point views at warehouse

| PBI table | LookML view | File | Cols | PK guess | Date cols |
|---|---|---|---|---|---|
| `AgeGroup` | `agegroup` | `views/agegroup.view.lkml` | 2 | `AgeGroupID` | - |
| `BU` | `bu` | `views/bu.view.lkml` | 4 | `BU` | - |
| `Date` | `date` | `views/date.view.lkml` | 12 | `Date` | Date, MonthStartDate, MonthEndDate |
| `Employee` | `employee` | `views/employee.view.lkml` | 16 | `EmplID` | date, TermDate, HireDate |
| `Ethnicity` | `ethnicity` | `views/ethnicity.view.lkml` | 2 | `Ethnic Group` | - |
| `FP` | `fp` | `views/fp.view.lkml` | 2 | `FP` | - |
| `Gender` | `gender` | `views/gender.view.lkml` | 3 | `ID` | - |
| `PayType` | `paytype` | `views/paytype.view.lkml` | 2 | `PayTypeID` | - |
| `SeparationReason` | `separationreason` | `views/separationreason.view.lkml` | 2 | `SeparationTypeID` | - |

### Step C — Explores and joins
Primary explore fact: **`FactTable`**.

| From (FK) | To (PK) | Card | Active | Looker action |
|---|---|---|---|---|
| `Employee[date]` | `Date[Date]` | M:1 | True | join date relationship from PBI M:1 |
| `Employee[FP]` | `FP[FP]` | M:1 | True | join fp relationship from PBI M:1 |
| `Employee[EthnicGroup]` | `Ethnicity[Ethnic Group]` | M:1 | True | join ethnicity relationship from PBI M:1 |
| `Employee[Gender]` | `Gender[ID]` | M:1 | True | join gender relationship from PBI M:1 |
| `Employee[PayTypeID]` | `PayType[PayTypeID]` | M:1 | True | join paytype relationship from PBI M:1 |
| `Employee[BU]` | `BU[BU]` | M:1 | True | join bu relationship from PBI M:1 |
| `Employee[AgeGroupID]` | `AgeGroup[AgeGroupID]` | M:1 | True | join agegroup relationship from PBI M:1 |
| `Employee[TermReason]` | `SeparationReason[SeparationTypeID]` | M:1 | True | join separationreason relationship from PBI M:1 |

### Step D — Measures

Mapped 30 measures; **21 TODO**.

| Power BI measure | Strategy / status |
|---|---|
| `Employee.EmpCount` | complex_todo / todo |
| `Employee.Seps` | complex_todo / todo |
| `Employee.Actives` | complex_todo / todo |
| `Employee.New Hires` | complex_todo / todo |
| `Employee.AVG Tenure Days` | complex_todo / todo |
| `Employee.AVG Tenure Months` | complex_todo / todo |
| `Employee.AVG Age` | complex_todo / todo |
| `Employee.Sum of BadHires` | complex_todo / todo |
| `Employee.New Hires SPLY` | complex_todo / todo |
| `Employee.Actives SPLY` | complex_todo / todo |
| `Employee.Seps SPLY` | complex_todo / todo |
| `Employee.EmpCount SPLY` | complex_todo / todo |
| `Employee.Seps YoY Var` | complex_todo / todo |
| `Employee.Actives YoY Var` | complex_todo / todo |
| `Employee.New Hires YoY Var` | complex_todo / todo |
| `Employee.Seps YoY % Change` | ratio / mapped |
| `Employee.Actives YoY % Change` | ratio / mapped |
| `Employee.New Hires YoY % Change` | ratio / mapped |
| `Employee.Bad Hires SPLY` | complex_todo / todo |
| `Employee.Bad Hires YoY Var` | complex_todo / todo |
| `Employee.Bad Hires YoY % Change` | ratio / mapped |
| `Employee.TO %` | ratio / mapped |
| `Employee.TO % Norm` | complex_todo / todo |
| `Employee.TO % Var` | complex_todo / todo |
| `Employee.Sep%ofActive` | ratio / mapped |
| `Employee.Sep%ofSMLYActives` | ratio / mapped |
| `Employee.BadHire%ofActives` | ratio / mapped |
| `Employee.BadHire%ofActiveSPLY` | ratio / mapped |
| `BU.Count of BU` | complex_todo / todo |
| `Date.Count of Date` | complex_todo / todo |

### Step E — Calculated columns (warehouse)

| Table | Column | DAX (truncated) | Action |
|---|---|---|---|
| `BU` | `Region` | `mid([RegionSeq], 3,15)` | Materialize; expose as dimension |
| `Date` | `MonthIncrementNumber` | `([Year]-MIN([Year]))*12 +[MonthNumber]` | Materialize; expose as dimension |
| `Employee` | `isNewHire` | `IF(YEAR([date]) = YEAR([HireDate]) && MONTH([date])=MONTH([HireDate]), 1)` | Materialize; expose as dimension |
| `Employee` | `AgeGroupID` | `IF([Age]<30, 1, IF([Age]<50, 2, 3))` | Materialize; expose as dimension |
| `Employee` | `TenureDays` | `IF([date]-[HireDate]<0,[HireDate]-[date],[date]-[HireDate])` | Materialize; expose as dimension |
| `Employee` | `TenureMonths` | `CEILING([TenureDays]/30, 1) -1` | Materialize; expose as dimension |
| `Employee` | `BadHires` | `IF(OR((([HireDate]-[TermDate])*-1)>=61,ISBLANK([TermDate])),0,1)` | Materialize; expose as dimension |

### Step F — Power Query M (recommended Looker / warehouse equivalent)

Decision order (best practice):

1. **Warehouse table/view + straight LookML view** (`sql_table_name`) — preferred
2. **LookML SQL derived table (SDT)** — temporary bridge for light SQL only
3. **Native derived table (NDT)** — rarely a Power Query replacement
4. Never encode heavy M merges/appends only in LookML

Stubs are inside the ZIP: `lookml/m_migration/` (`M_QUERY_RECOMMENDATIONS.md`, `sql/*.sql`, `lookml_stubs/*.lkml`).

| M query | Recommended pattern | Looker object | Build in |
|---|---|---|---|
| `BU` | `lookml_sql_derived_table` | warehouse view/table preferred; LookML SQL derived table acceptable if SELECT-only | `either` |
| `FP` | `lookml_sql_derived_table` | warehouse view/table preferred; LookML SQL derived table acceptable if SELECT-only | `either` |
| `PayType` | `lookml_sql_derived_table` | warehouse view/table preferred; LookML SQL derived table acceptable if SELECT-only | `either` |
| `SeparationReason` | `lookml_sql_derived_table` | warehouse view/table preferred; LookML SQL derived table acceptable if SELECT-only | `either` |
| `Date` | `lookml_sql_derived_table` | warehouse view/table preferred; LookML SQL derived table acceptable if SELECT-only | `either` |
| `Employee` | `warehouse_transform_model` | warehouse transform + straight view (avoid SDT for heavy M) | `warehouse` |
| `Ethnicity` | `warehouse_seed_plus_straight_view` | warehouse seed table + straight view (tiny SDT optional) | `warehouse` |
| `Gender` | `warehouse_seed_plus_straight_view` | warehouse seed table + straight view (tiny SDT optional) | `warehouse` |
| `AgeGroup` | `warehouse_seed_plus_straight_view` | warehouse seed table + straight view (tiny SDT optional) | `warehouse` |

#### `BU`

**Why:** M wraps a SQL statement. Prefer creating a warehouse view/table with that SQL, then a straight LookML view. A LookML sql-derived table is an acceptable temporary equivalent.

**Build steps:**

1. Prefer warehouse VIEW/TABLE with the M SQL (or source table).
2. Use straight LookML view with sql_table_name.
3. Use SDT only if warehouse object is not ready yet; migrate off SDT later.

- SQL stub: `m_migration/sql/bu.sql`
- LookML stub: `m_migration/lookml_stubs/bu_recommended.lkml`

#### `FP`

**Why:** M wraps a SQL statement. Prefer creating a warehouse view/table with that SQL, then a straight LookML view. A LookML sql-derived table is an acceptable temporary equivalent.

**Build steps:**

1. Prefer warehouse VIEW/TABLE with the M SQL (or source table).
2. Use straight LookML view with sql_table_name.
3. Use SDT only if warehouse object is not ready yet; migrate off SDT later.

- SQL stub: `m_migration/sql/fp.sql`
- LookML stub: `m_migration/lookml_stubs/fp_recommended.lkml`

#### `PayType`

**Why:** M wraps a SQL statement. Prefer creating a warehouse view/table with that SQL, then a straight LookML view. A LookML sql-derived table is an acceptable temporary equivalent.

**Build steps:**

1. Prefer warehouse VIEW/TABLE with the M SQL (or source table).
2. Use straight LookML view with sql_table_name.
3. Use SDT only if warehouse object is not ready yet; migrate off SDT later.

- SQL stub: `m_migration/sql/paytype.sql`
- LookML stub: `m_migration/lookml_stubs/paytype_recommended.lkml`

#### `SeparationReason`

**Why:** M wraps a SQL statement. Prefer creating a warehouse view/table with that SQL, then a straight LookML view. A LookML sql-derived table is an acceptable temporary equivalent.

**Build steps:**

1. Prefer warehouse VIEW/TABLE with the M SQL (or source table).
2. Use straight LookML view with sql_table_name.
3. Use SDT only if warehouse object is not ready yet; migrate off SDT later.

- SQL stub: `m_migration/sql/separationreason.sql`
- LookML stub: `m_migration/lookml_stubs/separationreason_recommended.lkml`

#### `Date`

**Why:** M wraps a SQL statement. Prefer creating a warehouse view/table with that SQL, then a straight LookML view. A LookML sql-derived table is an acceptable temporary equivalent.

**Build steps:**

1. Prefer warehouse VIEW/TABLE with the M SQL (or source table).
2. Use straight LookML view with sql_table_name.
3. Use SDT only if warehouse object is not ready yet; migrate off SDT later.

- SQL stub: `m_migration/sql/date.sql`
- LookML stub: `m_migration/lookml_stubs/date_recommended.lkml`

#### `Employee`

**Why:** M contains merge, append/union, or heavy transforms. Looker skills: keep LookML semantic; put ETL in the warehouse.

**Build steps:**

1. Read phase1/inventory/04_m_raw/Employee.m end-to-end.
2. Implement joins/unions/filters in dbt/Dataform/SQL.
3. Expose curated table to LookML views/employee.view.lkml via sql_table_name.
4. Mark any LookML SDT as temporary technical debt.

- SQL stub: `m_migration/sql/employee.sql`
- LookML stub: `m_migration/lookml_stubs/employee_recommended.lkml`

#### `Ethnicity`

**Why:** Embedded/static M tables should become warehouse seeds. Straight LookML view afterward; SDT only for tiny temporary seeds.

**Build steps:**

1. Extract static rows from M into a seed CSV or INSERT script.
2. Load seed to warehouse.
3. Use generated straight LookML view.

- SQL stub: `m_migration/sql/ethnicity.sql`
- LookML stub: `m_migration/lookml_stubs/ethnicity_recommended.lkml`

#### `Gender`

**Why:** Embedded/static M tables should become warehouse seeds. Straight LookML view afterward; SDT only for tiny temporary seeds.

**Build steps:**

1. Extract static rows from M into a seed CSV or INSERT script.
2. Load seed to warehouse.
3. Use generated straight LookML view.

- SQL stub: `m_migration/sql/gender.sql`
- LookML stub: `m_migration/lookml_stubs/gender_recommended.lkml`

#### `AgeGroup`

**Why:** Embedded/static M tables should become warehouse seeds. Straight LookML view afterward; SDT only for tiny temporary seeds.

**Build steps:**

1. Extract static rows from M into a seed CSV or INSERT script.
2. Load seed to warehouse.
3. Use generated straight LookML view.

- SQL stub: `m_migration/sql/agegroup.sql`
- LookML stub: `m_migration/lookml_stubs/agegroup_recommended.lkml`


## 6. Gaps (must resolve)

### Severity: HIGH

**[HIGH] Connection & warehouse**
- Gap: LookML still uses placeholders YOUR_LOOKER_CONNECTION and YOUR_PROJECT.YOUR_DATASET.
- Action: Set the real Looker connection name and point every sql_table_name at existing warehouse tables before validating.

**[HIGH] Power Query / ETL**
- Gap: 9 Power Query queries need warehouse/Looker equivalents. Pattern mix: {'lookml_sql_derived_table': 5, 'warehouse_transform_model': 1, 'warehouse_seed_plus_straight_view': 3}.
- Action: Open LOOKML_PROJECT.zip → lookml/m_migration/. For each query follow M_QUERY_RECOMMENDATIONS.md, implement sql/<query>.sql in the warehouse, then update the straight LookML view sql_table_name. Use LookML SDT only when the recommendation allows a temporary bridge.

**[HIGH] Complex DAX**
- Gap: 21 of 30 measures are TODO stubs (CALCULATE/time-intel/iterators).
- Action: Implement each TODO using LookML filters, period-over-period patterns, or warehouse logic. Keep original DAX in the field description until KPI parity passes.

**[HIGH] Calculated columns**
- Gap: 7 business calculated columns must be materialized (prefer warehouse), not left as DAX.
- Action: Create warehouse columns for: BU.Region; Date.MonthIncrementNumber; Employee.isNewHire; Employee.AgeGroupID; Employee.TenureDays; Employee.TenureMonths; Employee.BadHires

### Severity: MEDIUM

_None_

### Severity: LOW

**[LOW] Row-level security**
- Gap: No RLS roles in this PBIX inventory.
- Action: Still confirm with security owners whether Looker needs access_filter by region/org.

**[LOW] Auto date tables**
- Gap: 6 LocalDateTable_/DateTableTemplate_ tables skipped (correct).
- Action: Use business date columns with dimension_group timeframes. Do not migrate auto-date tables.

## 7. What to check (validation checklist)

### LookML / compile
- [ ] Validator: 0 errors
- [ ] One `primary_key: yes` per view
- [ ] Every join has `relationship:` + `sql_on:`
- [ ] Dialect-correct SQL

### Data grain
- [ ] Fact row count ≈ Power BI (same filters)
- [ ] No unexpected fan-out (count vs count_distinct on PK)
- [ ] Orphan FK rate understood for left_outer

### Business logic
- [ ] All HIGH gaps closed or signed off
- [ ] Calculated columns available
- [ ] Required measures implemented and spot-checked
- [ ] Inactive / M:M joins reviewed

### Security & ops
- [ ] RLS / access_filter decision recorded
- [ ] Caching / datagroup set
- [ ] QA explores hidden from end users

## 8. Acceptance criteria

1. Validator clean on target connection.
2. HIGH gaps closed or formally accepted.
3. At least 5 Power BI business questions reproduce in Looker within agreed tolerance.
4. Remaining MEDIUM/LOW gaps have owners and dates.

**KPI parity is NOT automatic.**

## 9. Inventory snapshot

- tables: **15**
- business_tables: **9**
- internal_tables: **6**
- columns: **87**
- measures: **30**
- calculated_columns: **43**
- calculated_tables: **6**
- relationships: **8**
- power_query: **9**
- m_files: **9**
- rls_roles: **0**
- hierarchies: **7**
- partitions: **122**
- auto_date_tables: **6**
- annotations: **158**
- sort_by_columns: **0**
- format_strings: **5**
- perspectives: **0**
- display_folders: **0**

## 10. Out of scope

- Power BI report pages, visuals, bookmarks, themes
- Automatic warehouse DDL generation
- Automatic KPI certification

---

_Generated by phase2/generate_developer_guide.py for `Human Resources Sample PBIX.pbix`._
