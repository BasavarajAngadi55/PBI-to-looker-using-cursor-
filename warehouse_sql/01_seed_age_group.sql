-- Source Power BI object: AgeGroup (Power Query)
-- Original M/DAX dependency: inventory/04_m_raw/AgeGroup.m (embedded Table.FromRows seed)
-- Why warehouse transformation is required: Mapping = WAREHOUSE_SEED; embedded static table cannot be queried by Looker until loaded.
-- Downstream LookML objects: views/age_group.view.lkml, employee.age_group_id join

CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.age_group` AS
SELECT 1 AS AgeGroupID, '<30' AS AgeGroup UNION ALL
SELECT 2, '30-49' UNION ALL
SELECT 3, '50+';
