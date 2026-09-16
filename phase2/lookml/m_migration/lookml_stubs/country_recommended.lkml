# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: country {
  label: "country"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.country` ;;

  # Add dimensions from Phase 1 inventory / generated views/country.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: country_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_country`
#     ;;
#   }
# }
