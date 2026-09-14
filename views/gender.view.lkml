view: gender {
  label: "Gender"
  sql_table_name: `hr.gender` ;;

  dimension: id {
    label: "Gender ID"
    description: "Gender code used on Employee (sample: D=Male, C=Female)."
    type: string
    sql: ${TABLE}.ID ;;
    primary_key: yes
  }

  dimension: gender {
    label: "Gender"
    description: "Gender display label."
    type: string
    sql: ${TABLE}.Gender ;;
    order_by_field: sort
  }

  dimension: sort {
    label: "Sort"
    description: "Display sort order."
    type: number
    sql: ${TABLE}.Sort ;;
  }
}
