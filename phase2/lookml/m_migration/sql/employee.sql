-- Recommended pattern: WAREHOUSE TRANSFORM MODEL (dbt/Dataform/SQL)
-- Power Query `Employee` has merges/appends/heavy transforms.
-- Best practice: implement transforms in ETL. LookML stays a thin straight view.
-- Do NOT rebuild merge/append logic as LookML derived tables.

CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.employee` AS
SELECT
  CAST(`PayTypeID` AS STRING) AS `PayTypeID`,
  CAST(`date` AS TIMESTAMP) AS `date`,
  CAST(`EmplID` AS INT64) AS `EmplID`,
  CAST(`Gender` AS STRING) AS `Gender`,
  CAST(`Age` AS INT64) AS `Age`,
  CAST(`EthnicGroup` AS STRING) AS `EthnicGroup`,
  CAST(`FP` AS STRING) AS `FP`,
  CAST(`TermDate` AS TIMESTAMP) AS `TermDate`,
  CAST(`BU` AS STRING) AS `BU`,
  CAST(`HireDate` AS TIMESTAMP) AS `HireDate`,
  CAST(`PayTypeID` AS STRING) AS `PayTypeID`,
  CAST(`TermReason` AS STRING) AS `TermReason`
-- TODO: translate M merges/appends/filters from 04_m_raw/Employee.m
FROM `YOUR_PROJECT.YOUR_DATASET.stg_employee_sources`  -- TODO
;

-- dbt-style sketch:
-- models/employee.sql  ->  SELECT ... FROM { ref('upstream') } ...
