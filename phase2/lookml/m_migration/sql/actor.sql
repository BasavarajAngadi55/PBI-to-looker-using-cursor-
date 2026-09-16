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
