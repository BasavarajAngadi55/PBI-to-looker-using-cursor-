view: pay_type {
  label: "Pay Type"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.pay_type` ;;

  dimension: pay_type_id {
    label: "Pay Type ID"
    primary_key: yes
    type: string
    sql: ${TABLE}.PayTypeID ;;
  }

  dimension: pay_type {
    label: "Pay Type"
    type: string
    sql: ${TABLE}.PayType ;;
  }
}
