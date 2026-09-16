# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: film_category {
  label: "film_category"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.film_category` ;;

  # Add dimensions from Phase 1 inventory / generated views/film_category.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: film_category_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_film_category`
#     ;;
#   }
# }
