let
    Source = Sql.Database(".", "IP", [Query="SELECT [HR].[FP].*   FROM [HR].[FP]"]),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"FP", "FP"}, {"FPDesc", "FPDesc"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"FP", type text}, {"FPDesc", type text}})
in
    #"Changed Type"
