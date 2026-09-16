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
