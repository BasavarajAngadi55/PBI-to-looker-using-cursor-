-- Preferred: materialize as warehouse view/table
CREATE OR REPLACE VIEW `YOUR_PROJECT.YOUR_DATASET.separationreason` AS
SELECT distinct SeparationTypeID, [Vol-Invol] SeparationReason#(lf)  FROM [IP].[HR].[TermReason]
;

-- Alternative (temporary): use the same SELECT inside a LookML derived_table (see lookml stub).
