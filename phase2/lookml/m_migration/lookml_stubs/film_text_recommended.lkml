# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: film_text {
  label: "film_text"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.film_text` ;;

  # Add dimensions from Phase 1 inventory / generated views/film_text.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: film_text_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_film_text`
#     ;;
#   }
# }
