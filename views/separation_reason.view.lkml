view: separation_reason {
  label: "Separation Reason"
  sql_table_name: `hr.separation_reason` ;;

  dimension: separation_type_id {
    label: "Separation Type ID"
    description: "V = Voluntary, U = Involuntary."
    type: string
    sql: ${TABLE}.SeparationTypeID ;;
    primary_key: yes
  }

  dimension: separation_reason {
    label: "Separation Reason"
    description: "Voluntary / Involuntary label."
    type: string
    sql: ${TABLE}.SeparationReason ;;
  }
}