-- Source Power BI object: Date
-- Original M/DAX dependency: inventory/04_m_raw/Date.m + calculated MonthIncrementNumber
-- Why warehouse transformation is required: Mapping = WAREHOUSE_SQL; MonthIncrementNumber uses MIN(Year) model-wide
-- Downstream LookML objects: views/date.view.lkml; EmpCount PeriodNumber logic

CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.date` AS
SELECT
  Date,
  Month,
  MonthNumber,
  Period,
  PeriodNumber,
  Qtr,
  QtrNumber,
  Year,
  Day,
  MonthStartDate,
  MonthEndDate,
  -- DAX: ([Year]-MIN([Year]))*12 + [MonthNumber]
  (Year - (SELECT MIN(Year) FROM `YOUR_PROJECT.SOURCE_DATASET.date`)) * 12 + MonthNumber AS MonthIncrementNumber
FROM `YOUR_PROJECT.SOURCE_DATASET.date`
;
