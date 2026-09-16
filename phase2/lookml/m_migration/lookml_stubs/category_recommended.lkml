# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: category {
  label: "category"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.category` ;;

  # Add dimensions from Phase 1 inventory / generated views/category.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: category_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_category`
#     ;;
#   }
# }
