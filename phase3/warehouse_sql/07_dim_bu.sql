-- Source Power BI object: BU
-- Original M/DAX dependency: inventory/04_m_raw/BU.m + calculated column Region (MID RegionSeq)
-- Why warehouse transformation is required: Mapping = WAREHOUSE_SQL; Region calc preferred in warehouse
-- Downstream LookML objects: views/bu.view.lkml (region dimension)

CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.bu` AS
SELECT DISTINCT
  market AS BU,
  REGIONTITLE AS RegionSeq,
  MARKETDIRECTOR AS VP,
  -- DAX: MID([RegionSeq], 3, 15) → characters after ordinal prefix e.g. "1-North" → "North"
  SUBSTR(REGIONTITLE, 3) AS Region
FROM `YOUR_PROJECT.SOURCE_DATASET.bu`
;
