-- Preferred: materialize as warehouse view/table
CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.date` AS
SELECT [HR].[Date].*   FROM [HR].[Date]
;

-- Alternative (temporary): use the same SELECT inside a LookML derived_table (see lookml stub).
