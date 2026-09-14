view: pay_type {
  label: "Pay Type"
  sql_table_name: `hr.pay_type` ;;

  dimension: pay_type_id {
    label: "Pay Type ID"
    description: "H = Hourly, S = Salaried."
    type: string
    sql: ${TABLE}.PayTypeID ;;
    primary_key: yes
  }

  dimension: pay_type {
    label: "Pay Type"
    description: "Hourly / Salaried label."
    type: string
    sql: ${TABLE}.PayType ;;
  }
}
