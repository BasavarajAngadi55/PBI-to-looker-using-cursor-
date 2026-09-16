-- Preferred: materialize as warehouse view/table
CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.fp` AS
SELECT [HR].[FP].*   FROM [HR].[FP]
;

-- Alternative (temporary): use the same SELECT inside a LookML derived_table (see lookml stub).
