# Looker Developer Guide — Power BI → LookML (Phase 2)

**Source PBIX:** `movie_rental_analysis.pbix`  
**LookML model:** `lookml/models/movie_rental_analysis.model.lkml`  
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
| `actor` | `actor` | `views/actor.view.lkml` | 4 | `actor_id` | last_update |
| `address` | `address` | `views/address.view.lkml` | 9 | `address_id` | last_update |
| `category` | `category` | `views/category.view.lkml` | 3 | `category_id` | last_update |
| `city` | `city` | `views/city.view.lkml` | 4 | `city_id` | last_update |
| `country` | `country` | `views/country.view.lkml` | 3 | `country_id` | last_update |
| `customer` | `customer` | `views/customer.view.lkml` | 10 | `customer_id` | create_date, last_update |
| `film` | `film` | `views/film.view.lkml` | 13 | `film_id` | last_update |
| `film_actor` | `film_actor` | `views/film_actor.view.lkml` | 3 | `actor_id` | last_update |
| `film_category` | `film_category` | `views/film_category.view.lkml` | 3 | `film_id` | last_update |
| `film_text` | `film_text` | `views/film_text.view.lkml` | 3 | `film_id` | - |
| `inventory` | `inventory` | `views/inventory.view.lkml` | 4 | `inventory_id` | last_update |
| `language` | `language` | `views/language.view.lkml` | 3 | `language_id` | last_update |
| `payment` | `payment` | `views/payment.view.lkml` | 7 | `payment_id` | payment_date, last_update |
| `rentat` | `rentat` | `views/rentat.view.lkml` | 7 | `rental_id` | rental_date, return_date, last_update |
| `staff` | `staff` | `views/staff.view.lkml` | 11 | `staff_id` | last_update |
| `store` | `store` | `views/store.view.lkml` | 4 | `store_id` | last_update |

### Step C — Explores and joins
Primary explore fact: **`FactTable`**.

| From (FK) | To (PK) | Card | Active | Looker action |
|---|---|---|---|---|
| `film_actor[actor_id]` | `actor[actor_id]` | M:1 | True | join actor relationship from PBI M:1 |
| `address[city_id]` | `city[city_id]` | M:1 | True | join city relationship from PBI M:1 |
| `city[country_id]` | `country[country_id]` | M:1 | True | join country relationship from PBI M:1 |
| `film[language_id]` | `language[language_id]` | M:1 | True | join language relationship from PBI M:1 |
| `film_category[category_id]` | `category[category_id]` | M:1 | True | join category relationship from PBI M:1 |
| `film[film_id]` | `film_category[film_id]` | M:1 | True | join film_category relationship from PBI M:1 |
| `film[film_id]` | `film_text[film_id]` | M:1 | True | join film_text relationship from PBI M:1 |
| `store[store_id]` | `staff[store_id]` | M:1 | True | join staff relationship from PBI M:1 |
| `film_actor[film_id]` | `film[film_id]` | M:1 | True | join film relationship from PBI M:1 |
| `customer[address_id]` | `address[address_id]` | M:1 | True | join address relationship from PBI M:1 |
| `payment[customer_id]` | `customer[customer_id]` | M:1 | True | join customer relationship from PBI M:1 |
| `customer[store_id]` | `store[store_id]` | M:1 | True | join store relationship from PBI M:1 |
| `rentat[inventory_id]` | `inventory[inventory_id]` | M:1 | True | join inventory relationship from PBI M:1 |
| `rentat[rental_id]` | `payment[rental_id]` | M:1 | True | join payment relationship from PBI M:1 |
| `rentat[staff_id]` | `staff[staff_id]` | M:1 | False | join staff relationship from PBI M:1 |
| `inventory[film_id]` | `film[film_id]` | M:1 | True | join film relationship from PBI M:1 |

### Step D — Measures

Mapped 5 measures; **2 TODO**.

| Power BI measure | Strategy / status |
|---|---|
| `payment.Revenue` | direct_sum / mapped |
| `inventory.Total Films Rented` | complex_todo / todo |
| `inventory.Average Inventory Value` | direct_average / mapped |
| `inventory.Inventory Turnover Rate` | ratio / mapped |
| `actor.FilmPopularity` | complex_todo / todo |

### Step E — Calculated columns (warehouse)

| Table | Column | DAX (truncated) | Action |
|---|---|---|---|
| `customer` | `Employment Duration` | `DATEDIFF('customer'[create_date], TODAY(), YEAR)` | Materialize; expose as dimension |

### Step F — Power Query

- `actor` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `address` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `city` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `country` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `category` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `film` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `film_actor` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `film_category` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `film_text` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `inventory` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `language` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `payment` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `rentat` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `staff` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `store` — source_type=`file` → rebuild in warehouse, then point sql_table_name
- `customer` — source_type=`file` → rebuild in warehouse, then point sql_table_name

## 6. Gaps (must resolve)

### Severity: HIGH

**[HIGH] Connection & warehouse**
- Gap: LookML still uses placeholders YOUR_LOOKER_CONNECTION and YOUR_PROJECT.YOUR_DATASET.
- Action: Set the real Looker connection name and point every sql_table_name at existing warehouse tables before validating.

**[HIGH] Power Query / ETL**
- Gap: 16 Power Query queries exist in PBIX. LookML does not recreate M.
- Action: Rebuild each query's grain and transforms in the warehouse (dbt/Dataform/SQL). Confirm row counts and keys match Power BI before Looker go-live. Queries: actor, address, city, country, category, film, film_actor, film_category, film_text, inventory, language, payment, rentat, staff, store, customer

**[HIGH] Complex DAX**
- Gap: 2 of 5 measures are TODO stubs (CALCULATE/time-intel/iterators).
- Action: Implement each TODO using LookML filters, period-over-period patterns, or warehouse logic. Keep original DAX in the field description until KPI parity passes.

**[HIGH] Calculated columns**
- Gap: 1 business calculated columns must be materialized (prefer warehouse), not left as DAX.
- Action: Create warehouse columns for: customer.Employment Duration

### Severity: MEDIUM

**[MEDIUM] Inactive relationship**
- Gap: Inactive in Power BI: rentat[staff_id] -> staff[staff_id] (M:1).
- Action: Looker has no inactive join. Keep as a separate aliased join (from:) and only expose when a measure needs USERELATIONSHIP-style behavior. Hide fields until needed.

### Severity: LOW

**[LOW] Row-level security**
- Gap: No RLS roles in this PBIX inventory.
- Action: Still confirm with security owners whether Looker needs access_filter by region/org.

**[LOW] Auto date tables**
- Gap: 20 LocalDateTable_/DateTableTemplate_ tables skipped (correct).
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

- tables: **36**
- business_tables: **16**
- internal_tables: **20**
- columns: **231**
- measures: **5**
- calculated_columns: **121**
- calculated_tables: **20**
- relationships: **16**
- power_query: **16**
- m_files: **16**
- rls_roles: **0**
- hierarchies: **20**
- partitions: **322**
- auto_date_tables: **20**
- annotations: **433**
- sort_by_columns: **0**
- format_strings: **63**
- perspectives: **0**
- display_folders: **0**

## 10. Out of scope

- Power BI report pages, visuals, bookmarks, themes
- Automatic warehouse DDL generation
- Automatic KPI certification

---

_Generated by phase2/generate_developer_guide.py for `movie_rental_analysis.pbix`._
