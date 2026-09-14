let
    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlTSUYopNTAwTjY2UIrViVYyAgoYG+iaWIJ5xkCeqYG2UmwsAA==", BinaryEncoding.Base64), Compression.Deflate))),
    #"Renamed Columns" = Table.RenameColumns(Source, {{"Column1", "AgeGroupID"}, {"Column2", "AgeGroup"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns", {{"AgeGroupID", Int64.Type}, {"AgeGroup", type text}})
 in
    #"Changed Type"