# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: film_actor {
  label: "film_actor"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.film_actor` ;;

  # Add dimensions from Phase 1 inventory / generated views/film_actor.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: film_actor_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_film_actor`
#     ;;
#   }
# }
