-- Preferred: materialize as warehouse view/table
CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.paytype` AS
select distinct PayTypeID, [Hrly-Salaried] PayType#(lf)from [HR].[PayGroup]
;

-- Alternative (temporary): use the same SELECT inside a LookML derived_table (see lookml stub).
