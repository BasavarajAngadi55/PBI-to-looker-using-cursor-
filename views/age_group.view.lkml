view: age_group {
  label: "Age Group"
  sql_table_name: `hr.age_group` ;;

  dimension: age_group_id {
    label: "Age Group ID"
    description: "1=<30, 2=30-49, 3=50+."
    type: number
    sql: ${TABLE}.AgeGroupID ;;
    primary_key: yes
  }

  dimension: age_group {
    label: "Age Group"
    description: "Age band display label."
    type: string
    sql: ${TABLE}.AgeGroup ;;
  }
}
