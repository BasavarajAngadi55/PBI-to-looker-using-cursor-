-- Source Power BI object: Gender (Power Query)
-- Original M/DAX dependency: inventory/04_m_raw/Gender.m (embedded seed)
-- Why warehouse transformation is required: Mapping = WAREHOUSE_SEED
-- Downstream LookML objects: views/gender.view.lkml, employee.gender_id join
-- MIGRATION NOTE: Sample PBIX uses C/D codes (not M/F). Confirm against seed decode / PBIX values before production.

CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.gender` AS
SELECT 'D' AS ID, 'Male' AS Gender, 1 AS Sort UNION ALL
SELECT 'C', 'Female', 2;
