view: ethnicity {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.ethnicity` ;;
}

# Tiny static alternative (temporary):
# view: ethnicity_sdt {
#   derived_table: {
#     sql:
#       SELECT 1 AS id, 'example' AS label
#       -- UNION ALL more seed rows from M
#     ;;
#   }
#   dimension: id { primary_key: yes type: number sql: ${TABLE}.id ;; }
# }
