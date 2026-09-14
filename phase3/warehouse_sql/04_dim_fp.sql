-- Source Power BI object: FP
-- Original M/DAX dependency: inventory/04_m_raw/FP.m → SELECT [HR].[FP].* FROM [HR].[FP]
-- Why warehouse transformation is required: Mapping = WAREHOUSE_SQL (Sql.Database source)
-- Downstream LookML objects: views/fp.view.lkml

CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.fp` AS
SELECT
  FP,
  FPDesc
FROM `YOUR_PROJECT.SOURCE_DATASET.fp`  -- TODO: map to your landed HR.FP extract
;
-- Alternative if loading a one-time extract table:
-- CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.fp` AS SELECT * FROM `YOUR_PROJECT.STAGING.fp_extract`;
