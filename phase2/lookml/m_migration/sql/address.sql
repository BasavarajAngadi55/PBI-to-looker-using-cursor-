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
