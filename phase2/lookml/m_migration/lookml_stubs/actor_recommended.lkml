# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: actor {
  label: "actor"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.actor` ;;

  # Add dimensions from Phase 1 inventory / generated views/actor.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: actor_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_actor`
#     ;;
#   }
# }
