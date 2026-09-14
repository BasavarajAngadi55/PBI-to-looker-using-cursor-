let
    Source = Sql.Database(".", "IP", [Query="select distinct market BU,#(lf)  REGIONTITLE Region,#(lf)  MARKETDIRECTOR VP#(lf)from hr.bu"]),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"BU", "BU"}, {"Region", "RegionSeq"}, {"VP", "VP"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"BU", type text}, {"RegionSeq", type text}, {"VP", type text}})
in
    #"Changed Type"