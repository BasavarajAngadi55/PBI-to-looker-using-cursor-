# Preferred LookML after warehouse load (straight view — NOT a derived table)
view: customer {
  label: "customer"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.customer` ;;

  # Add dimensions from Phase 1 inventory / generated views/customer.view.lkml
  # Keep primary_key: yes on the natural key.
}

# Temporary alternative ONLY if warehouse load is blocked (not best practice for file M):
# view: customer_sdt {
#   derived_table: {
#     sql:
#       SELECT * FROM `YOUR_PROJECT.YOUR_DATASET.stg_customer`
#     ;;
#   }
# }
