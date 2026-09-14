let
    Source = Sql.Database(".", "IP", [Query="select distinct PayTypeID, [Hrly-Salaried] PayType#(lf)from [HR].[PayGroup]"]),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"PayTypeID", "PayTypeID"}, {"PayType", "PayType"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"PayTypeID", type text}, {"PayType", type text}})
in
    #"Changed Type"