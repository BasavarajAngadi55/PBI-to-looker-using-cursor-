# Power Query M → Looker / warehouse recommendations

**Source:** `Human Resources Sample PBIX.pbix`  
**Queries:** 9  
**Approach:** deterministic (no LLM)

## Best-practice decision order

- 1. Warehouse table/view (ETL/dbt) + straight LookML view (sql_table_name) — preferred
- 2. LookML SQL derived table (SDT) — temporary bridge for light SQL only
- 3. Native derived table (NDT) — rarely a Power Query replacement
- 4. Never put heavy M merges/appends only in LookML

## Pattern summary

| Pattern | Count |
|---|---|
| `lookml_sql_derived_table` | 5 |
| `warehouse_seed_plus_straight_view` | 3 |
| `warehouse_transform_model` | 1 |

## Per-query recommendations

### `BU`

- **Recommended pattern:** `lookml_sql_derived_table`
- **Looker object:** warehouse view/table preferred; LookML SQL derived table acceptable if SELECT-only
- **Build in:** `either` (confidence: high)
- **Why:** M wraps a SQL statement. Prefer creating a warehouse view/table with that SQL, then a straight LookML view. A LookML sql-derived table is an acceptable temporary equivalent.
- **Signals:** sql_source, column_casts:3

**Build steps:**

1. Prefer warehouse VIEW/TABLE with the M SQL (or source table).
2. Use straight LookML view with sql_table_name.
3. Use SDT only if warehouse object is not ready yet; migrate off SDT later.

**Checks:**

- [ ] SQL dialect matches Looker connection
- [ ] Results match Power BI query for a sample filter

**SQL stub:** `m_migration/sql/bu.sql`
**LookML stub:** `m_migration/lookml_stubs/bu_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Preferred: materialize as warehouse view/table
CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.bu` AS
select distinct market BU,#(lf)  REGIONTITLE Region,#(lf)  MARKETDIRECTOR VP#(lf)from hr.bu
;

-- Alternative (temporary): use the same SELECT inside a LookML derived_table (see lookml stub).
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Option A (best practice): straight view on warehouse object
view: bu {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.bu` ;;
}

# Option B (temporary SDT) — looker-skills: prefer NDT for Looker-native rollups;
# for migrated M SQL, SDT is OK only until warehouse view exists.
view: bu_sdt {
  derived_table: {
    sql:
      select distinct market BU,#(lf)  REGIONTITLE Region,#(lf)  MARKETDIRECTOR VP#(lf)from hr.bu
    ;;
  }
  # Declare dimensions for selected columns; set primary_key: yes
}
```

</details>

### `FP`

- **Recommended pattern:** `lookml_sql_derived_table`
- **Looker object:** warehouse view/table preferred; LookML SQL derived table acceptable if SELECT-only
- **Build in:** `either` (confidence: high)
- **Why:** M wraps a SQL statement. Prefer creating a warehouse view/table with that SQL, then a straight LookML view. A LookML sql-derived table is an acceptable temporary equivalent.
- **Signals:** sql_source, column_casts:2

**Build steps:**

1. Prefer warehouse VIEW/TABLE with the M SQL (or source table).
2. Use straight LookML view with sql_table_name.
3. Use SDT only if warehouse object is not ready yet; migrate off SDT later.

**Checks:**

- [ ] SQL dialect matches Looker connection
- [ ] Results match Power BI query for a sample filter

**SQL stub:** `m_migration/sql/fp.sql`
**LookML stub:** `m_migration/lookml_stubs/fp_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Preferred: materialize as warehouse view/table
CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.fp` AS
SELECT [HR].[FP].*   FROM [HR].[FP]
;

-- Alternative (temporary): use the same SELECT inside a LookML derived_table (see lookml stub).
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Option A (best practice): straight view on warehouse object
view: fp {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.fp` ;;
}

# Option B (temporary SDT) — looker-skills: prefer NDT for Looker-native rollups;
# for migrated M SQL, SDT is OK only until warehouse view exists.
view: fp_sdt {
  derived_table: {
    sql:
      SELECT [HR].[FP].*   FROM [HR].[FP]
    ;;
  }
  # Declare dimensions for selected columns; set primary_key: yes
}
```

</details>

### `PayType`

- **Recommended pattern:** `lookml_sql_derived_table`
- **Looker object:** warehouse view/table preferred; LookML SQL derived table acceptable if SELECT-only
- **Build in:** `either` (confidence: high)
- **Why:** M wraps a SQL statement. Prefer creating a warehouse view/table with that SQL, then a straight LookML view. A LookML sql-derived table is an acceptable temporary equivalent.
- **Signals:** sql_source, column_casts:4

**Build steps:**

1. Prefer warehouse VIEW/TABLE with the M SQL (or source table).
2. Use straight LookML view with sql_table_name.
3. Use SDT only if warehouse object is not ready yet; migrate off SDT later.

**Checks:**

- [ ] SQL dialect matches Looker connection
- [ ] Results match Power BI query for a sample filter

**SQL stub:** `m_migration/sql/paytype.sql`
**LookML stub:** `m_migration/lookml_stubs/paytype_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Preferred: materialize as warehouse view/table
CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.paytype` AS
select distinct PayTypeID, [Hrly-Salaried] PayType#(lf)from [HR].[PayGroup]
;

-- Alternative (temporary): use the same SELECT inside a LookML derived_table (see lookml stub).
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Option A (best practice): straight view on warehouse object
view: paytype {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.paytype` ;;
}

# Option B (temporary SDT) — looker-skills: prefer NDT for Looker-native rollups;
# for migrated M SQL, SDT is OK only until warehouse view exists.
view: paytype_sdt {
  derived_table: {
    sql:
      select distinct PayTypeID, [Hrly-Salaried] PayType#(lf)from [HR].[PayGroup]
    ;;
  }
  # Declare dimensions for selected columns; set primary_key: yes
}
```

</details>

### `SeparationReason`

- **Recommended pattern:** `lookml_sql_derived_table`
- **Looker object:** warehouse view/table preferred; LookML SQL derived table acceptable if SELECT-only
- **Build in:** `either` (confidence: high)
- **Why:** M wraps a SQL statement. Prefer creating a warehouse view/table with that SQL, then a straight LookML view. A LookML sql-derived table is an acceptable temporary equivalent.
- **Signals:** sql_source, column_casts:3

**Build steps:**

1. Prefer warehouse VIEW/TABLE with the M SQL (or source table).
2. Use straight LookML view with sql_table_name.
3. Use SDT only if warehouse object is not ready yet; migrate off SDT later.

**Checks:**

- [ ] SQL dialect matches Looker connection
- [ ] Results match Power BI query for a sample filter

**SQL stub:** `m_migration/sql/separationreason.sql`
**LookML stub:** `m_migration/lookml_stubs/separationreason_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Preferred: materialize as warehouse view/table
CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.separationreason` AS
SELECT distinct SeparationTypeID, [Vol-Invol] SeparationReason#(lf)  FROM [IP].[HR].[TermReason]
;

-- Alternative (temporary): use the same SELECT inside a LookML derived_table (see lookml stub).
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Option A (best practice): straight view on warehouse object
view: separationreason {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.separationreason` ;;
}

# Option B (temporary SDT) — looker-skills: prefer NDT for Looker-native rollups;
# for migrated M SQL, SDT is OK only until warehouse view exists.
view: separationreason_sdt {
  derived_table: {
    sql:
      SELECT distinct SeparationTypeID, [Vol-Invol] SeparationReason#(lf)  FROM [IP].[HR].[TermReason]
    ;;
  }
  # Declare dimensions for selected columns; set primary_key: yes
}
```

</details>

### `Date`

- **Recommended pattern:** `lookml_sql_derived_table`
- **Looker object:** warehouse view/table preferred; LookML SQL derived table acceptable if SELECT-only
- **Build in:** `either` (confidence: high)
- **Why:** M wraps a SQL statement. Prefer creating a warehouse view/table with that SQL, then a straight LookML view. A LookML sql-derived table is an acceptable temporary equivalent.
- **Signals:** sql_source, column_casts:11

**Build steps:**

1. Prefer warehouse VIEW/TABLE with the M SQL (or source table).
2. Use straight LookML view with sql_table_name.
3. Use SDT only if warehouse object is not ready yet; migrate off SDT later.

**Checks:**

- [ ] SQL dialect matches Looker connection
- [ ] Results match Power BI query for a sample filter

**SQL stub:** `m_migration/sql/date.sql`
**LookML stub:** `m_migration/lookml_stubs/date_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Preferred: materialize as warehouse view/table
CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.date` AS
SELECT [HR].[Date].*   FROM [HR].[Date]
;

-- Alternative (temporary): use the same SELECT inside a LookML derived_table (see lookml stub).
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Option A (best practice): straight view on warehouse object
view: date {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.date` ;;
}

# Option B (temporary SDT) — looker-skills: prefer NDT for Looker-native rollups;
# for migrated M SQL, SDT is OK only until warehouse view exists.
view: date_sdt {
  derived_table: {
    sql:
      SELECT [HR].[Date].*   FROM [HR].[Date]
    ;;
  }
  # Declare dimensions for selected columns; set primary_key: yes
}
```

</details>

### `Employee`

- **Recommended pattern:** `warehouse_transform_model`
- **Looker object:** warehouse transform + straight view (avoid SDT for heavy M)
- **Build in:** `warehouse` (confidence: high)
- **Why:** M contains merge, append/union, or heavy transforms. Looker skills: keep LookML semantic; put ETL in the warehouse.
- **Signals:** sql_source, append_union, transformation_heavy, column_casts:12

**Build steps:**

1. Read phase1/inventory/04_m_raw/Employee.m end-to-end.
2. Implement joins/unions/filters in dbt/Dataform/SQL.
3. Expose curated table to LookML views/employee.view.lkml via sql_table_name.
4. Mark any LookML SDT as temporary technical debt.

**Checks:**

- [ ] Transform tests (unique key, not null) in warehouse
- [ ] Row grain matches Power BI
- [ ] No fan-out vs related facts

**SQL stub:** `m_migration/sql/employee.sql`
**LookML stub:** `m_migration/lookml_stubs/employee_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TRANSFORM MODEL (dbt/Dataform/SQL)
-- Power Query `Employee` has merges/appends/heavy transforms.
-- Best practice: implement transforms in ETL. LookML stays a thin straight view.
-- Do NOT rebuild merge/append logic as LookML derived tables.

CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.employee` AS
SELECT
  CAST(`PayTypeID` AS STRING) AS `PayTypeID`,
  CAST(`date` AS TIMESTAMP) AS `date`,
  CAST(`EmplID` AS INT64) AS `EmplID`,
  CAST(`Gender` AS STRING) AS `Gender`,
  CAST(`Age` AS INT64) AS `Age`,
  CAST(`EthnicGroup` AS STRING) AS `EthnicGroup`,
  CAST(`FP` AS STRING) AS `FP`,
  CAST(`TermDate` AS TIMESTAMP) AS `TermDate`,
  CAST(`BU` AS STRING) AS `BU`,
  CAST(`HireDate` AS TIMESTAMP) AS `HireDate`,
  CAST(`PayTypeID` AS STRING) AS `PayTypeID`,
  CAST(`TermReason` AS STRING) AS `TermReason`
-- TODO: translate M merges/appends/filters from 04_m_raw/Employee.m
FROM `YOUR_PROJECT.YOUR_DATASET.stg_employee_sources`  -- TODO
;

-- dbt-style sketch:
-- models/employee.sql  ->  SELECT ... FROM { ref('upstream') } ...
```

</details>

<details><summary>LookML preview</summary>

```lookml
# After warehouse model exists — straight view only
view: employee {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.employee` ;;
}

# NOT recommended: encoding M merge/append as LookML derived_table SQL.
# If you must bridge temporarily, keep SDT minimal and ticket warehouse ownership.
```

</details>

### `Ethnicity`

- **Recommended pattern:** `warehouse_seed_plus_straight_view`
- **Looker object:** warehouse seed table + straight view (tiny SDT optional)
- **Build in:** `warehouse` (confidence: medium)
- **Why:** Embedded/static M tables should become warehouse seeds. Straight LookML view afterward; SDT only for tiny temporary seeds.
- **Signals:** embedded_static, column_casts:2

**Build steps:**

1. Extract static rows from M into a seed CSV or INSERT script.
2. Load seed to warehouse.
3. Use generated straight LookML view.

**Checks:**

- [ ] Seed row count matches Power BI
- [ ] Types match Changed Type

**SQL stub:** `m_migration/sql/ethnicity.sql`
**LookML stub:** `m_migration/lookml_stubs/ethnicity_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE SEED + straight LookML view
-- Power Query `Ethnicity` looks like an embedded/static table (#table / enter data).
-- Best practice: seed CSV in dbt/Dataform or INSERT seed rows; then straight view.

CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.ethnicity` AS
SELECT
  CAST(`Ethnic Group` AS STRING) AS `Ethnic Group`,
  CAST(`Ethnicity` AS STRING) AS `Ethnicity`
-- TODO: paste literal rows from M #table / Enter Data
FROM UNNEST([])  -- replace with seed rows
;

-- Alternative small SDT (only if seed is tiny and temporary):
-- view with derived_table sql: SELECT ... UNION ALL SELECT ...
```

</details>

<details><summary>LookML preview</summary>

```lookml
view: ethnicity {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.ethnicity` ;;
}

# Tiny static alternative (temporary):
# view: ethnicity_sdt {
#   derived_table: {
#     sql:
#       SELECT 1 AS id, 'example' AS label
#       -- UNION ALL more seed rows from M
#     ;;
#   }
#   dimension: id { primary_key: yes type: number sql: ${TABLE}.id ;; }
# }
```

</details>

### `Gender`

- **Recommended pattern:** `warehouse_seed_plus_straight_view`
- **Looker object:** warehouse seed table + straight view (tiny SDT optional)
- **Build in:** `warehouse` (confidence: medium)
- **Why:** Embedded/static M tables should become warehouse seeds. Straight LookML view afterward; SDT only for tiny temporary seeds.
- **Signals:** embedded_static, column_casts:3

**Build steps:**

1. Extract static rows from M into a seed CSV or INSERT script.
2. Load seed to warehouse.
3. Use generated straight LookML view.

**Checks:**

- [ ] Seed row count matches Power BI
- [ ] Types match Changed Type

**SQL stub:** `m_migration/sql/gender.sql`
**LookML stub:** `m_migration/lookml_stubs/gender_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE SEED + straight LookML view
-- Power Query `Gender` looks like an embedded/static table (#table / enter data).
-- Best practice: seed CSV in dbt/Dataform or INSERT seed rows; then straight view.

CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.gender` AS
SELECT
  CAST(`ID` AS STRING) AS `ID`,
  CAST(`Gender` AS STRING) AS `Gender`,
  CAST(`Sort` AS INT64) AS `Sort`
-- TODO: paste literal rows from M #table / Enter Data
FROM UNNEST([])  -- replace with seed rows
;

-- Alternative small SDT (only if seed is tiny and temporary):
-- view with derived_table sql: SELECT ... UNION ALL SELECT ...
```

</details>

<details><summary>LookML preview</summary>

```lookml
view: gender {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.gender` ;;
}

# Tiny static alternative (temporary):
# view: gender_sdt {
#   derived_table: {
#     sql:
#       SELECT 1 AS id, 'example' AS label
#       -- UNION ALL more seed rows from M
#     ;;
#   }
#   dimension: id { primary_key: yes type: number sql: ${TABLE}.id ;; }
# }
```

</details>

### `AgeGroup`

- **Recommended pattern:** `warehouse_seed_plus_straight_view`
- **Looker object:** warehouse seed table + straight view (tiny SDT optional)
- **Build in:** `warehouse` (confidence: medium)
- **Why:** Embedded/static M tables should become warehouse seeds. Straight LookML view afterward; SDT only for tiny temporary seeds.
- **Signals:** embedded_static, column_casts:2

**Build steps:**

1. Extract static rows from M into a seed CSV or INSERT script.
2. Load seed to warehouse.
3. Use generated straight LookML view.

**Checks:**

- [ ] Seed row count matches Power BI
- [ ] Types match Changed Type

**SQL stub:** `m_migration/sql/agegroup.sql`
**LookML stub:** `m_migration/lookml_stubs/agegroup_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE SEED + straight LookML view
-- Power Query `AgeGroup` looks like an embedded/static table (#table / enter data).
-- Best practice: seed CSV in dbt/Dataform or INSERT seed rows; then straight view.

CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.agegroup` AS
SELECT
  CAST(`AgeGroupID` AS INT64) AS `AgeGroupID`,
  CAST(`AgeGroup` AS STRING) AS `AgeGroup`
-- TODO: paste literal rows from M #table / Enter Data
FROM UNNEST([])  -- replace with seed rows
;

-- Alternative small SDT (only if seed is tiny and temporary):
-- view with derived_table sql: SELECT ... UNION ALL SELECT ...
```

</details>

<details><summary>LookML preview</summary>

```lookml
view: agegroup {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.agegroup` ;;
}

# Tiny static alternative (temporary):
# view: agegroup_sdt {
#   derived_table: {
#     sql:
#       SELECT 1 AS id, 'example' AS label
#       -- UNION ALL more seed rows from M
#     ;;
#   }
#   dimension: id { primary_key: yes type: number sql: ${TABLE}.id ;; }
# }
```

</details>
