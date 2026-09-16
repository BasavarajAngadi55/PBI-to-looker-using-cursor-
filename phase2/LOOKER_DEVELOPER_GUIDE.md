# Looker Developer Guide — Power BI → LookML (Phase 2)

**Source PBIX:** `movie_rental_analysis.pbix`  
**LookML model:** `lookml/models/movie_rental_analysis.model.lkml`  
**Primary explore (fact):** `film`  
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

**What it means:** One business table becomes one LookML view file pointed at a warehouse table.

**How to build (step-by-step):**

1. Create file views/<snake_case_table>.view.lkml.
2. Declare view: <name> with label matching the Power BI table business name.
3. Set sql_table_name to the real warehouse table (replace YOUR_PROJECT.YOUR_DATASET).
4. Add dimensions for all columns that analysts need.
5. Put primary_key: yes on the unique key dimension (first field).

**What to check:**

- [ ] View compiles in Looker Validator with 0 errors.
- [ ] sql_table_name resolves on the connection (table exists).
- [ ] Exactly one primary_key: yes in the view.
- [ ] Row count in Explore (count) is plausible vs Power BI table rows.

**Suggestions / best practice:**

- Prefer clear warehouse names (restaurants, not Sheet1) while keeping friendly labels.
- Do not model LocalDateTable_* / DateTableTemplate_* as views.
- Hide technical surrogate keys with hidden: yes if users should not see them.

**Example:**

```lookml
view: sheet1 {
  sql_table_name: `proj.dataset.sheet1` ;;
  dimension: restaurant_id {
    primary_key: yes
    type: number
    sql: ${TABLE}.RestaurantID ;;
  }
}
```

Docs: https://cloud.google.com/looker/docs/reference/param-view-view · https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-view/SKILL.md

### 4.2 Column → **dimension (or dimension_group for dates)**

**What it means:** Physical columns become dimensions; dates become dimension_group timeframes.

**How to build (step-by-step):**

1. Map each inventory column to a snake_case LookML field name.
2. Choose type: string, number, yesno, or time (dimension_group).
3. For dates, use dimension_group: <name> { type: time timeframes: [...] sql: ... ;; }.
4. Copy business meaning into label: and description:.
5. Preserve format intent (currency, percent) via value_format_name when useful.

**What to check:**

- [ ] Field appears in Explore field picker with correct label.
- [ ] Filtering/grouping on the field returns values matching Power BI.
- [ ] Date fields support month/quarter/year without extra DAX date tables.

**Suggestions / best practice:**

- Never expose auto-date table columns; use business dates + timeframes.
- Use group_label to cluster related fields (IDs, geography, flags).
- If column names have spaces, quote in SQL: ${TABLE}.`Country name`.

**Example:**

```lookml
dimension_group: order {
  type: time
  timeframes: [raw, date, week, month, quarter, year]
  sql: ${TABLE}.OrderDate ;;
  datatype: date
}
```

Docs: https://cloud.google.com/looker/docs/reference/param-field-dimension · https://cloud.google.com/looker/docs/reference/param-field-dimension-group

### 4.3 Measure (DAX) → **measure**

**What it means:** DAX measures become LookML measures using sum/average/count_distinct patterns; measure-of-measures use type: number + ${measure}; ratios use NULLIF; dependent measures are listed in MEASURE_DEPENDENCIES.md.

**How to build (step-by-step):**

1. Classify each DAX expression (simple aggregate vs measure-math vs CALCULATE vs time intelligence).
2. Implement simple aggregates with type: sum / average / count_distinct and ${dimension} sql.
3. Implement ratios with 1.0 * ${num} / NULLIF(${den}, 0) and value_format_name (official Looker division pattern).
4. For CALCULATE with simple equality/ISBLANK filters, use filters: { field: "value" } on a base aggregate.
5. For DATESYTD/DATEADD/SUMX/etc., leave TODO and implement with Looker period analysis or warehouse metrics.
6. When a measure references other measures, emit type: number, list DEPENDS ON, and order fields so bases come first.
7. Keep original DAX in description: until KPI parity is signed off.

**What to check:**

- [ ] Measure returns non-null for a known filter set.
- [ ] Side-by-side vs Power BI for at least 3 filter combinations.
- [ ] No fan-out inflation after joins (compare count vs count_distinct on PK).
- [ ] Dependent measures compile only after their bases exist (Looker validator).

**Suggestions / best practice:**

- Prefer ${dimension} references inside aggregate measure sql (looker-skills).
- Never put filters: on type: number — filter the composing aggregates instead.
- Do not claim parity for COMPLEX DAX without tests.
- If PBIX has 0 measures, still add explicit KPIs users expect (counts, averages).
- Open MEASURE_DEPENDENCIES.md for this PBIX before editing KPI fields.

**Example:**

```lookml
measure: total_sales {
  type: sum
  sql: ${sales_amount} ;;
  value_format_name: usd_0
}
measure: avg_rating {
  type: average
  sql: ${rating} ;;
}
measure: seps_yoy_var {
  type: number
  description: "DEPENDS ON: Seps, Seps SPLY"
  sql: ${seps} - ${seps_sply} ;;
}
measure: to_percent {
  type: number
  sql: 1.0 * ${seps} / NULLIF(${actives}, 0) ;;
  value_format_name: percent_2
}
```

Docs: https://cloud.google.com/looker/docs/reference/param-field-measure · https://cloud.google.com/looker/docs/reference/param-measure-types · https://cloud.google.com/looker/docs/reference/param-field-filters · https://cloud.google.com/looker/docs/best-practices/how-to-troubleshoot-fields-with-division-displaying-0 · https://cloud.google.com/looker/docs/reference/field-reference · https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-modeling-guidelines/SKILL.md

### 4.4 Relationship (M:1 From->To) → **explore join (relationship: many_to_one)**

**What it means:** Power BI relationships become Explore joins with explicit relationship and sql_on.

**How to build (step-by-step):**

1. Choose the fact table as the explore base (usually the many side).
2. For each active M:1 relationship, add a join to the one-side view.
3. Set type: left_outer (typical) and relationship: many_to_one.
4. Write sql_on using ${view.field} syntax on both sides.
5. If the same dim joins twice, use from: + a unique join name (alias).
6. For joins off an intermediate dim, add required_joins: [intermediate_view].

**What to check:**

- [ ] Join keys match Phase 1 inventory from/to columns exactly.
- [ ] Exploring fact+dim does not multiply fact rows unexpectedly.
- [ ] Inactive Power BI relationships are not used as the default path.

**Suggestions / best practice:**

- M:M is a HIGH risk gap — prefer a warehouse bridge table.
- Looker has no inactive join flag; keep inactive paths aliased and hidden until needed.
- Always declare relationship: (looker-skills requirement).

**Example:**

```lookml
explore: sheet1 {
  join: sheet2 {
    type: left_outer
    relationship: many_to_one
    sql_on: ${sheet1.country_code} = ${sheet2.country_id} ;;
  }
}
```

Docs: https://cloud.google.com/looker/docs/reference/param-explore-join · https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-explore/SKILL.md

### 4.5 Calculated column (DAX) → **dimension (prefer warehouse column)**

**What it means:** Row-level DAX calculated columns should be materialized in the warehouse, then exposed as dimensions.

**How to build (step-by-step):**

1. List every business calculated column from Phase 1 (02_dax_objects.json).
2. Recreate the expression in warehouse SQL (CASE/TRIM/date logic).
3. Add the physical column to the warehouse table.
4. Expose it in the view as a dimension with description noting original DAX.
5. Only use LookML-only sql: for trivial expressions you accept maintaining in Looker.

**What to check:**

- [ ] Warehouse column exists and is populated for sample keys.
- [ ] Dimension values match Power BI calculated column for sample rows.

**Suggestions / best practice:**

- Warehouse-first keeps LookML thin and testable.
- Financial month / rating buckets / TRIM fields are typical warehouse CASE statements.
- Do not leave DAX in production LookML descriptions without an owner.

**Example:**

```lookml
dimension: cuisiness {
  description: "PBI calc: TRIM(Sheet1[Cuisines]) — prefer warehouse"
  type: string
  sql: ${TABLE}.cuisiness ;;
}
```

Docs: https://cloud.google.com/looker/docs/lookml-terms-and-concepts

### 4.6 Calculated table → **view (sql_table_name or derived_table)**

**What it means:** DAX calculated tables become warehouse tables (preferred) or LookML derived tables.

**How to build (step-by-step):**

1. Identify calculated tables in inventory (is_calculated_table).
2. Decide: materialize in warehouse vs SQL derived table in LookML.
3. Prefer warehouse for anything used in multiple explores or large grain.
4. Create the view with primary_key and needed dimensions.

**What to check:**

- [ ] Table grain and keys documented.
- [ ] Joins to the calculated table match Power BI relationships.

**Suggestions / best practice:**

- Avoid embedding heavy DAX table logic only inside LookML.
- Document why the calculated table exists (seed, bridge, snapshot).

**Example:**

```lookml
view: adjustment_factor_pct {
  sql_table_name: `proj.dataset.adjustment_factor_pct` ;;
  dimension: adjustment_factor_pct {
    primary_key: yes
    type: number
    sql: ${TABLE}.`Adjustment factor (%)` ;;
  }
}
```

Docs: https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-view/SKILL.md

### 4.7 Power Query M → **Warehouse table/view + straight LookML view (preferred); SDT only as temporary bridge**

**What it means:** Each M query gets a deterministic recommendation: warehouse straight view, warehouse transform, warehouse seed, or temporary LookML SQL derived table.

**How to build (step-by-step):**

1. Open lookml/m_migration/M_QUERY_RECOMMENDATIONS.md for this PBIX.
2. For each query, follow the recommended pattern (usually warehouse table + straight view).
3. Implement the matching sql/<query>.sql stub in your warehouse/dbt project.
4. Apply lookml_stubs/<query>_recommended.lkml guidance; update views/<query>.view.lkml sql_table_name.
5. Use SDT only when the recommendation explicitly allows a temporary bridge.
6. Do not re-implement File.Contents / Excel paths inside Looker.

**What to check:**

- [ ] Every M query has a recommendation row and SQL stub in the ZIP
- [ ] Warehouse row counts match Power BI for sample queries
- [ ] Generated views resolve after sql_table_name is updated
- [ ] No heavy merge/append logic left only in LookML

**Suggestions / best practice:**

- Best practice order: warehouse table/view > temporary SDT > avoid NDT as M replacement.
- File CSV M queries → load to warehouse, then straight view.
- SQL-in-M → warehouse view with that SELECT, or temporary SDT.
- Merge/append/heavy M → dbt/Dataform model, never LookML-only.
- Embedded #table → warehouse seed (+ tiny SDT only if temporary).

**Example:**

```lookml
-- warehouse
CREATE OR REPLACE TABLE `proj.dataset.actor` AS SELECT ...;

# LookML straight view
view: actor {
  sql_table_name: `proj.dataset.actor` ;;
}
```

Docs: https://cloud.google.com/looker/docs/lookml-terms-and-concepts · https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-view/SKILL.md

### 4.8 Hierarchy → **drill_fields / sets / dimension_group timeframes**

**What it means:** Hierarchies become drill paths or timeframes — not separate LookML hierarchy objects.

**How to build (step-by-step):**

1. For date hierarchies, rely on dimension_group timeframes (year > quarter > month > date).
2. For attribute hierarchies, add drill_fields: [level1, level2, level3] on the top field.
3. Optionally create a set: for curated field lists.

**What to check:**

- [ ] Users can drill year to month to date in Explores.
- [ ] No dependency on LocalDateTable_* hierarchies.

**Suggestions / best practice:**

- Skip migrating auto-date hierarchies from internal tables.
- Use drill_fields on measures for guided analysis paths.

**Example:**

```lookml
dimension: country {
  type: string
  sql: ${TABLE}.Country ;;
  drill_fields: [city, locality, restaurant_name]
}
```

Docs: https://cloud.google.com/looker/docs/reference/param-field-drill-fields

### 4.9 RLS / OLS → **access_grant / access_filter / required_access_grants**

**What it means:** Power BI row/object security maps to Looker access filters and grants — not automatic.

**How to build (step-by-step):**

1. Read Phase 1 RLS inventory (empty list means none found).
2. Define Looker user attributes (e.g. country, org_id).
3. Add access_filter on the explore or required_access_grants on sensitive fields.
4. Test with users in and out of each role.

**What to check:**

- [ ] Unauthorized users cannot see restricted rows/fields.
- [ ] Authorized users still see full expected grain.

**Suggestions / best practice:**

- Even if RLS is empty, confirm with security owners before production.
- Prefer access_filter for row security; access_grant for field-level.

**Example:**

```lookml
explore: sheet1 {
  access_filter: {
    field: sheet2.country_name
    user_attribute: allowed_country
  }
}
```

Docs: https://github.com/looker-open-source/looker-skills/blob/main/skills/lookml-access-grants/SKILL.md

### 4.10 LocalDateTable_* / DateTableTemplate_* → **Skip (use business date + dimension_group)**

**What it means:** Internal auto-date tables are Power BI implementation detail — do not migrate.

**How to build (step-by-step):**

1. Identify internal tables in inventory and exclude them from LookML views.
2. Find the real business date column on fact/dim tables.
3. Model that column as dimension_group.

**What to check:**

- [ ] No LocalDateTable_* views in the LookML project.
- [ ] Time-based analysis works via business dates.

**Suggestions / best practice:**

- Mark this as an intentional skip in gap docs (severity LOW).

**Example:**

```lookml
# SKIP creating view: local_date_table_...
# USE dimension_group on FactTable.ServiceDate instead
```

Docs: https://cloud.google.com/looker/docs/reference/param-field-dimension-group

### 4.11 Model / Dataset → **model (.model.lkml) + connection**

**What it means:** The Power BI dataset becomes a LookML model file with connection, includes, explores.

**How to build (step-by-step):**

1. Open models/<pbix_stem>.model.lkml from LOOKML_PROJECT.zip.
2. Set connection: to the Looker Admin connection name.
3. Keep include: lines for each view (granular includes preferred).
4. Confirm the primary explore points at the fact view.
5. Configure datagroup / persist_with when ETL cadence is known.

**What to check:**

- [ ] Model appears in Looker and Explore loads.
- [ ] Includes resolve; no missing view errors.

**Suggestions / best practice:**

- Hide dimension-only QA explores from end users (hidden: yes).
- One focused explore beats a mega-explore when possible.

**Example:**

```lookml
connection: "warehouse_bq"
include: "/views/sheet1.view.lkml"
include: "/views/sheet2.view.lkml"
explore: sheet1 {
  label: "Restaurants"
  description: "Migrated from Power BI Zomato model."
}
```

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
Primary explore fact: **`film`**.

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

See **[`MEASURE_DEPENDENCIES.md`](MEASURE_DEPENDENCIES.md)** for measures that depend on other measures (implement bases first; Looker `type: number` + `${measure}`).

| Power BI measure | Strategy / status | Depends on |
|---|---|---|
| `payment.Revenue` | direct_sum / mapped | — |
| `inventory.Total Films Rented` | complex_todo / todo | — |
| `inventory.Average Inventory Value` | direct_average / mapped | — |
| `inventory.Inventory Turnover Rate` | measure_ratio / mapped | Total Films Rented, Average Inventory Value |
| `actor.FilmPopularity` | complex_todo / todo | — |

### Step E — Calculated columns (warehouse)

| Table | Column | DAX (truncated) | Action |
|---|---|---|---|
| `customer` | `Employment Duration` | `DATEDIFF('customer'[create_date], TODAY(), YEAR)` | Materialize; expose as dimension |

### Step F — Power Query M (recommended Looker / warehouse equivalent)

Decision order (best practice):

1. **Warehouse table/view + straight LookML view** (`sql_table_name`) — preferred
2. **LookML SQL derived table (SDT)** — temporary bridge for light SQL only
3. **Native derived table (NDT)** — rarely a Power Query replacement
4. Never encode heavy M merges/appends only in LookML

Stubs are inside the ZIP: `lookml/m_migration/` (`M_QUERY_RECOMMENDATIONS.md`, `sql/*.sql`, `lookml_stubs/*.lkml`).

| M query | Recommended pattern | Looker object | Build in |
|---|---|---|---|
| `actor` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `address` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `city` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `country` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `category` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `film` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `film_actor` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `film_category` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `film_text` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `inventory` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `language` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `payment` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `rentat` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `staff` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `store` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |
| `customer` | `warehouse_table_plus_straight_view` | straight view (sql_table_name) over warehouse table | `warehouse` |

#### `actor`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.actor` with casts matching M Changed Type.
3. Point generated LookML views/actor.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/actor.sql`
- LookML stub: `m_migration/lookml_stubs/actor_recommended.lkml`

#### `address`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.address` with casts matching M Changed Type.
3. Point generated LookML views/address.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/address.sql`
- LookML stub: `m_migration/lookml_stubs/address_recommended.lkml`

#### `city`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.city` with casts matching M Changed Type.
3. Point generated LookML views/city.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/city.sql`
- LookML stub: `m_migration/lookml_stubs/city_recommended.lkml`

#### `country`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.country` with casts matching M Changed Type.
3. Point generated LookML views/country.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/country.sql`
- LookML stub: `m_migration/lookml_stubs/country_recommended.lkml`

#### `category`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.category` with casts matching M Changed Type.
3. Point generated LookML views/category.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/category.sql`
- LookML stub: `m_migration/lookml_stubs/category_recommended.lkml`

#### `film`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.film` with casts matching M Changed Type.
3. Point generated LookML views/film.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/film.sql`
- LookML stub: `m_migration/lookml_stubs/film_recommended.lkml`

#### `film_actor`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.film_actor` with casts matching M Changed Type.
3. Point generated LookML views/film_actor.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/film_actor.sql`
- LookML stub: `m_migration/lookml_stubs/film_actor_recommended.lkml`

#### `film_category`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.film_category` with casts matching M Changed Type.
3. Point generated LookML views/film_category.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/film_category.sql`
- LookML stub: `m_migration/lookml_stubs/film_category_recommended.lkml`

#### `film_text`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.film_text` with casts matching M Changed Type.
3. Point generated LookML views/film_text.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/film_text.sql`
- LookML stub: `m_migration/lookml_stubs/film_text_recommended.lkml`

#### `inventory`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.inventory` with casts matching M Changed Type.
3. Point generated LookML views/inventory.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/inventory.sql`
- LookML stub: `m_migration/lookml_stubs/inventory_recommended.lkml`

#### `language`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.language` with casts matching M Changed Type.
3. Point generated LookML views/language.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/language.sql`
- LookML stub: `m_migration/lookml_stubs/language_recommended.lkml`

#### `payment`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.payment` with casts matching M Changed Type.
3. Point generated LookML views/payment.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/payment.sql`
- LookML stub: `m_migration/lookml_stubs/payment_recommended.lkml`

#### `rentat`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.rentat` with casts matching M Changed Type.
3. Point generated LookML views/rentat.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/rentat.sql`
- LookML stub: `m_migration/lookml_stubs/rentat_recommended.lkml`

#### `staff`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.staff` with casts matching M Changed Type.
3. Point generated LookML views/staff.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/staff.sql`
- LookML stub: `m_migration/lookml_stubs/staff_recommended.lkml`

#### `store`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.store` with casts matching M Changed Type.
3. Point generated LookML views/store.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/store.sql`
- LookML stub: `m_migration/lookml_stubs/store_recommended.lkml`

#### `customer`

**Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.customer` with casts matching M Changed Type.
3. Point generated LookML views/customer.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

- SQL stub: `m_migration/sql/customer.sql`
- LookML stub: `m_migration/lookml_stubs/customer_recommended.lkml`


## 6. Gaps (must resolve)

### Severity: HIGH

**[HIGH] Connection & warehouse**
- Gap: LookML still uses placeholders YOUR_LOOKER_CONNECTION and YOUR_PROJECT.YOUR_DATASET.
- Action: Set the real Looker connection name and point every sql_table_name at existing warehouse tables before validating.

**[HIGH] Power Query / ETL**
- Gap: 16 Power Query queries need warehouse/Looker equivalents. Pattern mix: {'warehouse_table_plus_straight_view': 16}.
- Action: Open LOOKML_PROJECT.zip → lookml/m_migration/. For each query follow M_QUERY_RECOMMENDATIONS.md, implement sql/<query>.sql in the warehouse, then update the straight LookML view sql_table_name. Use LookML SDT only when the recommendation allows a temporary bridge.

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
