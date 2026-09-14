# MIGRATION NOTE:
# Source: Power BI Gender — sample uses C/D codes (not M/F)
view: gender {
  label: "Gender"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.gender` ;;

  dimension: id {
    label: "Gender ID"
    primary_key: yes
    type: string
    sql: ${TABLE}.ID ;;
  }

  dimension: gender {
    label: "Gender"
    type: string
    sql: ${TABLE}.Gender ;;
    order_by_field: sort
  }

  dimension: sort {
    label: "Sort"
    type: number
    hidden: yes
    sql: ${TABLE}.Sort ;;
  }
}
