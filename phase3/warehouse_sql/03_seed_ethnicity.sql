-- Source Power BI object: Ethnicity (Power Query)
-- Original M/DAX dependency: inventory/04_m_raw/Ethnicity.m (embedded seed)
-- Why warehouse transformation is required: Mapping = WAREHOUSE_SEED
-- Downstream LookML objects: views/ethnicity.view.lkml, employee.ethnic_group join
-- MIGRATION NOTE: Values reconstructed from Phase 1 extract patterns (Group A-G). Validate against PBIX if labels differ.

CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.ethnicity` AS
SELECT '1' AS `Ethnic Group`, 'Group A' AS Ethnicity UNION ALL
SELECT '2', 'Group B' UNION ALL
SELECT '3', 'Group C' UNION ALL
SELECT '4', 'Group D' UNION ALL
SELECT '5', 'Group E' UNION ALL
SELECT '6', 'Group F' UNION ALL
SELECT '7', 'Group G';
