# Power Query M → Looker / warehouse recommendations

**Source:** `movie_rental_analysis.pbix`  
**Queries:** 16  
**Approach:** deterministic (no LLM)

## Best-practice decision order

- 1. Warehouse table/view (ETL/dbt) + straight LookML view (sql_table_name) — preferred
- 2. LookML SQL derived table (SDT) — temporary bridge for light SQL only
- 3. Native derived table (NDT) — rarely a Power Query replacement
- 4. Never put heavy M merges/appends only in LookML

## Pattern summary

| Pattern | Count |
|---|---|
| `warehouse_table_plus_straight_view` | 16 |

## Per-query recommendations

### `actor`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:4

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.actor` with casts matching M Changed Type.
3. Point generated LookML views/actor.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/actor.sql`
**LookML stub:** `m_migration/lookml_stubs/actor_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `actor` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_actor`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.actor` AS
SELECT
  CAST(`actor_id` AS INT64) AS `actor_id`,
  CAST(`first_name` AS STRING) AS `first_name`,
  CAST(`last_name` AS STRING) AS `last_name`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_actor`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Desktop/Capston project/DATA/CSV/actor.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: actor {
  label: "actor"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.actor` ;;

  # Add dimensions from Phase 1 inventory / generated views/actor.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: actor_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_actor`
#     ;;
#   }
# }
```

</details>

### `address`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:9

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.address` with casts matching M Changed Type.
3. Point generated LookML views/address.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/address.sql`
**LookML stub:** `m_migration/lookml_stubs/address_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `address` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_address`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.address` AS
SELECT
  CAST(`address_id` AS INT64) AS `address_id`,
  CAST(`address` AS STRING) AS `address`,
  CAST(`address2` AS STRING) AS `address2`,
  CAST(`district` AS STRING) AS `district`,
  CAST(`city_id` AS INT64) AS `city_id`,
  CAST(`postal_code` AS INT64) AS `postal_code`,
  CAST(`phone` AS INT64) AS `phone`,
  CAST(`location` AS STRING) AS `location`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_address`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/address.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: address {
  label: "address"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.address` ;;

  # Add dimensions from Phase 1 inventory / generated views/address.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: address_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_address`
#     ;;
#   }
# }
```

</details>

### `city`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:4

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.city` with casts matching M Changed Type.
3. Point generated LookML views/city.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/city.sql`
**LookML stub:** `m_migration/lookml_stubs/city_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `city` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_city`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.city` AS
SELECT
  CAST(`city_id` AS INT64) AS `city_id`,
  CAST(`city` AS STRING) AS `city`,
  CAST(`country_id` AS INT64) AS `country_id`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_city`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/city.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: city {
  label: "city"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.city` ;;

  # Add dimensions from Phase 1 inventory / generated views/city.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: city_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_city`
#     ;;
#   }
# }
```

</details>

### `country`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:3

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.country` with casts matching M Changed Type.
3. Point generated LookML views/country.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/country.sql`
**LookML stub:** `m_migration/lookml_stubs/country_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `country` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_country`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.country` AS
SELECT
  CAST(`country_id` AS INT64) AS `country_id`,
  CAST(`country` AS STRING) AS `country`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_country`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/country.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: country {
  label: "country"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.country` ;;

  # Add dimensions from Phase 1 inventory / generated views/country.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: country_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_country`
#     ;;
#   }
# }
```

</details>

### `category`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:3

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.category` with casts matching M Changed Type.
3. Point generated LookML views/category.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/category.sql`
**LookML stub:** `m_migration/lookml_stubs/category_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `category` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_category`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.category` AS
SELECT
  CAST(`category_id` AS INT64) AS `category_id`,
  CAST(`name` AS STRING) AS `name`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_category`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/category.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: category {
  label: "category"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.category` ;;

  # Add dimensions from Phase 1 inventory / generated views/category.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: category_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_category`
#     ;;
#   }
# }
```

</details>

### `film`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:13

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.film` with casts matching M Changed Type.
3. Point generated LookML views/film.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/film.sql`
**LookML stub:** `m_migration/lookml_stubs/film_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `film` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_film`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.film` AS
SELECT
  CAST(`film_id` AS INT64) AS `film_id`,
  CAST(`title` AS STRING) AS `title`,
  CAST(`description` AS STRING) AS `description`,
  CAST(`release_year` AS INT64) AS `release_year`,
  CAST(`language_id` AS INT64) AS `language_id`,
  CAST(`original_language_id` AS INT64) AS `original_language_id`,
  CAST(`rental_duration` AS INT64) AS `rental_duration`,
  CAST(`rental_rate` AS FLOAT64) AS `rental_rate`,
  CAST(`length` AS INT64) AS `length`,
  CAST(`replacement_cost` AS FLOAT64) AS `replacement_cost`,
  CAST(`rating` AS STRING) AS `rating`,
  CAST(`special_features` AS STRING) AS `special_features`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_film`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/film.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: film {
  label: "film"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.film` ;;

  # Add dimensions from Phase 1 inventory / generated views/film.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: film_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_film`
#     ;;
#   }
# }
```

</details>

### `film_actor`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:3

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.film_actor` with casts matching M Changed Type.
3. Point generated LookML views/film_actor.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/film_actor.sql`
**LookML stub:** `m_migration/lookml_stubs/film_actor_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `film_actor` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_film_actor`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.film_actor` AS
SELECT
  CAST(`actor_id` AS INT64) AS `actor_id`,
  CAST(`film_id` AS INT64) AS `film_id`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_film_actor`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/film_actor.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: film_actor {
  label: "film_actor"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.film_actor` ;;

  # Add dimensions from Phase 1 inventory / generated views/film_actor.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: film_actor_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_film_actor`
#     ;;
#   }
# }
```

</details>

### `film_category`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:3

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.film_category` with casts matching M Changed Type.
3. Point generated LookML views/film_category.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/film_category.sql`
**LookML stub:** `m_migration/lookml_stubs/film_category_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `film_category` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_film_category`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.film_category` AS
SELECT
  CAST(`film_id` AS INT64) AS `film_id`,
  CAST(`category_id` AS INT64) AS `category_id`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_film_category`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/film_category.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: film_category {
  label: "film_category"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.film_category` ;;

  # Add dimensions from Phase 1 inventory / generated views/film_category.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: film_category_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_film_category`
#     ;;
#   }
# }
```

</details>

### `film_text`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:3

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.film_text` with casts matching M Changed Type.
3. Point generated LookML views/film_text.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/film_text.sql`
**LookML stub:** `m_migration/lookml_stubs/film_text_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `film_text` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_film_text`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.film_text` AS
SELECT
  CAST(`film_id` AS INT64) AS `film_id`,
  CAST(`title` AS STRING) AS `title`,
  CAST(`description` AS STRING) AS `description`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_film_text`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/film_text.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: film_text {
  label: "film_text"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.film_text` ;;

  # Add dimensions from Phase 1 inventory / generated views/film_text.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: film_text_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_film_text`
#     ;;
#   }
# }
```

</details>

### `inventory`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:4

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.inventory` with casts matching M Changed Type.
3. Point generated LookML views/inventory.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/inventory.sql`
**LookML stub:** `m_migration/lookml_stubs/inventory_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `inventory` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_inventory`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.inventory` AS
SELECT
  CAST(`inventory_id` AS INT64) AS `inventory_id`,
  CAST(`film_id` AS INT64) AS `film_id`,
  CAST(`store_id` AS INT64) AS `store_id`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_inventory`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/inventory.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: inventory {
  label: "inventory"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.inventory` ;;

  # Add dimensions from Phase 1 inventory / generated views/inventory.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: inventory_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_inventory`
#     ;;
#   }
# }
```

</details>

### `language`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:3

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.language` with casts matching M Changed Type.
3. Point generated LookML views/language.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/language.sql`
**LookML stub:** `m_migration/lookml_stubs/language_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `language` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_language`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.language` AS
SELECT
  CAST(`language_id` AS INT64) AS `language_id`,
  CAST(`name` AS STRING) AS `name`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_language`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/language.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: language {
  label: "language"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.language` ;;

  # Add dimensions from Phase 1 inventory / generated views/language.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: language_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_language`
#     ;;
#   }
# }
```

</details>

### `payment`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:7

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.payment` with casts matching M Changed Type.
3. Point generated LookML views/payment.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/payment.sql`
**LookML stub:** `m_migration/lookml_stubs/payment_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `payment` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_payment`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.payment` AS
SELECT
  CAST(`payment_id` AS INT64) AS `payment_id`,
  CAST(`customer_id` AS INT64) AS `customer_id`,
  CAST(`staff_id` AS INT64) AS `staff_id`,
  CAST(`rental_id` AS INT64) AS `rental_id`,
  CAST(`amount` AS FLOAT64) AS `amount`,
  CAST(`payment_date` AS TIMESTAMP) AS `payment_date`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_payment`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/payment.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: payment {
  label: "payment"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.payment` ;;

  # Add dimensions from Phase 1 inventory / generated views/payment.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: payment_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_payment`
#     ;;
#   }
# }
```

</details>

### `rentat`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:7

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.rentat` with casts matching M Changed Type.
3. Point generated LookML views/rentat.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/rentat.sql`
**LookML stub:** `m_migration/lookml_stubs/rentat_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `rentat` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_rentat`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.rentat` AS
SELECT
  CAST(`rental_id` AS INT64) AS `rental_id`,
  CAST(`rental_date` AS TIMESTAMP) AS `rental_date`,
  CAST(`inventory_id` AS INT64) AS `inventory_id`,
  CAST(`customer_id` AS INT64) AS `customer_id`,
  CAST(`return_date` AS TIMESTAMP) AS `return_date`,
  CAST(`staff_id` AS INT64) AS `staff_id`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_rentat`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/rentat.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: rentat {
  label: "rentat"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.rentat` ;;

  # Add dimensions from Phase 1 inventory / generated views/rentat.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: rentat_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_rentat`
#     ;;
#   }
# }
```

</details>

### `staff`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:11

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.staff` with casts matching M Changed Type.
3. Point generated LookML views/staff.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/staff.sql`
**LookML stub:** `m_migration/lookml_stubs/staff_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `staff` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_staff`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.staff` AS
SELECT
  CAST(`staff_id` AS INT64) AS `staff_id`,
  CAST(`first_name` AS STRING) AS `first_name`,
  CAST(`last_name` AS STRING) AS `last_name`,
  CAST(`address_id` AS INT64) AS `address_id`,
  CAST(`picture` AS STRING) AS `picture`,
  CAST(`email` AS STRING) AS `email`,
  CAST(`store_id` AS INT64) AS `store_id`,
  CAST(`active` AS INT64) AS `active`,
  CAST(`username` AS STRING) AS `username`,
  CAST(`password` AS STRING) AS `password`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_staff`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/staff.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: staff {
  label: "staff"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.staff` ;;

  # Add dimensions from Phase 1 inventory / generated views/staff.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: staff_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_staff`
#     ;;
#   }
# }
```

</details>

### `store`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:4

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.store` with casts matching M Changed Type.
3. Point generated LookML views/store.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/store.sql`
**LookML stub:** `m_migration/lookml_stubs/store_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `store` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_store`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.store` AS
SELECT
  CAST(`store_id` AS INT64) AS `store_id`,
  CAST(`manager_staff_id` AS INT64) AS `manager_staff_id`,
  CAST(`address_id` AS INT64) AS `address_id`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_store`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/store.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: store {
  label: "store"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.store` ;;

  # Add dimensions from Phase 1 inventory / generated views/store.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: store_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_store`
#     ;;
#   }
# }
```

</details>

### `customer`

- **Recommended pattern:** `warehouse_table_plus_straight_view`
- **Looker object:** straight view (sql_table_name) over warehouse table
- **Build in:** `warehouse` (confidence: high)
- **Why:** M is a file extract with light Promote Headers / Changed Type. Looker best practice: load to warehouse, then use a normal view — not a derived table.
- **Signals:** file_source, column_casts:9

**Build steps:**

1. Land the CSV/Excel in cloud storage or ingest to a staging table.
2. Create curated table `YOUR_PROJECT.YOUR_DATASET.customer` with casts matching M Changed Type.
3. Point generated LookML views/customer.view.lkml sql_table_name at that table.
4. Do not use File.Contents paths from M in Looker.
5. Optional SDT only as a short-term bridge off an already-loaded staging table.

**Checks:**

- [ ] Warehouse row count ≈ Power BI query row count
- [ ] Key column unique where M implied a grain
- [ ] LookML Validator resolves sql_table_name

**SQL stub:** `m_migration/sql/customer.sql`
**LookML stub:** `m_migration/lookml_stubs/customer_recommended.lkml`

<details><summary>SQL preview</summary>

```sql
-- Recommended pattern: WAREHOUSE TABLE + straight LookML view
-- Power Query `customer` was a file load (CSV/Excel) + light type changes.
-- Best practice: land data in the warehouse, then point LookML sql_table_name at it.
-- Do NOT re-implement File.Contents in Looker.

-- 1) Load / stage (example BigQuery)
-- LOAD DATA INTO `YOUR_PROJECT.YOUR_DATASET.stg_customer`
-- FROM FILES (format='CSV', uris=['gs://YOUR_BUCKET/...'], field_delimiter=';', skip_leading_rows=1);

-- 2) Curated table matching M "Changed Type"
CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.customer` AS
SELECT
  CAST(`customer_id` AS INT64) AS `customer_id`,
  CAST(`store_id` AS INT64) AS `store_id`,
  CAST(`first_name` AS STRING) AS `first_name`,
  CAST(`last_name` AS STRING) AS `last_name`,
  CAST(`email` AS STRING) AS `email`,
  CAST(`address_id` AS INT64) AS `address_id`,
  CAST(`active` AS INT64) AS `active`,
  CAST(`create_date` AS TIMESTAMP) AS `create_date`,
  CAST(`last_update` AS TIMESTAMP) AS `last_update`
FROM `YOUR_PROJECT.YOUR_DATASET.stg_customer`
;

-- Original file hint from M (local path — replace with cloud storage URI):
-- C:/Users/RADHA/Downloads/t/customer.csv
```

</details>

<details><summary>LookML preview</summary>

```lookml
# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: customer {
  label: "customer"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.customer` ;;

  # Add dimensions from Phase 1 inventory / generated views/customer.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: customer_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_customer`
#     ;;
#   }
# }
```

</details>
