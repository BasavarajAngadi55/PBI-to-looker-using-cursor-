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
