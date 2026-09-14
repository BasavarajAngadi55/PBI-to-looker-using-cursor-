let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUXIvyi8tUHBUitWJVjKC853AfGM43xnMN4HzXcB8UzjfFcw3g/PdwHxzON9dKTYWAA==", BinaryEncoding.Base64), Compression.Deflate))),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"Column1", "Ethnic Group"}, {"Column2", "Ethnicity"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"Ethnic Group", type text}, {"Ethnicity", type text}})
 in
    #"Changed Type"
