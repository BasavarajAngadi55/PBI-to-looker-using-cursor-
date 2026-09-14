view: separation_reason {
  label: "Separation Reason"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.separation_reason` ;;

  dimension: separation_type_id {
    label: "Separation Type ID"
    primary_key: yes
    type: string
    sql: ${TABLE}.SeparationTypeID ;;
  }

  dimension: separation_reason {
    label: "Separation Reason"
    type: string
    sql: ${TABLE}.SeparationReason ;;
  }
}
