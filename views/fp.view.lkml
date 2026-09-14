view: fp {
  label: "Full/Part Time"
  sql_table_name: `YOUR_PROJECT.YOUR_DATASET.fp` ;;

  dimension: fp {
    label: "FP"
    primary_key: yes
    type: string
    sql: ${TABLE}.FP ;;
  }

  dimension: fp_desc {
    label: "FP Description"
    type: string
    sql: ${TABLE}.FPDesc ;;
  }
}
