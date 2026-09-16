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
