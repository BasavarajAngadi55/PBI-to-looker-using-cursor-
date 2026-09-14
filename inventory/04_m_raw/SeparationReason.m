let
    Source = Sql.Database(".", "IP", [Query="SELECT distinct SeparationTypeID, [Vol-Invol] SeparationReason#(lf)  FROM [IP].[HR].[TermReason]"]),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"SeparationTypeID", "SeparationTypeID"}, {"SeparationReason", "SeparationReason"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"SeparationTypeID", type text}, {"SeparationReason", type text}})
in
    #"Changed Type"