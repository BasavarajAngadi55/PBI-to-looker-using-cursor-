-- Source Power BI object: SeparationReason
-- Original M/DAX dependency: inventory/04_m_raw/SeparationReason.m
-- Why warehouse transformation is required: Mapping = WAREHOUSE_SQL
-- Downstream LookML objects: views/separation_reason.view.lkml

CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.separation_reason` AS
SELECT DISTINCT
  SeparationTypeID,
  SeparationReason  -- source: [Vol-Invol]
FROM `YOUR_PROJECT.SOURCE_DATASET.term_reason`
;
