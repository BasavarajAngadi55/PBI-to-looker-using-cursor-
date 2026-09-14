view: fp {
  label: "Full / Part Time"
  sql_table_name: `hr.fp` ;;

  dimension: fp {
    label: "FP Code"
    description: "F = Full-Time, P = Part-Time."
    type: string
    sql: ${TABLE}.FP ;;
    primary_key: yes
  }

  dimension: fp_desc {
    label: "FP Description"
    description: "Full-Time / Part-Time label."
    type: string
    sql: ${TABLE}.FPDesc ;;
  }
}
