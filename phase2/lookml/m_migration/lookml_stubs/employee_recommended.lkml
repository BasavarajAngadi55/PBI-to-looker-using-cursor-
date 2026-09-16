# After warehouse model exists — straight view only
view: employee {
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.employee` ;;
}

# NOT recommended: encoding M merge/append as LookML derived_table SQL.
# If you must bridge temporarily, keep SDT minimal and ticket warehouse ownership.
