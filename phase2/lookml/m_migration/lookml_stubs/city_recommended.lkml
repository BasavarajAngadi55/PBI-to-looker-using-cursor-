# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: city {
  label: "city"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.city` ;;

  # Add dimensions from Phase 1 inventory / generated views/city.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: city_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_city`
#     ;;
#   }
# }
