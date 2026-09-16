-- Preferred: materialize as warehouse view/table
CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.bu` AS
select distinct market BU,#(lf)  REGIONTITLE Region,#(lf)  MARKETDIRECTOR VP#(lf)from hr.bu
;

-- Alternative (temporary): use the same SELECT inside a LookML derived_table (see lookml stub).
