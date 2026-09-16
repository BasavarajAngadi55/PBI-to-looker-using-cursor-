view: gender {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.gender` ;;
}

# Tiny static alternative (temporary):
# view: gender_sdt {
#   derived_table: {
#     sql:
#       SELECT 1 AS id, 'example' AS label
#       -- UNION ALL more seed rows from M
#     ;;
#   }
#   dimension: id { primary_key: yes type: number sql: ${TABLE}.id ;; }
# }
