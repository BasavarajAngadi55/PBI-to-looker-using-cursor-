-- Source Power BI object: Employee (FACT)
-- Original M/DAX dependency: inventory/04_m_raw/Employee.m (complex Sql.Database UNION actives + seps)
-- Why warehouse transformation is required: Mapping = WAREHOUSE_SQL HIGH; all HR KPIs depend on this grain
-- Downstream LookML objects: views/employee.view.lkml (all measures); explore joins
--
-- MIGRATION NOTE:
-- Source: Power BI Employee.m
-- Decision: Provide BigQuery-shaped template mirroring M SQL (date +1 year, gender M→C else D, EmplID%2=0, month-end snapshots)
-- Reason: Looker cannot run Power Query; warehouse must materialize actives UNION seps
-- Suggestion: Replace SOURCE_DATASET placeholders with your landed IP/HR extracts; validate row counts vs PBIX
--
-- TODO: USER INPUT REQUIRED — map YOUR_PROJECT.SOURCE_DATASET.* to actual landed tables
-- TODO: KPI parity validation required after load

CREATE OR REPLACE TABLE `YOUR_PROJECT.YOUR_DATASET.employee` AS
WITH
actives AS (
  SELECT
    DATE_ADD(d.Date, INTERVAL 1 YEAR) AS date,
    b.Market AS BU,
    e.EmplID AS EmplID,
    IF(e.Gender = 'M', 'C', 'D') AS Gender,
    e.Age - (2013 - EXTRACT(YEAR FROM d.Date)) AS Age,
    e.EthnicGroup AS EthnicGroup,
    e.FP AS FP,
    DATE_ADD(e.SenDate, INTERVAL 1 YEAR) AS HireDate,
    p.PayTypeID AS PayTypeID,
    CAST(NULL AS DATE) AS TermDate,
    CAST(NULL AS STRING) AS TermReason
  FROM `YOUR_PROJECT.SOURCE_DATASET.all_emps` e
  CROSS JOIN `YOUR_PROJECT.SOURCE_DATASET.date` d
  INNER JOIN `YOUR_PROJECT.SOURCE_DATASET.bu` b ON b.UNIT = e.Unit
  INNER JOIN `YOUR_PROJECT.SOURCE_DATASET.pay_group` p ON p.PayGroup = e.PayGroup
  WHERE d.Day = 1
    AND e.SenDate <= d.MonthEndDate
    AND COALESCE(e.TermDate, DATE '9999-01-01') >= d.MonthEndDate
    AND d.Date < DATE '2014-01-01'
    AND MOD(e.EmplID, 2) = 0
),
seps AS (
  SELECT
    DATE_ADD(d.Date, INTERVAL 1 YEAR) AS date,
    b.Market AS BU,
    e.EmplID AS EmplID,
    IF(e.Gender = 'M', 'C', 'D') AS Gender,
    e.Age - (2013 - EXTRACT(YEAR FROM d.Date)) AS Age,
    e.EthnicGroup AS EthnicGroup,
    e.FP AS FP,
    DATE_ADD(e.SenDate, INTERVAL 1 YEAR) AS HireDate,
    p.PayTypeID AS PayTypeID,
    DATE_ADD(e.TermDate, INTERVAL 1 YEAR) AS TermDate,
    t.SeparationTypeID AS TermReason
  FROM `YOUR_PROJECT.SOURCE_DATASET.all_emps` e
  CROSS JOIN `YOUR_PROJECT.SOURCE_DATASET.date` d
  INNER JOIN `YOUR_PROJECT.SOURCE_DATASET.bu` b ON b.UNIT = e.Unit
  INNER JOIN `YOUR_PROJECT.SOURCE_DATASET.pay_group` p ON p.PayGroup = e.PayGroup
  INNER JOIN `YOUR_PROJECT.SOURCE_DATASET.term_reason` t
    ON t.`Term-Discharge` = e.`Term-Discharge`
  WHERE d.Day = 1
    AND e.TermDate <= d.MonthEndDate
    AND e.TermDate >= d.MonthStartDate
    AND d.Date < DATE '2014-01-01'
    AND MOD(e.EmplID, 2) = 0
),
base AS (
  SELECT * FROM actives
  UNION ALL
  SELECT * FROM seps
)
SELECT
  date,
  EmplID,
  Gender,
  Age,
  EthnicGroup,
  FP,
  TermDate,
  BU,
  HireDate,
  PayTypeID,
  TermReason,
  -- Calculated columns (from Employee DAX) — materialize for performance
  CASE
    WHEN EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM HireDate)
     AND EXTRACT(MONTH FROM date) = EXTRACT(MONTH FROM HireDate)
    THEN 1 ELSE NULL
  END AS isNewHire,
  CASE
    WHEN Age < 30 THEN 1
    WHEN Age < 50 THEN 2
    ELSE 3
  END AS AgeGroupID,
  ABS(DATE_DIFF(date, HireDate, DAY)) AS TenureDays,
  CAST(CEIL(ABS(DATE_DIFF(date, HireDate, DAY)) / 30.0) - 1 AS INT64) AS TenureMonths,
  CASE
    WHEN TermDate IS NULL THEN 0
    WHEN DATE_DIFF(TermDate, HireDate, DAY) >= 61 THEN 0
    ELSE 1
  END AS BadHires
FROM base
;
