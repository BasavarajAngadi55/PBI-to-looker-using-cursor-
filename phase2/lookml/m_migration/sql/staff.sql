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
