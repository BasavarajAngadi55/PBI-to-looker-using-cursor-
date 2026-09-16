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
