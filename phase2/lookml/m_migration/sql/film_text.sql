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
