-- Source Power BI object: PayType
-- Original M/DAX dependency: inventory/04_m_raw/PayType.m
-- Why warehouse transformation is required: Mapping = WAREHOUSE_SQL
-- Downstream LookML objects: views/pay_type.view.lkml

CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.pay_type` AS
SELECT DISTINCT
  PayTypeID,
  PayType  -- source alias: [Hrly-Salaried]
FROM `YOUR_PROJECT.SOURCE_DATASET.pay_group`
;
