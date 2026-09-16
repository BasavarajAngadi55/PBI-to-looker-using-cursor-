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
